import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { taskService } from '../services/api'
import type { Task } from '../types'

export const useTaskStore = defineStore('tasks', () => {
  const tasks = ref<Task[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const donetaskss = computed(() => 
    tasks.value.filter(tasks => tasks.status === 'done')
  )

  const inProgresstaskss = computed(() => 
    tasks.value.filter(tasks => tasks.status === 'in progress')
  )

  const waitingtaskss = computed(() => 
    tasks.value.filter(tasks => tasks.status === 'waiting')
  )
  
  const overduetaskss = computed(() => 
    tasks.value.filter(tasks => tasks.status === 'overdue')
  )

  async function fetchTasks() {
    loading.value = true
    error.value = null
    try {
      tasks.value = await taskService.getTasks()
      return tasks
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch sensors'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  async function createTask(newTask: Task) {
    loading.value = true
    error.value = null
    try {
      await taskService.createTask(newTask)
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch sensors'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  async function markTaskDone(taskId: string) {
    loading.value = true
    error.value = null
    try {
      await taskService.markTaskDone(taskId)
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch sensors'
      console.error(err)
    } finally {
      loading.value = false
    }
    const task = tasks.value.find(t => t.id === taskId);
    if (task) {
      task.status = "done";  // Vue tracks this change reactively
    }

  }

  return {
    tasks,
    loading,
    error,
    donetaskss,
    inProgresstaskss,
    waitingtaskss,
    overduetaskss,
    fetchTasks,
    createTask,
    markTaskDone
  }
})