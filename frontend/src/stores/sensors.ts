import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { sensorService } from '../services/api'
import type { Sensor, SensorData } from '../types'

export const useSensorStore = defineStore('sensors', () => {
  const sensors = ref<Sensor[]>([])
  const sensorData = ref<SensorData[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const activeSensors = computed(() => 
    sensors.value.filter(sensor => sensor.status === 'active')
  )

  const inactiveSensors = computed(() => 
    sensors.value.filter(sensor => sensor.status === 'inactive')
  )


  const loadSensorsFromLocalStorage = () => {
    const storedSensors = localStorage.getItem('sensors')
    if (storedSensors) {
      sensors.value = JSON.parse(storedSensors)
    }
  }

  const loadSensorDataFromLocalStorage = () => {
    const storedSensorData = localStorage.getItem('sensorData')
    if (storedSensorData) {
      sensorData.value = JSON.parse(storedSensorData)
    }
  }

  async function fetchSensors() {
    loading.value = true
    error.value = null
    try {
      sensors.value = await sensorService.getSensors()
      localStorage.setItem('sensors', JSON.stringify(sensors.value))
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch sensors'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  async function fetchSensorData(sensorId: string, timeRange?: string) {
    loading.value = true
    error.value = null
    try {
      sensorData.value = await sensorService.getSensorData(sensorId, timeRange)
      localStorage.setItem('sensorData', JSON.stringify(sensorData.value))
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch sensor data'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  async function createSensor(sensor: Omit<Sensor, 'id' | 'created_at' | 'updated_at'>) {
    loading.value = true
    error.value = null
    try {
      const newSensor = await sensorService.createSensor(sensor)
      sensors.value.push(newSensor)
      localStorage.setItem('sensors', JSON.stringify(sensors.value))
      return newSensor
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create sensor'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateSensor(id: string, updates: Partial<Sensor>) {
    loading.value = true
    error.value = null
    try {
      const updatedSensor = await sensorService.updateSensor(id, updates)
      const index = sensors.value.findIndex(s => s.id === id)
      if (index !== -1) {
        sensors.value[index] = updatedSensor
        localStorage.setItem('sensors', JSON.stringify(sensors.value))
      }
      return updatedSensor
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update sensor'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteSensor(id: string) {
    loading.value = true
    error.value = null
    try {
      await sensorService.deleteSensor(id)
      sensors.value = sensors.value.filter(s => s.id !== id)
      localStorage.setItem('sensors', JSON.stringify(sensors.value))
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete sensor'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    sensors,
    sensorData,
    loading,
    error,
    activeSensors,
    inactiveSensors,
    loadSensorsFromLocalStorage,
    loadSensorDataFromLocalStorage,
    fetchSensors,
    fetchSensorData,
    createSensor,
    updateSensor,
    deleteSensor
  }
})