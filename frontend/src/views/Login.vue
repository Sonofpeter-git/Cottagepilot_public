<script setup lang="ts">
import { ref } from 'vue'
import { useAccountStore } from '../stores/account';

const accountStore = useAccountStore()
const username = ref('')
const password = ref('')
const error = ref('')
const failedAttempts = ref(0)


const handleLogin = async () => {
  error.value = ''
  try {
    const status = await accountStore.login(username.value, password.value)
    if (status == true){
      failedAttempts.value = 0
    } else {
      failedAttempts.value++
      error.value = 'Invalid username or password'
    }
  } catch (err) {
    failedAttempts.value++
    error.value = 'Invalid username or password'
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center gradiant_1 justify-center text-white">
    <div class="max-w-md w-full gradiant_2 p-8 rounded-lg shadow-lg">
      <h2 class="text-2xl font-bold mb-6 text-center text-white">Login</h2>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="username" class="block mb-1">Username</label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            class="w-full px-3 py-2 rounded bg-extraNeutral border text-secondary border-gray-600 focus:outline-none focus:ring-2 focus:ring-secondary"
          />
        </div>
        <div>
          <label for="password" class="block mb-1">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="w-full px-3 py-2 rounded bg-extraNeutral text-secondary border border-gray-600 focus:outline-none focus:ring-2 focus:ring-secondary"
          />
        </div>
        <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
        <div v-if="failedAttempts >= 1" class="text-center">
          <router-link 
            to="/forgot-password" 
            class="text-white hover:text-indigo-300 text-sm underline"
          >
            Forgot your password?
          </router-link>
        </div>
        <button
          type="submit"
          class="w-full py-2 bg-indigo-600 rounded hover:bg-indigo-700 transition-colors"
        >
          Login
        </button>
      </form>
      
      <div class="mt-6 text-center">
        <p class="text-sm text-gray-300">
          Don't have an account?
          <router-link 
            to="/pricing" 
            class="text-indigo-400 hover:text-indigo-300 font-medium underline"
          >
            Sign up
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>
<style>
.gradiant_1{
  background: linear-gradient(135deg, var(--primary-color) 20%,  var(--secondary-color) 100%);
}
.gradiant_2{
  background: linear-gradient(135deg, var(--secondary-color) 20% ,var(--primary-color) 100%);
}
</style>
