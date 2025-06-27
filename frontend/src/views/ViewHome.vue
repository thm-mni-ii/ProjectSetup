<template>
  <v-container fluid class="home">
    <v-row justify="center" align="center" class="home__row">
      <v-col cols="12" md="8" lg="6" class="home__col">
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

            <div class="user-details">
              <h3 class="text-h6 mb-3">Benutzerinformationen</h3>
              <v-row>
                <v-col cols="12" sm="6">
                  <v-card variant="outlined" class="pa-3">
                    <div class="text-center">
                      <v-icon size="24" color="primary" class="mb-2">mdi-account</v-icon>
                      <p class="text-body-2 text-medium-emphasis mb-1">Benutzername</p>
                      <p class="text-body-1 font-weight-medium">{{ user.username }}</p>
                    </div>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-card variant="outlined" class="pa-3">
                    <div class="text-center">
                      <v-icon size="24" color="success" class="mb-2">mdi-calendar</v-icon>
                      <p class="text-body-2 text-medium-emphasis mb-1">Registriert</p>
                      <p class="text-body-1 font-weight-medium">{{ formatDate(user.created_at) }}</p>
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

const user = ref<User | null>(null)

onMounted(() => {
  loadUserFromStorage()
})

const loadUserFromStorage = () => {
  try {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      user.value = JSON.parse(storedUser)
    }
  } catch (error) {
    console.error('Fehler beim Laden der Benutzerdaten:', error)
    user.value = null
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

  .user-details {
    .v-card {
      &:hover {
        transform: translateY(-2px);
      }
    }
  }
}
</style>
