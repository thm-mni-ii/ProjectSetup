<template>
  <v-container class="create-post-view">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="pa-6">
          <v-card-title class="text-h5 mb-4">
            <v-icon class="mr-2">mdi-plus</v-icon>
            Neuen Blog-Post erstellen
          </v-card-title>

          <v-form @submit.prevent="createPost">
            <v-text-field v-model="title" label="Titel" prepend-inner-icon="mdi-format-title" variant="outlined" :rules="[rules.required]" :error-messages="titleErrors" class="mb-4" required />

            <v-textarea v-model="content" label="Inhalt" prepend-inner-icon="mdi-text" variant="outlined" :rules="[rules.required, rules.minLength]" :error-messages="contentErrors" rows="8" auto-grow class="mb-4" required />

            <v-alert v-if="error" type="error" class="mb-4" closable @click:close="error = ''">
              {{ error }}
            </v-alert>

            <v-alert v-if="success" type="success" class="mb-4" closable @click:close="success = ''">
              {{ success }}
            </v-alert>

            <div class="d-flex justify-space-between">
              <v-btn prepend-icon="mdi-arrow-left" variant="outlined" @click="$router.back()"> Zurück </v-btn>

              <v-btn type="submit" color="primary" prepend-icon="mdi-send" :loading="loading" :disabled="!isFormValid"> Post erstellen </v-btn>
            </div>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import BlogService from '@/services/service.blog'

const router = useRouter()

const title = ref('')
const content = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const titleErrors = ref<string[]>([])
const contentErrors = ref<string[]>([])

const rules = {
  required: (value: string) => !!value || 'Dieses Feld ist erforderlich',
  minLength: (value: string) => value.length >= 10 || 'Mindestens 10 Zeichen erforderlich'
}

const isFormValid = computed(() => {
  return title.value.trim() !== '' && content.value.trim() !== '' && content.value.length >= 10
})

const validateForm = () => {
  titleErrors.value = []
  contentErrors.value = []

  if (!title.value.trim()) {
    titleErrors.value.push('Titel ist erforderlich')
  }

  if (!content.value.trim()) {
    contentErrors.value.push('Inhalt ist erforderlich')
  } else if (content.value.length < 10) {
    contentErrors.value.push('Inhalt muss mindestens 10 Zeichen lang sein')
  }

  return titleErrors.value.length === 0 && contentErrors.value.length === 0
}

const createPost = async () => {
  if (!validateForm()) {
    return
  }

  loading.value = true
  error.value = ''
  success.value = ''

  try {
    await BlogService.createPost({
      title: title.value.trim(),
      content: content.value.trim()
    })

    success.value = 'Post wurde erfolgreich erstellt!'

    // Nach 2 Sekunden zu Posts weiterleiten
    setTimeout(() => {
      router.push('/posts')
    }, 2000)
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Fehler beim Erstellen des Posts'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.create-post-view {
  padding-top: 2rem;
}
</style>
