<template>
  <v-app-bar :elevation="2" color="primary" dark prominent class="app-header">
    <v-app-bar-title class="title-text">
      <router-link to="/" class="title-link"><v-icon size="32" class="mr-2">mdi-storefront</v-icon> Marktplatz </router-link>
    </v-app-bar-title>

    <v-spacer></v-spacer>

    <template #append>
      <!-- Eingeloggt: Benutzer-Avatar und Logout -->
      <div v-if="user" class="user-section d-flex align-center">
        <v-avatar color="light-blue" size="40" class="mr-3">
          <span class="text-body-1 font-weight-bold">
            {{ userInitials }}
          </span>
        </v-avatar>

        <div class="user-info d-none d-sm-block mr-3">
          <div class="text-body-2 font-weight-medium">{{ user.username }}</div>
          <div class="text-caption opacity-75">ID: {{ user.id }}</div>
        </div>

        <v-menu>
          <template #activator="{ props }">
            <v-btn v-bind="props" icon="mdi-chevron-down" variant="text" size="small"></v-btn>
          </template>

          <v-list>
            <v-list-item @click="$router.push('/')">
              <template #prepend>
                <v-icon>mdi-account</v-icon>
              </template>
              <v-list-item-title>Profil</v-list-item-title>
            </v-list-item>

            <v-list-item @click="logout">
              <template #prepend>
                <v-icon>mdi-logout</v-icon>
              </template>
              <v-list-item-title>Abmelden</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>

      <!-- Nicht eingeloggt: Login und Register Buttons -->
      <div v-else class="auth-buttons d-flex align-center">
        <v-btn to="/login" active-class="active" prepend-icon="mdi-login" color="white" variant="text" class="mr-2">
          <span>Login</span>
          <v-tooltip activator="parent" location="bottom"> Anmelden </v-tooltip>
        </v-btn>

        <v-btn to="/register" active-class="active" prepend-icon="mdi-account-plus" color="white" variant="outlined" size="small">
          <span>Registrieren</span>
          <v-tooltip activator="parent" location="bottom"> Neues Konto erstellen </v-tooltip>
        </v-btn>
      </div>
    </template>
  </v-app-bar>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type User from '@/model/User'

const router = useRouter()
const user = ref<User | null>(null)

// Benutzerinitialen für Avatar berechnen
const userInitials = computed(() => {
  if (!user.value?.username) return ''
  const words = user.value.username.split(' ')
  if (words.length > 1) {
    return words[0][0].toUpperCase() + words[1][0].toUpperCase()
  }
  return user.value.username.substring(0, 2).toUpperCase()
})

// Benutzerdaten aus Local Storage laden
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

// Logout-Funktion
const logout = () => {
  localStorage.removeItem('user')
  localStorage.removeItem('token')
  user.value = null
  router.push('/login')
}

onMounted(() => {
  loadUserFromStorage()

  // Listen for storage changes to update user data
  window.addEventListener('storage', (e) => {
    if (e.key === 'user') {
      loadUserFromStorage()
    }
  })
})
</script>

<style scoped lang="scss">
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;

  .title-link {
    color: white;
    text-decoration: none;
    font-weight: 600;
    font-size: 1.25rem;
    transition: opacity 0.3s ease;

    &:hover {
      opacity: 0.8;
    }
  }

  .user-section {
    .v-avatar {
      border: 2px solid rgba(255, 255, 255, 0.3);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }

    .user-info {
      color: white;
      text-align: right;
    }
  }

  .auth-buttons {
    .v-btn {
      margin-left: 8px;

      &.v-btn--variant-outlined {
        border-color: rgba(255, 255, 255, 0.5);

        &:hover {
          background-color: rgba(255, 255, 255, 0.1);
        }
      }

      &.v-btn--variant-text:hover {
        background-color: rgba(255, 255, 255, 0.1);
      }
    }
  }
}

.icon {
  height: 35px;
  width: auto;
  margin-right: 20px;
}
</style>
