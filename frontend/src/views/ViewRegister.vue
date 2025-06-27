<template>
  <div class="login-container">
    <v-card class="login-card">
      <v-card-title class="text-h5">Register</v-card-title>
      <v-card-text>
        <v-form ref="form" v-model="valid" @submit.prevent="submitForm">
          <v-text-field v-model="username" label="Username" :rules="[rules.required]" required></v-text-field>
          <v-text-field v-model="password" label="Password" type="password" :rules="[rules.required]" required></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn type="submit" color="primary" @click="submitForm">Register</v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import AuthService from '@/services/service.auth'

const router = useRouter()
const valid = ref(false)
const username = ref('')
const password = ref('')
const form = ref()
const rules = {
  required: (value: string) => !!value || 'Required.'
}

const submitForm = async () => {
  if (form.value.validate()) {
    try {
      AuthService.register(username.value, password.value)
        .then((response) => {
          console.log('Registration successful:', response)
          // Redirect to login page after successful registration
          router.push('/login')
        })
        .catch((error) => {
          console.error('Registration failed:', error)
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
