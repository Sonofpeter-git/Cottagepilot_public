<template>
  <div class="max-w-md mx-auto p-4">
    <h2 class="text-xl font-bold mb-4">Set New Password</h2>
    <form @submit.prevent="submit">
      <input
        v-model="password"
        type="password"
        placeholder="New password"
        class="w-full p-2 border mb-4"
        required
      />
      <p v-if="errors.new_password" class="text-red-600 text-sm mb-1" v-for="(err, idx) in errors.new_password" :key="idx">{{ err }}</p>
      <input
        v-model="confirmPassword"
        type="password"
        placeholder="Confirm new password"
        class="w-full p-2 border mb-4"
        required
      />
      <button class="bg-blue-600 text-white px-4 py-2 rounded">Reset Password</button>
    </form>
    <p v-if="message" class="mt-4" :class="status">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../../services/api' 
import { accountService } from '../../services/api'
const route = useRoute()

const password = ref<string>('')
const confirmPassword = ref<string>('')

const message = ref<string>('')
const status = ref<string>('text-green-600')

const uid = route.params.uid as string
const token = route.params.token as string
const errors = ref<{ [key: string]: string[] }>({})


onMounted(async () => {
  try {
    const csrf = await accountService.get_csrf()
    localStorage.setItem('csrf', csrf)
    await api.get(`/password-reset/${uid}/${token}/`)
  } catch {
    message.value = 'Invalid or expired reset link.'
    status.value = 'text-red-600'
  }
})


const submit = async () => {
  if (password.value !== confirmPassword.value) {
    message.value = 'Passwords do not match.'
    status.value = 'text-red-600'
    return
  }

  try {
    message.value = ''
    const response = await api.post('/password-reset/complete/', {
      uid,
      token,
      new_password: password.value,
    })
    
    if (response.data.status == "true"){
      message.value = 'Password successfully changed. Please signin'
      status.value = 'text-green-600'
      password.value = ''
      confirmPassword.value = ''
      errors.value = {}
    } else {
      errors.value = response.data.errors ?? {}
    }
    



  } catch (err) {
    message.value = 'Failed to reset password.'
    status.value = 'text-red-600'
  }
}
</script>
