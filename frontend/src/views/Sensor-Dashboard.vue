<script setup lang="ts">
import { onMounted, computed, ComputedRef } from 'vue'
import { useSensorStore } from '../stores/sensors'
import { useAccountStore } from '../stores/account'
import { RouterLink } from 'vue-router'
import { 
  ChartBarIcon, 
  CpuChipIcon, 
  ExclamationTriangleIcon,
  CheckCircleIcon 
} from '@heroicons/vue/24/outline'
import type { Stats } from '../types'

const sensorStore = useSensorStore()
const accountStore = useAccountStore()

const stats: ComputedRef<Stats> = computed(() => ({
  total: sensorStore.sensors.length,
  active: sensorStore.activeSensors.length,
  inactive: sensorStore.inactiveSensors.length,
  error: sensorStore.sensors.filter((s: { status: string }) => s.status === 'error').length
}));

const recentSensors = computed(() => 
  sensorStore.sensors
    .slice()
    .sort((a: { updated_at: string | number | Date }, b: { updated_at: string | number | Date }) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
    .slice(0, 5)
)

const getSensorIcon = (type: string) => {
  const icons: Record<string, string> = {
    temperature: '🌡️',
    humidity: '💧',
    pressure: '📊',
    light: '💡',
    motion: '🏃',
    air_quality: '🌬️'
  }
  return icons[type] || '📡'
}

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    active: 'text-green-400',
    inactive: 'text-gray-400',
    error: 'text-red-400'
  }
  return colors[status] || 'text-gray-400'
}

onMounted(() => {
  sensorStore.loadSensorsFromLocalStorage()
  sensorStore.loadSensorDataFromLocalStorage()
  sensorStore.fetchSensors()
  accountStore.fetchAccount()
})
</script>

<template>
  <div class="min-h-screen py-8 px-3 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-7xl">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-secondary mb-4">Sensor dashboard</h1>
        <p class="text-secondary">Monitor your IoT sensors and system performance at a glance.</p>
      </div>
      <div v-if="accountStore.account?.cottage_plan !== 'Basic'">
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div class="rounded rounded-md shadow p-6 bg-popUpBg">
            <div class="flex items-center">
              <div class="p-3 rounded shadow-full bg-primary-500/20">
                <CpuChipIcon class="w-6 h-6 text-secondary" />
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-secondary/80">Total Sensors</p>
                <p class="text-2xl font-semibold text-secondary">{{ stats.total }}</p>
              </div>
            </div>
          </div>

          <div class="rounded rounded-md shadow p-6 bg-popUpBg">
            <div class="flex items-center">
              <div class="p-3 rounded shadow-full bg-green-500/20">
                <CheckCircleIcon class="w-6 h-6 text-green-400" />
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-secondary/80">Active</p>
                <p class="text-2xl font-semibold text-secondary">{{ stats.active }}</p>
              </div>
            </div>
          </div>

          <div class="rounded rounded-md shadow p-6 bg-popUpBg">
            <div class="flex items-center">
              <div class="p-3 rounded shadow-full bg-gray-500/20">
                <CpuChipIcon class="w-6 h-6 text-gray-400" />
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-secondary/80">Inactive</p>
                <p class="text-2xl font-semibold text-secondary">{{ stats.inactive }}</p>
              </div>
            </div>
          </div>

          <div class="rounded rounded-md shadow p-6 bg-popUpBg">
            <div class="flex items-center">
              <div class="p-3 rounded shadow-full bg-red-500/20">
                <ExclamationTriangleIcon class="w-6 h-6 text-red-400" />
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-secondary/80">Errors</p>
                <p class="text-2xl font-semibold text-secondary">{{ stats.error }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Recent Sensors -->
          <div class="rounded rounded-md shadow p-6 bg-popUpBg">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-semibold text-secondary">Recent Sensors</h2>
              <RouterLink
                to="/manage-sensors"
                class="text-secondary hover:bg-blue-300 p-2 rounded text-sm font-medium"
              >
                View All
              </RouterLink>
            </div>

            <div v-if="sensorStore.loading" class="text-center py-8">
              <div class="animate-spin rounded shadow-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
              <p class="text-secondary mt-2">Loading...</p>
            </div>

            <div v-else-if="recentSensors.length === 0" class="text-center py-8">
              <CpuChipIcon class="w-12 h-12 text-secondary mx-auto mb-2" />
              <p class="text-secondary/60">No sensors found</p>
              <RouterLink
                to="/sensors"
                class="text-secondary-400 hover:text-secondary-300 text-sm font-medium mt-2 inline-block"
              >
                Add your first sensor
              </RouterLink>
            </div>

            <div v-else class="space-y-4">
              <div
                v-for="sensor in recentSensors"
                :key="sensor.id"
                class="flex items-center justify-between p-4 rounded shadow-lg bg-white/5 hover:bg-white/10 transition-colors"
              >
                <div class="flex items-center gap-3">
                  <span class="text-xl">{{ getSensorIcon(sensor.type) }}</span>
                  <div>
                    <h3 class="font-medium text-secondary">{{ sensor.name }}</h3>
                    <p class="text-sm text-secondary/60">{{ sensor.location }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <div :class="['text-sm font-medium', getStatusColor(sensor.status)]">
                    {{ sensor.status }}
                  </div>
                  <div v-if="sensor.last_reading" class="text-sm text-secondary/60">
                    {{ sensor.last_reading }} {{ sensor.unit }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="rounded rounded-md shadow p-6 bg-popUpBg">
            <h2 class="text-xl font-semibold text-secondary mb-6">Quick Actions</h2>
            <div class="space-y-4">
              <RouterLink
                to="/manage-sensors"
                class="block p-4 rounded shadow-lg bg-white/5 hover:bg-primary-500/30 transition-colors group"
              >
                <div class="flex items-center gap-3">
                  <CpuChipIcon class="w-6 h-6 text-secondary group-hover:text-secondary-300" />
                  <div>
                    <h3 class="font-medium text-secondary">Manage Sensors</h3>
                    <p class="text-sm text-secondary">Add, edit, or remove sensors</p>
                  </div>
                </div>
              </RouterLink>

              <RouterLink
                to="/sensor-data"
                class="block p-4 rounded shadow-lg bg-white/5 hover:bg-secondary-500/30 transition-colors group"
              >
                <div class="flex items-center gap-3">
                  <ChartBarIcon class="w-6 h-6 text-secondary group-hover:text-black-300" />
                  <div>
                    <h3 class="font-medium text-secondary">View Data</h3>
                    <p class="text-sm text-secondary">Analyze sensor data and trends</p>
                  </div>
                </div>
              </RouterLink>

              <div class="p-4 rounded shadow-lg bg-white/5">
                <div class="flex items-center gap-3">
                  <div class="w-6 h-6 rounded shadow-full bg-yellow-500/20 flex items-center justify-center">
                    <span class="text-secondary text-sm">⚡</span>
                  </div>
                  <div>
                    <h3 class="font-medium text-secondary">System Status</h3>
                    <div v-if="stats.inactive == 0">
                      <p class="text-sm text-green-500">All systems operational</p>
                    </div>
                    <div v-else>
                      <p class="text-sm text-red-300">Some sensors are inactive</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <div class="bg-popUpBg rounded-lg p-6">
          <p>Please upgrade your plan to access this feature. If you wish to upgrade your plan please contact us at cottagepilot@gmail.com</p>
        </div>
     </div>
    </div>
  </div>
</template>