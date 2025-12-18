<script setup lang="ts">
import { ref, onMounted } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import { useReservationstore } from '../../stores/calendar'
import type { Account, Reservation } from '../../types'
import interactionPlugin from '@fullcalendar/interaction'
import { useAccountStore } from '../../stores/account'

// events reactive array typed as Reservation[]
const events = ref<Reservation[]>([])

const title = ref('')
const reservationOwner = ref('')
const users = ref<Account[]>([])
const modalVisible = ref(false)
const selectedDateRange = ref<{startStr: string, endStr: string} | null>(null)

const Reservationstore = useReservationstore()
const accountStore = useAccountStore()

const handleEventClick = async (info: any) => {
  const confirmed = confirm('Do you want to delete this reservation?')
  if (confirmed) {
    try {
      await Reservationstore.deleteReservation(info.event.id)
      // Remove event from local events array
      events.value = events.value.filter(event => Number(event.id) !== Number(info.event.id))
      // Force update calendar events by resetting the array reference
      calendarOptions.value.events = [...events.value]
    } catch (error) {
      alert('Failed to delete reservation')
      console.error('Error deleting reservation:', error)
    }
  }
}

// handle date selection
const handleDateSelect = async (selectionInfo: any) => {
  selectedDateRange.value = { startStr: selectionInfo.startStr, endStr: selectionInfo.endStr }
  title.value = ''
  reservationOwner.value = ''
  modalVisible.value = true
}

const saveReservation = async () => {
  if (!title.value || !reservationOwner.value || !selectedDateRange.value) {
    alert('Please fill in all fields')
    return
  }

  const owner = users.value.find(user => user.id === reservationOwner.value)
  if (!owner) {
    console.error('Reservation owner not found')
    return
  }
  

  const newEvent = {
    id: Date.now().toString(),
    title: title.value + " " + owner.username,
    start: selectedDateRange.value.startStr,
    end: selectedDateRange.value.endStr,
    reservationOwner: reservationOwner.value,
    color: owner.user_color
  }
  events.value.push(newEvent)
  calendarOptions.value.events = [...events.value]
  modalVisible.value = false
  title.value = ''
  reservationOwner.value = ''
  selectedDateRange.value = null
  await Reservationstore.createReservations(newEvent)
}

const cancelReservation = () => {
  modalVisible.value = false
  title.value = ''
  reservationOwner.value = ''
  selectedDateRange.value = null
}

// calendar options reactive object
const calendarOptions = ref({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  selectable: true,
  editable: true,
  events: events.value,
  eventClick: handleEventClick,
  select: handleDateSelect,
  weekNumbers: true,
  weekText: '',
  firstDay: 1
})

onMounted(async () => {
  try {
    const Reservations = await Reservationstore.fetchReservations()
    if (Reservations) {
      events.value = Reservations.value.map((reservation: Reservation) => ({
        id: reservation.id,
        description: reservation.description,
        title: (reservation.title + " " + reservation.ownerName),
        start: reservation.start,
        end: reservation.end,
        color: reservation.eventColor
      }))
      // update the calendarOptions.events after fetching
      calendarOptions.value.events = events.value
    }
    // fetch users for reservationOwner select
    const fetchedUsers = await accountStore.fetchCottageUsers()
    if (fetchedUsers) {
      users.value = fetchedUsers.filter((user): user is Account => user !== undefined)
    }
  } catch (error) {
    console.error('Error fetching events or users:', error)
  }
})
</script>
z
<template>
      <!-- Calendar Card -->
      <div class="rounded-lg p-6 text-secondary">
        <FullCalendar :options="calendarOptions" />
        <div v-if="modalVisible" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div class="bg-secondary text-extraNeutral rounded-lg p-6 w-96">
            <h2 class="text-xl font-bold mb-4 text-extraNeutral">New Reservation</h2>
            <div class="mb-4">
              <label for="title" class="block mb-1 text-extraNeutral">Title</label>
              <input id="title" v-model="title" type="text" class="w-full p-2 rounded bg-gray-700 text-extraNeutral border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div class="mb-4">
              <label for="reservationOwner" class="block mb-1 text-extraNeutral">Reservation Owner</label>
              <select id="reservationOwner" v-model="reservationOwner" class="w-full p-2 rounded bg-gray-700 text-extraNeutral border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="" disabled>Select a user</option>
                <option v-for="user in users" :key="user.id" :value="user.id">{{ user.username }}</option>
              </select>
            </div>
            <div class="flex justify-end space-x-4">
              <button @click="cancelReservation" class="px-4 py-2 bg-gray-600 rounded hover:bg-gray-500 text-extraNeutral">Cancel</button>
              <button @click="saveReservation" class="px-4 py-2 bg-primary text-secondary rounded hover:bg-blue-500 text-extraNeutral">Save</button>
            </div>
          </div>
        </div>
    </div>
</template>
