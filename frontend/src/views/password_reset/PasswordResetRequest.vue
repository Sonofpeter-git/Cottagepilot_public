<template>
  <div class="max-w-md mx-auto p-4">
    <h2 class="text-xl font-bold mb-4">Reset Your Password</h2>
    <form @submit.prevent="submit">
      <input
        v-model="email"
        type="email"
        placeholder="Enter your email"
        class="w-full p-2 border mb-4"
        required
      />
      <button class="bg-blue-600 text-white px-4 py-2 rounded">Send Reset Link</button>
    </form>
    <p v-if="message" class="mt-4 text-green-600">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../../services/api'
import { accountService } from '../../services/api'

const email = ref<string>('')
const message = ref<string>('')

const submit = async () => {
  try {
    const csrf = await accountService.get_csrf()
    localStorage.setItem('csrf', csrf)

    await api.post('/password-reset/', { email: email.value })
    message.value = 'If that email exists, a reset link was sent.'
  } catch (error) {
    message.value = 'An error occurred. Please try again later.'
  }
}
</script>
