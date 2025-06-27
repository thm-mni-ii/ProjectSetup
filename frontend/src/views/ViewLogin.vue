<template>
  <div class="login-container">
    <v-card class="login-card">
      <v-card-title class="text-h5">Login</v-card-title>
      <v-card-text>
        <v-form ref="form" v-model="valid" @submit.prevent="submitForm">
          <v-text-field v-model="username" label="Username" :rules="[rules.required]" required></v-text-field>
          <v-text-field v-model="password" label="Password" type="password" :rules="[rules.required]" required></v-text-field>
          <v-btn type="submit" color="primary">Login</v-btn>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="$router.push('/register')">Register</v-btn>
      </v-card-actions>
    </v-card>

    <v-snackbar v-model="snackbar" :timeout="3000" color="error">
      <span>Login failed. Please check your credentials.</span>
    </v-snackbar>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthService from '@/services/service.auth'

const router = useRouter()
const username = ref('')
const password = ref('')
const form = ref()
const rules = {
  required: (value: string) => !!value || 'Required.'
}
const valid = ref(false)
const snackbar = ref(false)

const submitForm = async () => {
  if (form.value.validate()) {
    try {
      AuthService.login(username.value, password.value)
        .then((response) => {
          console.log('Login successful:', response)
          // Store the token in localStorage or Vuex store
          localStorage.setItem('token', response.data.access_token)
          // Redirect to home page after successful login
          router.push('/')
        })
        .catch((error) => {
          console.error('Login failed:', error)
          snackbar.value = true
        })
    } catch (error) {
      console.error('Login failed:', error)
    }
  }
}
</script>

<style scoped>
.login-container {
  justify-content: center;
  align-items: center;
  padding: 5vw 30vh;
  background-color: #f5f5f5;
}
</style>
