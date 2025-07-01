<template>
  <v-container class="statistics-view">
    <v-row justify="center">
      <v-col cols="12" lg="10">
        <v-card class="mb-6">
          <v-card-title class="text-h4 pa-6">
            <v-icon class="mr-3">mdi-chart-bar</v-icon>
            Nutzerstatistiken
          </v-card-title>

          <v-card-text class="px-6 pb-6">
            <div class="mb-8">
              <h3 class="text-h6 mb-4">{{ monthlyStats.title }}</h3>
              <v-card variant="outlined" class="pa-4">
                <div v-if="loading" class="text-center py-4">
                  <v-progress-circular indeterminate color="primary" />
                  <div class="mt-2">Lade Statistiken...</div>
                </div>

                <div v-else-if="monthlyStats.data.length > 0">
                  <v-row>
                    <v-col v-for="stat in monthlyStats.data" :key="stat.month" cols="12" sm="6" md="4" lg="3">
                      <v-card variant="tonal" color="primary" class="text-center pa-4">
                        <div class="text-h4 font-weight-bold text-primary">
                          {{ stat.user_count }}
                        </div>
                        <div class="text-body-2 text-medium-emphasis">
                          {{ formatMonth(stat.month) }}
                        </div>
                      </v-card>
                    </v-col>
                  </v-row>
                </div>

                <div v-else class="text-center py-4 text-medium-emphasis">Keine Daten verfügbar</div>
              </v-card>
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
import BlogService from '@/services/service.blog'

interface UserStatistic {
  month: string
  user_count: number
}

interface StatisticsResponse<T> {
  title: string
  data: T[]
}

const monthlyStats = ref<StatisticsResponse<UserStatistic>>({
  title: 'Lädt...',
  data: []
})

const loading = ref(false)

const formatMonth = (monthStr: string) => {
  if (!monthStr) return 'Unbekannt'
  const [year, month] = monthStr.split('-')
  const monthNames = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
  return `${monthNames[parseInt(month) - 1]} ${year}`
}

const loadMonthlyStats = async () => {
  loading.value = true
  try {
    const response = await BlogService.getUsersByMonth()
    monthlyStats.value = response.data
  } catch (error) {
    console.error('Fehler beim Laden der monatlichen Statistiken:', error)
    monthlyStats.value = {
      title: 'Fehler beim Laden',
      data: []
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadMonthlyStats()
})
</script>

<style scoped>
.statistics-view {
  padding-top: 2rem;
}
</style>
