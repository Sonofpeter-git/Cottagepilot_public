<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTaskStore } from '../stores/tasks'
import { taskService } from '../services/api'

const route = useRoute()
const router = useRouter()
const taskStore = useTaskStore()

const taskId = route.params.id
const task = ref()
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const error = ref()
const success = ref()

const monthOptions = {
  '1': 'January',
  '2': 'February',
  '3': 'March',
  '4': 'April',
  '5': 'May',
  '6': 'June',
  '7': 'July',
  '8': 'August',
  '9': 'September',
  '10': 'October',
  '11': 'November',
  '12': 'December'
}

const fetchTask = () => {
  loading.value = true
  error.value = null
  success.value = null
  const found = taskStore.tasks.find(t => t.id === taskId)
  if (found) {
    task.value = { ...found }
    loading.value = false
  } else {
    // If not found in store, fetch from API
    taskService.getTasks().then(tasks => {
      const t = tasks.find(t => t.id === taskId)
      if (t) {
        task.value = { ...t }
      } else {
        error.value = 'Task not found'
      }
      loading.value = false
    }).catch(err => {
      error.value = err.message || 'Failed to load task'
      loading.value = false
    })
  }
}

const saveTask = async () => {
  if (!task.value) return
  saving.value = true
  error.value = null
  success.value = null
  try {
    await taskService.updateTask(task.value.id, task.value)
    success.value = 'Task saved successfully'
    // Update store
    await taskStore.fetchTasks()
  } catch (ex) {
    error.value = 'Failed to save task'
  } finally {
    saving.value = false
  }
}

const deleteTask = async () => {
  if (!task.value) return
  if (!confirm('Are you sure you want to delete this task?')) return
  deleting.value = true
  error.value = null
  success.value = null
  try {
    await taskService.deleteTask(task.value.id)
    success.value = 'Task deleted successfully'
    // Update store
    await taskStore.fetchTasks()
    router.push('/task-list/')
  } catch (err) {
    error.value = 'Failed to delete task'
  } finally {
    deleting.value = false
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchTask()
})
</script>

<style scoped>
.task-details {
  max-width: 900px;
}
</style>

<template>
  <div class="task-details p-4 max-w-3xl mx-auto text-secondary">
    <h1 class="text-2xl font-bold mb-4">Task Details</h1>

    <div v-if="loading" class="text-center">Loading task...</div>
    <div v-else>
      <form @submit.prevent="saveTask" class="space-y-4">
        <div class=" rounded-lg p-6">
          <label class="block font-semibold mb-1" for="name">Name</label>
          <input id="name" v-model="task.name" type="text" class="w-full border border-borderColor shadow rounded p-2 text-secondary bg-popUpBg" required />
        </div>

        <div class=" rounded-lg p-6">
          <label class="block font-semibold mb-1" for="description">Description</label>
          <textarea id="description" v-model="task.description" class="w-full border border-borderColor shadow rounded p-2 text-secondary bg-popUpBg" rows="3" required></textarea>
        </div>

        <div class=" rounded-lg p-6">
          <label class="block font-semibold mb-1" for="additional_info">Additional Info</label>
          <textarea id="additional_info" v-model="task.additional_info" class="w-full border border-borderColor shadow rounded p-2 text-secondary bg-popUpBg" rows="2"></textarea>
        </div>

        <div class=" rounded-lg p-6">
          <label class="block font-semibold mb-1" for="location">Location</label>
          <input id="location" v-model="task.location" type="text" class="w-full border border-borderColor shadow rounded p-2 text-secondary bg-popUpBg" required />
        </div>

        <div class=" rounded-lg p-6">
          <label class="block font-semibold mb-1" for="status">Status</label>
          <select id="status" v-model="task.status" class="w-full border border-borderColor shadow rounded p-2 text-secondary bg-popUpBg" required>
            <option class="text-secondary" value="done">Done</option>
            <option class="text-secondary" value="in progress">In progress</option>
            <option class="text-secondary" value="waiting">Waiting</option>
            <option class="text-secondary" value="overdue">Overdue</option>
          </select>
        </div>

        <div class=" rounded-lg p-3">
          <label class="block font-semibold mb-1" for="limit_value">Task group</label>
          <input id="group" v-model.number="task.group" type="string" class="w-full border border-borderColor shadow rounded p-2 text-secondary bg-popUpBg" />
        </div>

        <div class=" rounded-lg p-3">
          <label class="block font-semibold mb-1" for="limit_value">Limit Value</label>
          <input id="limit_value" v-model.number="task.limit_value" type="number" class="w-full border border-borderColor shadow rounded p-2 text-secondary bg-popUpBg" />
        </div>

        <div class=" rounded-lg p-6">
          <label class="block font-semibold mb-1" for="month_correlation">Month Correlation</label>
          <select id="month_correlation" v-model="task.month_correlation" class="w-full border border-borderColor shadow rounded p-2 text-secondary bg-popUpBg">
            <option value="" text-secondary>None</option>
            <option v-for="(monthName, monthNum) in monthOptions" :key="monthNum" :value="monthNum" class="text-secondary">
              {{ monthName }}
            </option>
          </select>
        </div>  

        <div class=" rounded-lg p-6">
          <label class="block font-semibold mb-1" for="time_correlation">Due date</label>
          <input id="time_correlation" v-model="task.time_correlation" type="date" class="w-full border border-borderColor shadow rounded p-2 text-secondary bg-popUpBg" />
        </div>

        <div class="flex space-x-4 mt-6">
          <button type="submit" class="bg-primary text-secondary px-4 py-2 rounded hover:bg-blue-700" :disabled="saving">
            {{ saving ? 'Saving...' : 'Save' }}
          </button>
          <button type="button" @click="deleteTask" class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700" :disabled="deleting">
            {{ deleting ? 'Deleting...' : 'Delete' }}
          </button>
          <button type="button" @click="goBack" class="bg-secondary text-extraNeutral px-4 py-2 rounded hover:bg-gray-500">
            Back
          </button>
        </div>
      </form>
      <div v-if="error" class="mt-4 text-red-600 font-semibold">{{ error }}</div>
      <div v-if="success" class="mt-4 text-green-600 font-semibold">{{ success }}</div>
    </div>
  </div>
</template>
