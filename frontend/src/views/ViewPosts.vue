<template>
  <v-container class="posts-view">
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-6">
          <h1 class="text-h4 font-weight-bold">Blog Posts</h1>
          <v-btn color="primary" prepend-icon="mdi-plus" size="large" @click="$router.push('/posts/create')"> Neuer Post </v-btn>
        </div>

        <v-row>
          <v-col v-for="post in posts" :key="post.id" cols="12" md="6" lg="4">
            <v-card class="post-card h-100" hover @click="$router.push(`/posts/${post.id}`)">
              <v-card-title class="text-h6">
                {{ post.title }}
              </v-card-title>

              <v-card-subtitle class="d-flex align-center">
                <v-avatar size="24" color="primary" class="mr-2">
                  <span class="text-caption text-white">
                    {{ post.author_username.substring(0, 2).toUpperCase() }}
                  </span>
                </v-avatar>
                {{ post.author_username }}
                <v-spacer />
                <span class="text-caption">
                  {{ formatDate(post.created_at) }}
                </span>
              </v-card-subtitle>

              <v-card-text>
                <p class="text-body-2 text-truncate-3">
                  {{ post.content }}
                </p>
              </v-card-text>

              <v-card-actions>
                <v-chip size="small" prepend-icon="mdi-comment" variant="outlined"> {{ post.comments.length }} Kommentare </v-chip>
                <v-spacer />
                <v-btn icon="mdi-arrow-right" variant="text" size="small" @click.stop="$router.push(`/posts/${post.id}`)" />
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

        <!-- Empty State -->
        <v-card v-if="posts.length === 0" class="text-center pa-8">
          <v-icon size="64" color="grey-lighten-2" class="mb-4">mdi-post-outline</v-icon>
          <h3 class="text-h6 mb-2">Noch keine Posts vorhanden</h3>
          <p class="text-body-2 text-medium-emphasis mb-4">Erstelle den ersten Blog-Post für diese Community!</p>
          <v-btn color="primary" prepend-icon="mdi-plus" @click="$router.push('/posts/create')"> Ersten Post erstellen </v-btn>
        </v-card>

        <!-- Pagination -->
        <div v-if="posts.length > 0" class="text-center mt-6">
          <v-pagination v-model="currentPage" :length="Math.ceil(totalPosts / pageSize)" color="primary" @update:model-value="loadPosts" />
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Post } from '@/model/Post'
import BlogService from '@/services/service.blog'

const posts = ref<Post[]>([])
const currentPage = ref(1)
const pageSize = ref(6)
const totalPosts = ref(0)

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('de-DE', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadPosts = async () => {
  try {
    const skip = (currentPage.value - 1) * pageSize.value
    const response = await BlogService.getPosts(skip, pageSize.value)
    posts.value = response.data

    // Für Demo-Zwecke nehmen wir an, dass es mehr Posts geben könnte
    totalPosts.value = response.data.length < pageSize.value ? skip + response.data.length : skip + response.data.length + 1
  } catch (err: any) {
    console.error('Fehler beim Laden der Posts:', err)
  }
}

onMounted(() => {
  loadPosts()
})
</script>

<style scoped>
.post-card {
  transition: transform 0.2s ease;
  cursor: pointer;
}

.post-card:hover {
  transform: translateY(-2px);
}
</style>
