<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="text-center">
        <h2 class="text-3xl font-bold text-gray-900 mb-2">
          Choose Your Cottage
        </h2>
        <p class="text-gray-600 mb-8">
          Select which cottage you'd like to access
        </p>
      </div>

      <div class="bg-popUpBg shadow-lg rounded-lg p-6">
        <div v-if="loading" class="text-center py-8">
          <svg class="animate-spin h-8 w-8 text-blue-600 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p class="text-gray-500">Loading your cottages...</p>
        </div>

        <div v-else-if="error" class="text-center py-8">
          <div class="text-red-600 mb-4">
            <svg class="h-12 w-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <p class="text-red-600 mb-4">{{ error }}</p>
          <button 
            @click="loadCottages" 
            class="text-blue-600 hover:text-blue-800 font-medium"
          >
            Try Again
          </button>
        </div>

        <div v-else-if="cottages.length === 0" class="text-center py-8">
          <div class="text-gray-400 mb-4">
            <svg class="h-12 w-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
            </svg>
          </div>
          <p class="text-gray-500 mb-4">You don't have access to any cottages yet.</p>
          <router-link 
            to="/add-or-create-cottage/" 
            class="text-blue-600 hover:text-blue-800 font-medium"
          >
            Create a new cottage
          </router-link>
        </div>

        <div v-else>
          <form @submit.prevent="handleCottageSelection" class="space-y-6">
            <div>
              <label for="cottage-select" class="block text-sm font-medium text-gray-700 mb-2">
                Select Cottage
              </label>
              <select
                id="cottage-select"
                v-model="selectedCottageId"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-popUpBg"
              >
                <option value="" disabled>Select a cottage...</option>
                <option 
                  v-for="cottage in cottages" 
                  :key="cottage.id" 
                  :value="cottage.id"
                >
                  {{ cottage.name }} - {{ cottage.address }}
                </option>
              </select>
            </div>

            <button
              type="submit"
              :disabled="!selectedCottageId || isSelecting"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="isSelecting" class="flex items-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Accessing...
              </span>
              <span v-else>Access Cottage</span>
            </button>
          </form>

          <!-- Cottage Preview -->
          <div v-if="selectedCottage" class="mt-6 p-4 bg-gray-50 rounded-md">
            <h3 class="text-sm font-medium text-gray-900 mb-2">Selected Cottage Details</h3>
            <div class="space-y-1 text-sm text-gray-600">
              <p><strong>Name:</strong> {{ selectedCottage.name }}</p>
              <p><strong>Address:</strong> {{ selectedCottage.address }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Create New Cottage Option -->
      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600">
          Don't see your cottage?
          <router-link to="/add-or-create-cottage/" class="text-blue-600 hover:text-blue-800 font-medium">
            Create a new one
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../services/api'
import { Cottage } from '../types'


const router = useRouter()

const cottages = ref<Cottage[]>([])
const selectedCottageId = ref('')
const loading = ref(false)
const error = ref('')
const isSelecting = ref(false)

const selectedCottage = computed(() => {
  return cottages.value.find(c => c.id === selectedCottageId.value) || null
})

const loadCottages = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/cottage/user-cottages/')
    cottages.value = response.data.results || []
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Failed to load cottages'
    console.error('Error loading cottages:', err)
  } finally {
    loading.value = false
  }
}

const handleCottageSelection = async () => {
  if (!selectedCottageId.value) return

  isSelecting.value = true

  try {
    // Set the selected cottage in the store
    const cottage = selectedCottage.value
    if (cottage) {
      try {
        const response = await api.post('/cottage/select-cottage/', {'id': selectedCottageId.value})
        if (response.status == 200){
          // Redirect to dashboard or home
          localStorage.setItem('cottageInstanceActive', 'true')
          router.push('/dashboard')
        } 
        
      } catch (err: any) {
        error.value = err.response?.data?.error || 'Failed to load cottages'
        console.error('Error loading cottages:', err)
      } finally {
        loading.value = false
      }
          
      
    }
  } catch (err) {
    console.error('Error selecting cottage:', err)
    error.value = 'Failed to access cottage'
  } finally {
    isSelecting.value = false
  }
}

// Load cottages on component mount
onMounted(() => {
  loadCottages()
})
</script>