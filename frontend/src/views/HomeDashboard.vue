<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useSensorStore } from '../stores/sensors'
import { useTaskStore } from '../stores/tasks'
import CalendarComponent from '../components/calendar/calendarComponent.vue'
import { isSameWeek } from 'date-fns';

const sensorStore = useSensorStore()
const taskStore = useTaskStore()

// Selected month (0 = January, 11 = December)
const currentMonth = ref(new Date().getMonth()) // Current month by default

const sensorsLimited = computed(() => {
  return sensorStore.sensors.length > 5 ? sensorStore.sensors.slice(0, 5) : sensorStore.sensors
})

const urgentTasks = computed(() => {
  return taskStore.tasks.filter(task => {
    const taskMonth = parseInt(task.month_correlation ?? '') - 1
    const parsedDate = task.time_correlation ? new Date(task.time_correlation) : undefined;
    const imdonthMatch = !isNaN(taskMonth) && taskMonth === currentMonth.value && task.status !== 'done'
    const isOverdue = task.status === 'overdue'
    const isInSameWeek = (parsedDate ? isSameWeek(parsedDate, new Date(), { weekStartsOn: 1 }) : false) && task.status !== 'done';
    return imdonthMatch || isOverdue || isInSameWeek
  })
})


onMounted(() => {
  sensorStore.fetchSensors()
  taskStore.fetchTasks()
})
</script>

<template>
  <div class="py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <div class="mb-2 md:mb-4">
        <h1 class="text-3xl font-bold text-secondary mb-3 flex justify-left">Home/Dashboard</h1>
        <p class="text-secondary">Glimps into waht to do</p>
      </div>
      <div class="block md:grid md:grid-cols-6 md:grid-rows-6 md:gap-2 pb-4">
        <!-- Calendar Card -->
        <div class="bg-popUpBg shadow rounded-md col-span-3 row-span-2 mb-4">
          <h2 class="text-xl font-semibold text-secondary pt-6 pl-6">Calendar</h2>
          <CalendarComponent class="h-auto"/>
        </div>



        <!-- Urgent Tasks Card -->
        <div class="bg-popUpBg shadow rounded-md p-6 mb-4 col-start-4 col-span-3 row-start-1 row-span-2">
          <h2 class="text-xl font-semibold text-secondary mb-4">TODO</h2>
          <div v-if="taskStore.loading" class="text-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
            <p class="text-secondary mt-2">Loading...</p>
          </div>
          <div v-else-if="urgentTasks.length === 0" class="text-center py-8">
            <p class="text-secondary/60">No urgent tasks found</p>
          </div>
          <ul v-else class="space-y-4">
            <router-link
              v-for="task in urgentTasks"
              :key="task.id"
              :to="`/task/${task.id}`"
              class="block rounded-md"
            >
              <div class="flex p-4 rounded-md justify-between bg-popUpBg2 items-center hover:bg-primary">
                <div>
                  <h3 class="font-medium text-secondary">{{ task.name }}</h3>
                  <p class="text-sm text-secondary/60">{{ task.description }}</p>
                </div>
                <div class="text-sm font-medium" :class="{
                  'text-red-400': task.status === 'overdue',
                  'text-yellow-400': task.status !== 'done' && task.status !== 'overdue'
                }">
                  {{ task.status }}
                </div>
              </div>
            </router-link>
          </ul>
        </div>

        <!-- Sensors Card -->
        <div class="bg-popUpBg shadow rounded-md p-6 mt-4 col-start-1 col-span-3 row-start-3 row-span-2">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-semibold text-secondary">Sensors</h2>
            <router-link
              to="/manage-sensors"
              class="text-secondary rounded-md hover:bg-primary p-2 rounded-mdtext-sm font-medium"
            >
              View All
            </router-link>
          </div>
          <div v-if="sensorStore.loading" class="text-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
            <p class="text-secondary mt-2">Loading...</p>
          </div>
          <div v-else-if="sensorsLimited.length === 0" class="text-center py-8">
            <p class="text-secondary/60">No sensors found</p>
            <router-link
              to="/manage-sensors/"
              class="text-secondary-400 hover:text-secondary-300 text-sm font-medium mt-2 inline-block"
            >
              Add your first sensor
            </router-link>
          </div>
          <ul v-else class="space-y-4">
            <li
              v-for="sensor in sensorsLimited"
              :key="sensor.id"
              class="p-3 rounded-md bg-popUpBg2 hover:bg-primary transition-colors"
            >
              <div class="flex justify-between items-center">
                <div>
                  <h3 class="font-medium text-secondary">{{ sensor.name }}</h3>
                  <p class="text-sm text-black">{{ sensor.location }}</p>
                </div>
                <div class="text-sm font-medium" :class="{
                  'text-green-600': sensor.status === 'active',
                  'text-gray-600': sensor.status === 'inactive',
                  'text-red-600': sensor.status === 'error'
                }">
                  {{ sensor.status }}
                </div>
              </div>
              <div v-if="sensor.last_reading" class="text-sm text-black mt-1">
                {{ sensor.last_reading }} {{ sensor.unit }}
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
