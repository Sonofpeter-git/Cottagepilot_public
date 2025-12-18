<template>
  <div class="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-4xl font-bold text-center mb-10 text-gray-900">Pricing Plans</h1>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div v-for="plan in plans" :key="plan.id" class="bg-popUpBg rounded-lg shadow p-6 flex flex-col">
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">{{ plan.name }}</h2>
          <p class="text-3xl font-bold mb-6 text-gray-900">{{ plan.price }}</p>
          <ul class="mb-6 space-y-2 flex-grow">
            <li v-for="feature in plan.features" :key="feature" class="text-gray-700">• {{ feature }}</li>
          </ul>
          <button
            @click="openSignupModal()"
            class="mt-auto bg-primary hover:font-bold hover:shadow-md text-white font-semibold py-2 px-4 rounded"
          >
            Start
          </button>
        </div>
      </div>
    </div>
    <div class="bg-popUpBg rounded-lg shadow p-6 mt-6 w-2/3 justify-center m-auto text-center flex flex-col">
    <p class="font-semibold text-secondary">Cottagepilot Pricing Explanation</p>
    <p class="text-secondary">Cottagepilot offers flexible subscription plans designed to suit different cottage management needs. All pricing applies per cottage instance, meaning you pay for each cottage you manage. Users connected to your cottage can generate and manage content freely without additional costs.</p>
    </div>    
    <div v-if="modalVisible" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div class="bg-white rounded-lg p-8 w-full max-w-md">
        <h2 class="text-2xl font-bold mb-6 text-gray-900">Sign Up</h2>
        <form @submit.prevent="submitSignup">
          <div class="mb-4">
            <label for="username" class="block text-gray-700 font-semibold mb-1">Username</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p v-if="errors.username" class="text-red-600 text-sm mt-1" v-for="(err, idx) in errors.username" :key="idx">{{ err }}</p>
          </div>
          <div class="mb-4">
            <label for="email" class="block text-gray-700 font-semibold mb-1">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p v-if="errors.email" class="text-red-600 text-sm mt-1" v-for="(err, idx) in errors.email" :key="idx">{{ err }}</p>
          </div>
          <div class="mb-4">
            <label for="password1" class="block text-gray-700 font-semibold mb-1">Password</label>
            <input
              id="password1"
              v-model="form.password1"
              type="password"
              required
              class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <p v-if="errors.password1" class="text-red-600 text-sm mt-1" v-for="(err, idx) in errors.password1" :key="idx">{{ err }}</p>
          <div class="mb-4">
            <label for="password2" class="block text-gray-700 font-semibold mb-1">Confirm Password</label>
            <input
              id="password2"
              v-model="form.password2"
              type="password"
              required
              class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p v-if="errors.password2" class="text-red-600 text-sm mt-1" v-for="(err, idx) in errors.password2" :key="idx">{{ err }}</p>
          </div>
          <p class="font-semibold">By Signin Up you accept our <a href="/privacy-policy/" target="_blank" class="text-blue-500">Privacy Policy</a> and <a target="_blank" href="/terms-of-service/" class="text-blue-500">Terms of Service</a> </p>
          <div class="flex justify-end space-x-4">
            <button
              type="button"
              @click="closeSignupModal"
              class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 text-gray-800 font-semibold"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700 text-white font-semibold"
            >
              Sign Up
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
//import { useRouter } from 'vue-router'
//const router = useRouter() 
const plans = [
  {
    id: 1,
    name: 'Basic',
    price: '€14.99/mo',
    features: ['Users: 1 user', 'Sensors: No support', 'Simple task management'],
  },
  {
    id: 2,
    name: 'Standard',
    price: '€19.99/mo',
    features: ['Users: Up to 3 users', 'Sensors: Support for 2 sensor', 'Tasks: Task sharing and reminders'],
  },
  {
    id: 3,
    name: 'Premium',
    price: '€24.99/mo',
    features: ['Users: Unlimited users', 'Sensors: 10 sensors with alerts', 'Tasks: Task sharing and reminders'],
  },
]

const modalVisible = ref(false)
const form = ref({
  username: '',
  email: '',
  password1: '',
  password2: '',
})

const errors = ref<{ [key: string]: string[] }>({})

function openSignupModal() {
  modalVisible.value = true
  errors.value = {}
}

function closeSignupModal() {
  modalVisible.value = false
  form.value = {
    username: '',
    email: '',
    password1: '',
    password2: '',
  }
  errors.value = {}
}

/*import { useAccountStore } from '../stores/account'
import { accountService } from '../services/api'
import { api } from '../services/api'
import { signUpResponse } from '../types'*/


async function submitSignup() {
  if (form.value.password1 !== form.value.password2) {
    errors.value = { password2: ['Passwords do not match'] }
    return
  }
  alert("We have temporarily suspended automatic signups to ensure we provide the best possible service to our current clients. However, we would love to have you! Please contact us at cottagepilot@gmail.com to join our waiting list, and we will do our best to accommodate you as soon as possible.")
  /*
  try {
    const csrf = await accountService.get_csrf()
    localStorage.setItem('csrf', csrf)

    const response = await api.post<signUpResponse>('/signup/', {
      username: form.value.username,
      email: form.value.email,
      password1: form.value.password1,
      password2: form.value.password2,
    })

    if (response.data.token != "no" && response.data.redirect){
      const accountStore = useAccountStore()
      accountStore.updateAuthVariables(response.data.token, response.data.cottageInstanceActive)
      router.push(response.data.redirect)
      closeSignupModal()
    } else {
      errors.value = response.data.message ?? {}
      form.value.password1 = ""
      form.value.password2 = ""
    }
  } catch (error: any) {
      alert('Signup failed: ' + (error.message || 'Unknown error'))
  }*/
}
</script>