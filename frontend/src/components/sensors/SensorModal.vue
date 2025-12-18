<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { useSensorStore } from '../../stores/sensors'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import type { Sensor } from '../../types'

interface Props {
  sensor?: Sensor | null
}

interface Emits {
  (e: 'close'): void
  (e: 'saved'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const sensorStore = useSensorStore()
const loading = ref(false)

const form = reactive({
  name: '',
  type: 'temperature' as Sensor['type'],
  location: '',
  description: '',
  status: 'active' as Sensor['status'],
  unit: ''
})

const sensorTypes = [
  { value: 'temperature', label: 'Temperature', unit: '°C' },
  { value: 'humidity', label: 'Humidity', unit: '%' },
  { value: 'pressure', label: 'Pressure', unit: 'hPa' },
  { value: 'light', label: 'Light', unit: 'lux' },
  { value: 'motion', label: 'Motion', unit: 'boolean' },
  { value: 'air_quality', label: 'Air Quality', unit: 'AQI' }
]

// Auto-set unit based on sensor type
watch(() => form.type, (newType) => {
  const sensorType = sensorTypes.find(t => t.value === newType)
  if (sensorType) {
    form.unit = sensorType.unit
  }
})

// Initialize form with sensor data if editing
watch(() => props.sensor, (sensor) => {
  if (sensor) {
    form.name = sensor.name
    form.type = sensor.type
    form.location = sensor.location
    form.description = sensor.description || ''
    form.status = sensor.status
    form.unit = sensor.unit
  } else {
    // Reset form for new sensor
    form.name = ''
    form.type = 'temperature'
    form.location = ''
    form.description = ''
    form.status = 'active'
    form.unit = '°C'
  }
}, { immediate: true })

const handleSubmit = async () => {
  loading.value = true
  try {
    if (props.sensor) {
      await sensorStore.updateSensor(props.sensor.id, form)
    } else {
      await sensorStore.createSensor(form)
    }
    emit('saved')
  } catch (error) {
    console.error('Failed to save sensor:', error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex min-h-screen items-center justify-center p-4">
      <div class="fixed inset-0 bg-black/50 backdrop-blur-sm" @click="emit('close')"></div>
      
      <div class="relative glass-effect rounded-lg p-6 w-full max-w-md">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold text-white">
            {{ sensor ? 'Edit Sensor' : 'Add New Sensor' }}
          </h2>
          <button
            @click="emit('close')"
            class="text-white/60 hover:text-white transition-colors"
          >
            <XMarkIcon class="w-6 h-6" />
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-white mb-2">Name</label>
            <input
              v-model="form.name"
              type="text"
              required
              class="w-full px-3 py-2 rounded-lg border border-white/20 bg-white/10 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-secondary-500"
              placeholder="Enter sensor name"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-white mb-2">Type</label>
            <select
              v-model="form.type"
              required
              class="w-full px-3 py-2 rounded-lg border border-white/20 bg-white/10 text-white focus:outline-none focus:ring-2 focus:ring-secondary-500"
            >
              <option v-for="type in sensorTypes" :key="type.value" :value="type.value" class="text-black">
                {{ type.label }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-white mb-2">Location</label>
            <input
              v-model="form.location"
              type="text"
              required
              class="w-full px-3 py-2 rounded-lg border border-white/20 bg-white/10 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-secondary-500"
              placeholder="Enter sensor location"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-white mb-2">Unit</label>
            <input
              v-model="form.unit"
              type="text"
              required
              class="w-full px-3 py-2 rounded-lg border border-white/20 bg-white/10 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-secondary-500"
              placeholder="Measurement unit"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-white mb-2">Status</label>
            <input
              v-model="form.status"
              required
              class="w-full px-3 py-2 rounded-lg border border-white/20 bg-white/10 text-white focus:outline-none focus:ring-2 focus:ring-secondary-500"
              disabled
            >
            </input>
          </div>

          <div>
            <label class="block text-sm font-medium text-white mb-2">Description</label>
            <textarea
              v-model="form.description"
              rows="3"
              class="w-full px-3 py-2 rounded-lg border border-white/20 bg-white/10 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-secondary-500"
              placeholder="Optional description"
            ></textarea>
          </div>

          <div class="flex gap-3 pt-4">
            <button
              type="button"
              @click="emit('close')"
              class="flex-1 px-4 py-2 border border-white/20 text-white rounded-lg hover:bg-white/10 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="flex-1 px-4 py-2 bg-secondary-600 text-white rounded-lg hover:bg-secondary-700 transition-colors disabled:opacity-50"
            >
              {{ loading ? 'Saving...' : (sensor ? 'Update' : 'Create') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>