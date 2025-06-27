<template>
  <v-app-bar :elevation="1">
    <v-app-bar-title>
      <router-link to="/">123</router-link>
    </v-app-bar-title>

    <template #append>
      <v-btn to="/login" active-class="active" prepend-icon="mdi-login" color="primary" variant="text">
        <span> Login </span>
        <v-tooltip activator="parent" location="bottom"> Login </v-tooltip>
      </v-btn>
    </template>
  </v-app-bar>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<style scoped lang="scss">
.icon {
  height: 35px;
  width: auto;
  margin-right: 20px;
}
</style>
