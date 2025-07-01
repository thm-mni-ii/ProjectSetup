<template>
  <v-container class="post-detail-view">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card v-if="post" class="mb-6">
          <!-- Post Header -->
          <v-card-title class="text-h4 pa-6 pb-2">
            {{ post.title }}
          </v-card-title>

          <v-card-subtitle class="px-6 pb-4">
            <div class="d-flex align-center">
              <v-avatar size="32" color="primary" class="mr-3">
                <span class="text-body-2 text-white">
                  {{ post.author_username.substring(0, 2).toUpperCase() }}
                </span>
              </v-avatar>
              <div>
                <div class="text-body-2 font-weight-medium">{{ post.author_username }}</div>
                <div class="text-caption text-medium-emphasis">
                  {{ formatDate(post.created_at) }}
                </div>
              </div>
            </div>
          </v-card-subtitle>

          <v-card-text class="px-6 py-4">
            <div class="text-body-1" style="white-space: pre-wrap; line-height: 1.7">
              {{ post.content }}
            </div>
          </v-card-text>

          <v-divider />

          <v-card-text class="px-6 py-4">
            <div class="d-flex align-center mb-4">
              <h3 class="text-h6">
                <v-icon class="mr-2">mdi-comment</v-icon>
                Kommentare ({{ post.comments.length }})
              </h3>
            </div>

            <v-card variant="outlined" class="mb-4">
              <v-card-text>
                <v-form @submit.prevent="addComment">
                  <v-textarea v-model="newComment" label="Neuen Kommentar schreiben..." variant="outlined" rows="3" :rules="[rules.required]" :error-messages="commentErrors" class="mb-3" />

                  <div class="text-right">
                    <v-btn type="submit" color="primary" prepend-icon="mdi-send" :loading="commentLoading" :disabled="!newComment.trim()" size="small"> Kommentar hinzufügen </v-btn>
                  </div>
                </v-form>
              </v-card-text>
            </v-card>

            <div v-if="post.comments.length > 0" class="comments-list">
              <v-card v-for="(comment, index) in post.comments" :key="index" variant="outlined" class="mb-3">
                <v-card-text class="py-3">
                  <div class="d-flex align-start">
                    <v-avatar size="28" color="secondary" class="mr-3 mt-1">
                      <span class="text-caption text-white">
                        {{ comment.author_username.substring(0, 2).toUpperCase() }}
                      </span>
                    </v-avatar>
                    <div class="flex-grow-1">
                      <div class="d-flex justify-space-between align-center mb-2">
                        <span class="text-body-2 font-weight-medium">
                          {{ comment.author_username }}
                        </span>
                        <span class="text-caption text-medium-emphasis">
                          {{ formatDate(comment.created_at) }}
                        </span>
                      </div>
                      <p class="text-body-2 mb-0" style="white-space: pre-wrap">
                        {{ comment.text }}
                      </p>
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </div>

            <div v-else class="text-center py-8">
              <v-icon size="48" color="grey-lighten-2" class="mb-3">mdi-comment-outline</v-icon>
              <p class="text-body-2 text-medium-emphasis">Noch keine Kommentare vorhanden. Sei der Erste!</p>
            </div>
          </v-card-text>
        </v-card>

        <div class="text-center">
          <v-btn prepend-icon="mdi-arrow-left" variant="outlined" @click="$router.push('/posts')"> Zurück zu den Posts </v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type { Post } from '@/model/Post'
import BlogService from '@/services/service.blog'

const route = useRoute()

const post = ref<Post | null>(null)

const newComment = ref('')
const commentLoading = ref(false)
const commentErrors = ref<string[]>([])

const rules = {
  required: (value: string) => !!value || 'Kommentar darf nicht leer sein'
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('de-DE', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadPost = async () => {
  const postId = route.params.id as string
  if (!postId) return

  try {
    const response = await BlogService.getPost(postId)
    post.value = response.data
  } catch (err: any) {
    console.error('Fehler beim Laden des Posts:', err)
  }
}

const addComment = async () => {
  if (!newComment.value.trim() || !post.value) return

  commentLoading.value = true
  commentErrors.value = []

  try {
    await BlogService.addComment(post.value.id, {
      text: newComment.value.trim()
    })

    // Post neu laden um den neuen Kommentar zu sehen
    await loadPost()
    newComment.value = ''
  } catch (err: any) {
    commentErrors.value = [err.response?.data?.detail || 'Fehler beim Hinzufügen des Kommentars']
  } finally {
    commentLoading.value = false
  }
}

onMounted(() => {
  loadPost()
})
</script>

<style scoped>
.post-detail-view {
  padding-top: 2rem;
}

.comments-list {
  max-height: 500px;
  overflow-y: auto;
}
</style>
