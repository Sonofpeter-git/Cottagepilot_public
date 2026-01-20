<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { sensorService } from '../../services/api'
import SensorModal from './SensorModal.vue'
import type { Sensor } from '../../types'
interface Emits {
  (e: 'close'): void
  (e: 'saved'): void
}

const emit = defineEmits<Emits>()
const sensorId = ref('')
const loading = ref(false)
const error = ref<string | null>(null)
const showModal = ref(false)
const editingSensor = ref<Sensor | null>(null)

const handleSubmit = async () => {
  error.value = null
  loading.value = true
  try {
    editingSensor.value = await sensorService.postClaimSensor(sensorId.value)
    showModal.value = true;
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to claim sensor'
  } finally {
    loading.value = false
  }
}

const closeModal = () => {
  showModal.value = false
  editingSensor.value = null
  emit('close')
}

const onSaved = () => {
  closeModal()
  sensorId.value = ''
  emit('saved')
}

onMounted(async () => {
})
</script>

<template>
  <div class="max-w-md mx-auto p-4 bg-gray-800 rounded-lg text-white">
    <h2 class="text-xl font-semibold mb-4">Claim Sensor</h2>
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label for="sensorId" class="block mb-1">Sensor ID</label>
        <input
          id="sensorId"
          v-model="sensorId"
          type="text"
          required
          class="w-full px-3 py-2 rounded bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-secondary-500"
          placeholder="Enter sensor ID"
        />
      </div>
      <div v-if="error" class="text-red-500">{{ error }}</div>
      <button
        type="submit"
        :disabled="loading"
        class="w-full py-2 bg-secondary-600 rounded hover:bg-secondary-700 transition-colors disabled:opacity-50"
      >
        {{ loading ? 'Claiming...' : 'Claim Sensor' }}
      </button>
    </form>

    <SensorModal
      v-if="showModal"
      :sensor="editingSensor"
      @close="closeModal"
      @saved="onSaved"
    />
  </div>
</template>
