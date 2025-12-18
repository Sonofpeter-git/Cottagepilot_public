<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from './components/layout/Navbar.vue'
import Footer from './components/layout/Footer.vue'
</script>

<template>
  <div id="app" class="min-h-screen min-w-screen text-secondary flex flex-col">
    <Navbar />
    <main class="flex-1">
      <RouterView />
    </main>
    <Footer />
  </div>
</template>

<style scoped>
#app {
  background: var(--extra-neutral-color);
  min-height: 100vh;
}
</style>