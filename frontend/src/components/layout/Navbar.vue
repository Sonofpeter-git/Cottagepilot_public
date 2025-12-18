<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useAccountStore } from '../../stores/account';

const accountStore = useAccountStore()
const router = useRouter()
const route = useRoute()
// Define the navigation links based on the router configuration
const allNavLinks = [
  { name: 'Home', path: '/' },
  { name: 'Blogs', path: '/blogs/' },
  { name: 'Dashboard', path: '/dashboard/' },
  { name: 'About', path: '/about/' },
  { name: 'Pricing', path: '/pricing/' },
  //{ name: 'Testimonials', path: '/testimonials' },
  { name: 'Story', path: '/story/' },
  { name: 'Sensor dashboard', path: '/sensor-dashboard/' },
  { name: 'Tasks', path: '/task-list/' },
  {name: 'Calendar', path: '/calendar/'},
  { name: 'Notes', path: '/notes/'},
  { name: 'Contact', path: '/contact/' },
  { name: 'Login', path: '/login/' },
  { name: 'Account', path: '/account/'},
]

// Filter nav links based on login status
const navLinks = computed(() => {
  if (accountStore.isUserAuthenticated) {
    // Remove About, Testimonials, Story, Home when logged in
    return allNavLinks.filter(link => !['Home', 'About', /*'Testimonials',*/ 'Story', 'Pricing', 'Login'].includes(link.name))
  } else {
    return allNavLinks.filter(link => !['Dashboard','Account', 'Sensor dashboard', 'Tasks', 'Notes', 'Calendar'].includes(link.name))
  }
})

const isActive = (path: string) => {
  return route.path === path
}

const navigateTo = (path: string) => {
  router.push(path)
}

// Reactive property to track if window width is less than 700px
const isMobile = ref(window.innerWidth < 700)
const dropdownOpen = ref(false)

const handleResize = () => {
  isMobile.value = window.innerWidth < 700
  if (!isMobile.value) {
    dropdownOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}
</script>
<template>
  <nav class="nav text-white pb-4">
    <div class="w-full mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <div class="flex-shrink-0 font-bold text-xl cursor-pointer text-black" @click="navigateTo('/')">
          <img src="/cottagePilotLogo.png" alt="CottagePilot" class="h-10 w-auto block" />
        </div>
        <!-- Inline nav links for desktop -->
        <div v-if="!isMobile" class="hidden gradiant md:flex md:justify-center md:rounded-full md:w-auto md:m-auto md:mt-3 space-x-4">
          <button
            v-for="link in navLinks"
            :key="link.name"
            @click="navigateTo(link.path)"
            :class="[
              'p-4 px-7 rounded text-sm font-medium focus:outline-none',
              isActive(link.path) ? ' bg-black/30 rounded-full px-7' : 'hover:font-bold'
            ]"
          >
            {{ link.name }}
          </button>
        </div>
        <!-- Dropdown menu for mobile -->
        <div v-else class="relative">
          <button @click="toggleDropdown" class="px-3 py-2 rounded-md text-sm font-medium focus:outline-none bg-white bg-opacity-20 hover:bg-white hover:bg-opacity-30">
            Menu
          </button>
          <div v-if="dropdownOpen" class="absolute right-0 mt-2 w-48 bg-white bg-opacity-90 text-black rounded-md shadow-lg z-10">
            <button
              v-for="link in navLinks"
              :key="link.name"
              @click="navigateTo(link.path); dropdownOpen = false"
              class="block w-full text-left px-4 py-2 text-sm hover:bg-blue-500 hover:text-white"
            >
              {{ link.name }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.gradiant {
  user-select: none;
  background: linear-gradient(135deg, var(--primary-color) 20%,  var(--secondary-color) 100%);
}
</style>
