<template>
  <div class="p-6 max-w-5xl mx-auto">
    <h1 class="text-3xl font-bold mb-3 text-title_font text-secondary">Manage Sensors</h1>
    <p class="text-secondary mb-6">Type something smart here</p>
    <div v-if="accountStore.account?.cottage_plan !== 'Basic'">
      <div v-if="sensorStore.loading" class="text-center py-8">
        Loading sensors...
      </div>

      <div v-if="sensorStore.error" class="text-red-500 mb-4">
        {{ sensorStore.error }}
      </div>
      <div class="bg-popUpBg rounded-lg p-6">
        <table v-if="!sensorStore.loading && sensorStore.sensors.length && !showMobileVersio" class="w-full border-collapse text-secondary">
          <thead>
            <tr class="bg-firstRow text-secondary">
              <th class="border border-secondary px-4 py-2 text-left">Name</th>
              <th class="hidden md:table-cell border border-secondary px-4 py-2 text-left">Type</th>
              <th class="hidden md:table-cell border border-secondary px-4 py-2 text-left">Location</th>
              <th class="hidden md:table-cell border border-secondary px-4 py-2 text-left">Unit</th>
              <th class="border border-secondary px-4 py-2 text-left">Status</th>
              <th class="hidden md:table-cell border border-secondary px-4 py-2 text-left">Description</th>
              <th class="border border-secondary px-4 py-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="sensor in sensorStore.sensors.filter(s => s && s.id)" :key="sensor.id" class="hover:bg-hover">
              <td class="border border-secondary px-4 py-2">{{ sensor.name }}</td>
              <td class="hidden md:table-cell border border-secondary px-4 py-2">{{ sensor.type }}</td>
              <td class="hidden md:table-cell border border-secondary px-4 py-2">{{ sensor.location }}</td>
              <td class="hidden md:table-cell border border-secondary px-4 py-2">{{ sensor.unit }}</td>
              <td class="border border-secondary px-4 py-2">{{ sensor.status }}</td>
              <td class="hidden md:table-cell border border-secondary px-4 py-2">{{ sensor.description }}</td>
              <td class="border border-secondary px-4 py-2">
                <button
                  @click="openEditModal(sensor)"
                  class="px-2 py-1 text-extraNeutral bg-secondary rounded hover:bg-transparent hover:text-secondary transition-colors border border-secondary"
                >
                  Manage
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        
        <table v-if="!sensorStore.loading && sensorStore.sensors.length && showMobileVersio" class="w-full border-collapse">
          <thead>
            <tr class="bg-firstRow text-secondary">
              <th class="border border-secondary px-4 py-2 text-left">Name</th>
              <th class="border border-secondary px-4 py-2 text-left">Status</th>
              <th class="border border-secondary px-4 py-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="sensor in sensorStore.sensors.filter(s => s && s.id)" :key="sensor.id" class="hover:bg-hover">
              <td class="border border-secondary px-4 py-2">{{ sensor.name }}</td>
              <td class="border border-secondary px-4 py-2">{{ sensor.status }}</td>
              <td class="border border-secondary px-4 py-2">
                <button
                  @click="openEditModal(sensor)"
                  class="px-2 py-1 glass-effet text-secondary rounded hover:border-2 transition-colors"
                >
                  Manage
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <button
          v-if="sensorStore.sensors.length"
          @click="openAddModal"
          class="m-4 ml-0 px-4 py-2 text-secondary border border-secondary rounded hover:border-2 transition-colors"
          >
          Add New Sensor
        </button>
      </div>
      <div v-if="!sensorStore.loading && !sensorStore.sensors.length" class="text-center py-8 text-gray-400">
        <br><p>No sensors found</p>
        <button
        @click="openAddModal"
        class="m-4 ml-0 px-4 border-2 py-2 bg-secondary-600 text-secondary rounded hover:bg-secondary-700 transition-colors"
        >
        Add New Sensor
        </button>
      </div>
      <SensorModal
        v-if="showModal"
        :sensor="editingSensor"
        @close="closeModal"
        @saved="onSaved"
      />

      <ClamSensorForm
        v-if="showClamSensorForm"
        @close="closeModal"
        @saved="onSaved"
      />
    </div>
    <div v-else>
      <div class="bg-popUpBg rounded-lg p-6">
        <p>Please upgrade your plan to access this feature. If you wish to upgrade your plan please contact us at cottagepilot@gmail.com</p>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { useSensorStore } from '../stores/sensors'
  import SensorModal from '../components/sensors/SensorModal.vue'
  import ClamSensorForm from '../components/sensors/ClamSensorForm.vue'
  import type { Sensor } from '../types'
  import { useAccountStore } from '../stores/account'
  const accountStore = useAccountStore()
  const sensorStore = useSensorStore()
  const showModal = ref(false)
  const editingSensor = ref<Sensor | null>(null)
  const showClamSensorForm = ref(false)
  const showMobileVersio = ref(false)

  const openAddModal = () => {
    showClamSensorForm.value = true
  }

  const openEditModal = (sensor: Sensor) => {
    editingSensor.value = sensor
    showModal.value = true
  }

  const closeModal = () => {
    showModal.value = false
    showClamSensorForm.value = false
  }

  const onSaved = async () => {
    await sensorStore.fetchSensors()
    closeModal()
  }

  onMounted(async () => {
    await sensorStore.fetchSensors()
    await accountStore.fetchAccount()
    console.log(window.innerWidth)
    if (window.innerWidth <= 800){
      showMobileVersio.value = true
    }
  })
</script>