<template>
  <div class="min-h-screen bg-extraNeutral py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md mx-auto">
      <div class="text-center">
        <h2 class="text-3xl font-bold text-gray-900 mb-2">
          Invite Members to Cottage
        </h2>
        <p class="text-gray-600 mb-8">
          Send invitations to join your cottage via email
        </p>
      </div>

      <div class="shadow-lg bg-popUpBg rounded-lg p-6">
        <form @submit.prevent="handleInvite" class="space-y-6">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email Address
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="Enter email address"
            />
          </div>
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Sending...
            </span>
            <span v-else>Send Invitation</span>
          </button>
        </form>

        <!-- Success/Error Messages -->
        <div v-if="notification" :class="notificationClass" class="mt-4 p-4 rounded-md">
          <div class="flex">
            <div class="ml-3">
              <p class="text-sm font-medium">{{ notification.message }}</p>
            </div>
          </div>
        </div>

        <!-- Recent Invitations -->
        <div v-if="recentInvitations.length > 0" class="mt-8">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Recent Invitations</h3>
          <div class="space-y-3">
            <div
              v-for="invitation in recentInvitations"
              :key="invitation.id"
              class="flex items-center justify-between p-3 bg-gray-50 rounded-md"
            >
              <div>
                <p class="text-sm font-medium text-gray-900">{{ invitation.email }}</p>
                <p class="text-xs text-gray-500">{{ formatDate(invitation.sent_at) }}</p>
              </div>
              <span :class="getStatusClass(invitation.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                {{ invitation.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { api } from '../services/api'

interface Invitation {
  id: string
  email: string
  status: 'pending' | 'accepted' | 'expired'
  sent_at: string
}

const email = ref('')
const isLoading = ref(false)
const notification = ref<{ type: 'success' | 'error'; message: string } | null>(null)
const recentInvitations = ref<Invitation[]>([])

const notificationClass = computed(() => {
  if (!notification.value) return ''
  return notification.value.type === 'success'
    ? 'bg-green-50 border border-green-200'
    : 'bg-red-50 border border-red-200'
})

const handleInvite = async () => {
  if (!email.value.trim()) {
    showNotification('error', 'Please enter an email address')
    return
  }

  isLoading.value = true
  notification.value = null

  try {
    const response = await api.post('cottage/invitations/send/', {
      email: email.value.trim(),
    })


    if (response.data.status == 'success') {
      showNotification('success', response.data.message)
      email.value = ''
      
      // Add to recent invitations
      recentInvitations.value.unshift({
        id: response.data.invitation_id,
        email: response.data.email,
        status: 'pending',
        sent_at: new Date().toISOString()
      })
      
      // Keep only last 5
      recentInvitations.value = recentInvitations.value.slice(0, 5)
    } else if (response.status == 200){
      showNotification("error" , response.data.message)
    }
  } catch (error: any) {
    const errorMessage = error.response?.data?.error || 'Failed to send invitation'
    showNotification('error', errorMessage)
  } finally {
    isLoading.value = false
  }
}

const showNotification = (type: 'success' | 'error', message: string) => {
  notification.value = { type, message }
  setTimeout(() => {
    notification.value = null
  }, 5000)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusClass = (status: string) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-800',
    accepted: 'bg-green-100 text-green-800',
    expired: 'bg-red-100 text-red-800'
  }
  return classes[status as keyof typeof classes] || 'bg-gray-100 text-gray-800'
}

</script>
