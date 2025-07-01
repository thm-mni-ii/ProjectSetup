<template>
  <v-container fluid class="home">
    <v-row justify="center" align="center" class="home__row">
      <v-col cols="12" md="10" lg="8" class="home__col">
        <v-card class="pa-6">
          <div v-if="user" class="user-profile">
            <div class="d-flex align-center mb-4">
              <v-avatar color="primary" size="80" class="mr-4">
                <span class="text-h4 font-weight-bold text-white">
                  {{ userInitials }}
                </span>
              </v-avatar>
              <div>
                <h2 class="text-h5 mb-1">{{ user.username }}</h2>
                <p class="text-body-2 text-medium-emphasis mb-0">ID: {{ user.id }}</p>
                <p class="text-body-2 text-medium-emphasis">Mitglied seit: {{ formatDate(user.created_at) }}</p>
              </div>
            </div>

            <v-divider class="mb-4"></v-divider>

            <!-- Quick Actions -->
            <div class="mb-6">
              <h3 class="text-h6 mb-3">Schnellzugriff</h3>
              <v-row>
                <v-col cols="12" sm="6" md="3">
                  <v-card variant="outlined" class="pa-3 text-center action-card" hover @click="$router.push('/posts')">
                    <v-icon size="32" color="primary" class="mb-2">mdi-post</v-icon>
                    <p class="text-body-2 font-weight-medium mb-1">Alle Posts</p>
                    <p class="text-caption text-medium-emphasis">Blog-Posts anzeigen</p>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="6" md="3">
                  <v-card variant="outlined" class="pa-3 text-center action-card" hover @click="$router.push('/posts/create')">
                    <v-icon size="32" color="success" class="mb-2">mdi-plus</v-icon>
                    <p class="text-body-2 font-weight-medium mb-1">Neuer Post</p>
                    <p class="text-caption text-medium-emphasis">Blog-Post erstellen</p>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="6" md="3">
                  <v-card variant="outlined" class="pa-3 text-center action-card" hover @click="$router.push('/statistics')">
                    <v-icon size="32" color="info" class="mb-2">mdi-chart-line</v-icon>
                    <p class="text-body-2 font-weight-medium mb-1">Statistiken</p>
                    <p class="text-caption text-medium-emphasis">Nutzer-Statistiken</p>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="6" md="3">
                  <v-card variant="outlined" class="pa-3 text-center action-card" hover>
                    <v-icon size="32" color="warning" class="mb-2">mdi-account</v-icon>
                    <p class="text-body-2 font-weight-medium mb-1">Profil</p>
                    <p class="text-caption text-medium-emphasis">Konto verwalten</p>
                  </v-card>
                </v-col>
              </v-row>
            </div>

            <!-- User Stats -->
            <div v-if="userStats" class="mb-6">
              <h3 class="text-h6 mb-3">Meine Aktivität</h3>
              <v-row>
                <v-col cols="12" sm="6">
                  <v-card variant="outlined" class="pa-3">
                    <div class="text-center">
                      <v-icon size="24" color="primary" class="mb-2">mdi-post</v-icon>
                      <p class="text-body-2 text-medium-emphasis mb-1">Meine Posts</p>
                      <p class="text-h6 font-weight-bold">{{ userStats.postCount }}</p>
                    </div>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-card variant="outlined" class="pa-3">
                    <div class="text-center">
                      <v-icon size="24" color="success" class="mb-2">mdi-calendar</v-icon>
                      <p class="text-body-2 text-medium-emphasis mb-1">Registriert</p>
                      <p class="text-h6 font-weight-bold">{{ formatDate(user.created_at) }}</p>
                    </div>
                  </v-card>
                </v-col>
              </v-row>
            </div>

            <!-- Recent Posts -->
            <div v-if="recentPosts.length > 0">
              <h3 class="text-h6 mb-3">Meine letzten Posts</h3>
              <v-row>
                <v-col v-for="post in recentPosts" :key="post.id" cols="12" sm="6">
                  <v-card variant="outlined" class="pa-3 post-preview" hover @click="$router.push(`/posts/${post.id}`)">
                    <h4 class="text-body-1 font-weight-medium mb-2">{{ post.title }}</h4>
                    <p class="text-body-2 text-medium-emphasis mb-2 text-truncate">
                      {{ post.content }}
                    </p>
                    <div class="d-flex justify-space-between align-center">
                      <span class="text-caption">{{ formatDate(post.created_at) }}</span>
                      <v-chip size="x-small" variant="outlined"> {{ post.comments.length }} Kommentare </v-chip>
                    </div>
                  </v-card>
                </v-col>
              </v-row>
            </div>
          </div>

          <div v-else class="text-center pa-8">
            <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-account-off</v-icon>
            <h3 class="text-h6 mb-2">Keine Benutzerdaten gefunden</h3>
            <p class="text-body-2 text-medium-emphasis">Bitte melden Sie sich an, um Ihre Profildaten zu sehen.</p>
            <v-btn color="primary" variant="elevated" class="mt-4" @click="$router.push('/login')"> Anmelden </v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type User from '@/model/User'
import type { Post } from '@/model/Post'
import BlogService from '@/services/service.blog'

const user = ref<User | null>(null)
const userStats = ref<{ postCount: number } | null>(null)
const recentPosts = ref<Post[]>([])

onMounted(() => {
  loadUserFromStorage()
  if (user.value) {
    loadUserStats()
    loadRecentPosts()
  }
})

const loadUserFromStorage = () => {
  try {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      user.value = JSON.parse(storedUser)
    }
  } catch (error) {
    console.error('Fehler beim Laden der Benutzerdaten:', error)
  }
}

const loadUserStats = async () => {
  if (!user.value) return

  try {
    const response = await BlogService.getUserPosts(user.value.id.toString())
    userStats.value = {
      postCount: response.data.length
    }
  } catch (error) {
    console.error('Fehler beim Laden der Benutzerstatistiken:', error)
  }
}

const loadRecentPosts = async () => {
  if (!user.value) return

  try {
    const response = await BlogService.getUserPosts(user.value.id.toString())
    recentPosts.value = response.data.slice(0, 4) // Nur die letzten 4 Posts
  } catch (error) {
    console.error('Fehler beim Laden der Posts:', error)
  }
}

// Benutzerinitialen für Avatar berechnen
const userInitials = computed(() => {
  if (!user.value?.username) return ''
  const words = user.value.username.split(' ')
  if (words.length > 1) {
    return words[0][0].toUpperCase() + words[1][0].toUpperCase()
  }
  return user.value.username.substring(0, 2).toUpperCase()
})

// Datum formatieren
const formatDate = (dateString: string | Date) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('de-DE', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped lang="scss">
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.user-profile {
  .v-avatar {
    border: 3px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
}

.action-card {
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
  cursor: pointer;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
}

.post-preview {
  transition: transform 0.2s ease;
  cursor: pointer;

  &:hover {
    transform: translateY(-1px);
  }
}
</style>
