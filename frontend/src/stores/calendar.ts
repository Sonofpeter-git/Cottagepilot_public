import { defineStore } from 'pinia'
import { ref } from 'vue'
import { calendarService } from '../services/api'
import type { Reservation } from '../types'

export const useReservationstore = defineStore('Reservations', () => {
    const Reservations = ref<Reservation[]>([])
    const loading = ref(false)
    const error = ref<string | null>(null)

    async function fetchReservations() {
        loading.value = true
        error.value = null
        try {
        Reservations.value = await calendarService.getReservations()
        console.log(await calendarService.getReservations())
        return Reservations
        } catch (err) {
        error.value = err instanceof Error ? err.message : 'Failed to fetch sensors'
        console.error(err)
        } finally {
        loading.value = false
        }
    }

    async function createReservations(newReservation: Reservation) {
        loading.value = true
        error.value = null
        try {
            const exclusiveEnd = new Date(newReservation.end)
            exclusiveEnd.setDate(exclusiveEnd.getDate() - 1)

            // Format to "YYYY-MM-DD"
            const yyyy = exclusiveEnd.getFullYear()
            const mm   = String(exclusiveEnd.getMonth() + 1).padStart(2, '0')
            const dd   = String(exclusiveEnd.getDate()).padStart(2, '0')
            const inclusiveEndStr = `${yyyy}-${mm}-${dd}`

            const newReservationBody = { ...newReservation }
            newReservationBody.end = inclusiveEndStr

            await calendarService.createReservations(newReservationBody)
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Failed to create new note class'
            console.error(err)
        } finally {
            loading.value = false
            fetchReservations()
        }
    }


    async function updateReservation(id: string, updates: Partial<Reservation>) {
        loading.value = true
        error.value = null
        try {
            const updatedSensor = await calendarService.updateReservation(id, updates)
            return updatedSensor
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Failed to update sensor'
            console.error(err)
            throw err
        } finally {
            loading.value = false
        }
    }

    async function deleteReservation(classId: string) {
        loading.value = true
        error.value = null
        try {
        await calendarService.deleteReservation(classId)
        
        } catch (err) {
        error.value = err instanceof Error ? err.message : 'Failed to delete note class'
        console.error(err)
        } finally {
        loading.value = false
        fetchReservations()
        }
    }


  return {
    Reservations,
    loading,
    error,
    updateReservation,
    deleteReservation,
    fetchReservations,
    createReservations
  }
})