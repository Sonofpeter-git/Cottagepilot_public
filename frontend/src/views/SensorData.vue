<script setup lang="ts">
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useSensorStore } from '../stores/sensors'
import { useAccountStore } from '../stores/account'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { format } from 'date-fns'

import type { WSMessage} from '../types/websocket';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const route = useRoute()
const sensorStore = useSensorStore()
const accountStore = useAccountStore()
const selectedSensorId = ref(route.params.id as string || '')
const timeRange = ref('24h')

const timeRangeOptions = [
  { value: '1h', label: 'Last Hour' },
  { value: '24h', label: 'Last 24 Hours' },
  { value: '7d', label: 'Last 7 Days' },
  { value: '30d', label: 'Last 30 Days' }
]

const selectedSensor = computed(() => 
  sensorStore.sensors.find((s: any) => s.id === selectedSensorId.value)
)

  const chartData = computed(() => {
  if (!sensorStore.sensorData.length) return null

  const data = sensorStore.sensorData.slice().reverse()
  
  return {
    labels: data.map((d: any) => format(new Date(d.timestamp), 'MMM dd, HH:mm')),
    datasets: [
      {
        label: selectedSensor.value ? `${selectedSensor.value.name} (${selectedSensor.value.unit})` : 'Sensor Data',
        data: data.map((d: any) => d.value),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: 'rgb(59, 130, 246)',
        pointBorderColor: 'white',
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
      }
    ]
  }
})

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: 'rgba(0, 0, 0, 0.8)'
      }
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: 'rgba(0, 0, 0, 0.8)',
      bodyColor: 'white',
      borderColor: 'rgba(255, 255, 255, 0.2)',
      borderWidth: 1,
    }
  },
  scales: {
    x: {
      ticks: {
        color: 'rgba(0, 0, 0, 0.8)'
      },
      grid: {
        color: 'rgba(255, 255, 255, 0.1)'
      }
    },
    y: {
      ticks: {
        color: 'rgba(0, 0, 0, 0.8)'
      },
      grid: {
        color: 'rgba(255, 255, 255, 0.1)'
      }
    }
  }
}))



// 1. Separate reactive states for different data streams
const isConnected = ref(false);

let socket: WebSocket | null = null;

const handleMessage = (event: MessageEvent) => {
    const data = JSON.parse(event.data) as WSMessage;

    // 2. The Router: TypeScript now provides autocomplete for 'payload' 
    // based on which 'case' you are in!
    switch (data.type) {
        case 'sensor_update':
          console.log("Received sensor update via WebSocket:", data.payload);
          console.log("Selected Sensor ID:", selectedSensorId.value);
          if (data.payload.sensor_id === selectedSensorId.value) {
            sensorStore.sensorData.unshift(data.payload);
          }
          break;
            
        case 'task_update':
            break;

        case 'note_update':
            break;

        default:
            console.warn('Unknown message type received');
    }
};

const connect = () => {
    socket = new WebSocket(`wss://cloud.cottagepilot.fi/ws/unified/${accountStore.account?.access_to_cottage}/`);
    socket.onopen = () => isConnected.value = true;
    console.log('WebSocket connected🚀 ' + accountStore.account?.access_to_cottage);
    socket.onmessage = handleMessage;
    socket.onclose = () => {
        isConnected.value = false;
        setTimeout(connect, 3000); // Reconnect logic
    };
};



const stats = computed(() => {
  if (!sensorStore.sensorData.length) return null

  const values = sensorStore.sensorData.map((d: any) => d.value)
  const min = Math.min(...values)
  const max = Math.max(...values)
  const avg = values.reduce((a: number, b: number) => a + b, 0) / values.length

  return { min, max, avg: Math.round(avg * 100) / 100 }
})

const fetchData = async () => {
  if (selectedSensorId.value) {
    await sensorStore.fetchSensorData(selectedSensorId.value, timeRange.value)
  }
}

watch([selectedSensorId, timeRange], fetchData)

onMounted(async () => {
  await accountStore.fetchAccount()
  await sensorStore.loadSensorsFromLocalStorage()
  await sensorStore.loadSensorDataFromLocalStorage()
  sensorStore.fetchSensors()
  if (selectedSensorId.value) {
    fetchData()
  }
  connect()
})


onUnmounted(() => socket?.close());

</script>

<template>
  <div class="min-h-screen py-8 px-4 sm:px-6 lg:px-8 text-secondary">
    <div class="mx-auto max-w-7xl">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-secondary mb-4">Sensor Data Visualization</h1>
        <p class="text-secondary/80">View and analyze real-time data from your sensors.</p>
      </div>

      <!-- Controls -->
      <div class="glass-effect rounded-lg p-6 mb-8">
        <div class="flex flex-col sm:flex-row gap-4">
          <div class="flex-1">
            <label class="block text-sm font-medium text-secondary mb-2">Select Sensor</label>
            <select
              v-model="selectedSensorId"
              class="w-full px-4 py-2 rounded-lg border border-white/20 bg-select_bg text-secondary focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option class="text-secondary" value="">Choose a sensor...</option>
              <option
                v-for="sensor in sensorStore.sensors"
                :key="sensor.id"
                :value="sensor.id"
                @click=""
                class="text-secondary"
              >
                {{ sensor.name }} - {{ sensor.location }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-secondary mb-2">Time Range</label>
            <select
              v-model="timeRange"
              :disabled="!selectedSensorId"
              class="px-4 py-2 rounded-lg border border-white/20 bg-select_bg text-secondary focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50"
            >
              <option
                v-for="option in timeRangeOptions"
                :key="option.value"
                :value="option.value"
                class="text-secondary"
              >
                {{ option.label }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Content -->
      <div v-if="!selectedSensorId" class="text-center py-12">
        <div class="text-6xl mb-4">📊</div>
        <h2 class="text-2xl font-semibold text-secondary mb-2">Select a Sensor</h2>
        <p class="text-secondary/80">Choose a sensor from the dropdown above to view its data.</p>
      </div>

      <div v-else-if="sensorStore.loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto"></div>
        <p class="text-secondary/80 mt-4">Loading sensor data...</p>
      </div>

      <div v-else-if="!sensorStore.sensorData.length" class="text-center py-12">
        <div class="text-6xl mb-4">📈</div>
        <h2 class="text-2xl font-semibold text-secondary mb-2">No Data Available</h2>
        <p class="text-secondary/80">This sensor doesn't have any data for the selected time range.</p>
      </div>

      <div v-else class="space-y-8">
        <!-- Stats Cards -->
        <div v-if="stats" class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="glass-effect rounded-lg p-6 text-center">
            <div class="text-2xl font-bold text-secondary mb-2">{{ stats.min }}</div>
            <div class="text-secondary/80">Minimum</div>
            <div class="text-sm text-secondary/60">{{ selectedSensor?.unit }}</div>
          </div>
          <div class="glass-effect rounded-lg p-6 text-center">
            <div class="text-2xl font-bold text-secondary mb-2">{{ stats.avg }}</div>
            <div class="text-secondary/80">Average</div>
            <div class="text-sm text-secondary/60">{{ selectedSensor?.unit }}</div>
          </div>
          <div class="glass-effect rounded-lg p-6 text-center">
            <div class="text-2xl font-bold text-secondary mb-2">{{ stats.max }}</div>
            <div class="text-secondary/80">Maximum</div>
            <div class="text-sm text-secondary/60">{{ selectedSensor?.unit }}</div>
          </div>
        </div>

        <!-- Chart -->
        <div class="glass-effect rounded-lg p-6">
          <h3 class="text-xl font-semibold text-secondary mb-6">
            {{ selectedSensor?.name }} - {{ timeRangeOptions.find(o => o.value === timeRange)?.label }}
          </h3>
          <div class="chart-container">
            <Line
              v-if="chartData"
              :data="chartData"
              :options="chartOptions"
            />
          </div>
        </div>

        <!-- Recent Data Table -->
        <div class="glass-effect rounded-lg p-6">
          <h3 class="text-xl font-semibold text-secondary mb-6">Recent Readings</h3>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-white/20">
                  <th class="text-left py-3 px-4 text-secondary font-medium">Timestamp</th>
                  <th class="text-left py-3 px-4 text-secondary font-medium">Value</th>
                  <th class="text-left py-3 px-4 text-secondary font-medium">Unit</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="data in sensorStore.sensorData.slice(0, 10)"
                  :key="data.id"
                  class="border-b border-white/10"
                >
                  <td class="py-3 px-4 text-secondary/80">
                    {{ format(new Date(data.timestamp), 'MMM dd, yyyy HH:mm:ss') }}
                  </td>
                  <td class="py-3 px-4 text-secondary font-medium">{{ data.value }}</td>
                  <td class="py-3 px-4 text-secondary/80">{{ selectedSensor?.unit }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>