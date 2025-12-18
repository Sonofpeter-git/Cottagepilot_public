<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useTaskStore } from '../stores/tasks'
import { useSensorStore } from '../stores/sensors'
import { useRouter } from 'vue-router'
import type {Task} from '../types/index.ts'


const taskStore = useTaskStore()
const sensorStore = useSensorStore()
const MonthFilterActive = ref(false)
const StatusFilterActive = ref(false)
const SensorFilterActive = ref(false)
const GroupFilterActive = ref(false)
const selectMonth = ref('month')
const selectStatus = ref('status')
const selectSensor = ref('sensor')
const selectGroup = ref('group')
const filterActive = ref(false)
const router = useRouter()
const tasks = ref<Task[]>([])
const showAddForm = ref(false)
const adding = ref(false)

const newTask = ref<Task>({
  id: '',
  name: '',
  description: '',
  additional_info: undefined,
  location: '',
  status: 'waiting',
  sensor: undefined,
  limit_value: undefined,
  month_correlation: undefined,
  time_correlation: undefined,
})

const monthOptions: Record<string, string> = {
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

const statusOptions = ['done', 'in progress', 'waiting', 'overdue']

function filter(){
  tasks.value = taskStore.tasks
  if (selectMonth.value == 'month'){
    MonthFilterActive.value = false;
  } else {
    MonthFilterActive.value = true;
  }
  
  if (selectStatus.value == "status"){
    StatusFilterActive.value = false;
  } else {
    StatusFilterActive.value = true;
  }

  if (selectSensor.value == "sensor"){
    SensorFilterActive.value = false;
  } else {
    SensorFilterActive.value = true;
  }

  if (selectGroup.value == "group"){
    GroupFilterActive.value = false
  } else{
    GroupFilterActive.value = true
  }
    

  if (MonthFilterActive .value == true || StatusFilterActive.value == true || SensorFilterActive.value == true || GroupFilterActive.value == true){
    filterActive.value = true
  } else {
    filterActive.value = false
  }


  //handle all possible filter cases
  if (MonthFilterActive.value == true){
   tasks.value = (tasks.value).filter((task: { month_correlation?: string }) => task.month_correlation === selectMonth.value)
  }
 
  if (StatusFilterActive.value == true){
    tasks.value = (tasks.value).filter((task: { status: string }) => task.status === selectStatus.value)
  }

  if (SensorFilterActive.value == true){
    tasks.value = (tasks.value).filter((task: { sensor_name?: string }) => task.sensor_name === selectSensor.value)
  }

  if (GroupFilterActive.value == true){
    tasks.value = (tasks.value).filter((task: { group?: string }) => task.group === selectGroup.value)
  }
}

const addTask = async () => {
  adding.value = true
  try {
    await taskStore.createTask(newTask.value)
    showAddForm.value = false
    // Reset form
    newTask.value = {
        id: '',
        name: '',
        description: '',
        additional_info: undefined,
        location: '',
        status: 'waiting',
        owner: '',
        sensor: undefined,
        limit_value: undefined,
        month_correlation: undefined,
        time_correlation: undefined,
        created_at: new Date().toISOString()
    }
    await taskStore.fetchTasks()
    tasks.value = taskStore.tasks
  } catch (error) {
    console.error('Failed to add task:', error)
  } finally {
    adding.value = false
  }
}

const cancelAdd = () => {
  showAddForm.value = false
}

onMounted(async () => {
  await taskStore.fetchTasks()
  tasks.value = taskStore.tasks
  await sensorStore.fetchSensors()
  console.log(taskStore.tasks)
})
</script>

<style scoped>
.tasks-view {
  justify-content: space;
}
</style>

<template>
  <div class="block center pt-10">
    <h1 class="text-3xl font-bold mb-3 text-title_font text-secondary text-center">Tasks</h1>
    <p class="text-secondary text-center">Glimps into what to do</p>
  </div>  
  <div class="flex justify-center flex-wrap">
    <div class="m-5 mb-20 shadow rounded-md bg-popUpBg">
      <h1 class="block text-center font-bold mb-4 text-secondary text-title_font">All tasks</h1>
      <div class="tasks-view p-4 flex flex-col md:flex-row text-secondary md:justify-center">
        <div v-if="taskStore.loading" class="bg-popUpBg2 w-max">Loading tasks...</div>
        <table v-else class="bg-popUpBg2 w-max">
          <thead class="glass-effect p-6 mb-8 rounded-lg">
            <tr class="glass-effect">
              <th class="border border-2 px-4 py-2 text-secondary text-left text-secondary">Name</th>
              <th class="hidden md:table-cell table-cell border border-2 px-4 py-2 text-secondary text-left">Description</th>
              <th class="hidden md:table-cell border border-2 px-4 py-2 text-secondary text-left">Month</th>
              <th class="border border-2 px-4 py-2 text-secondary text-left text-secondary">Status</th>
              <th class="hidden md:table-cell border border-2 px-4 py-2 text-secondary text-left">Location</th>
              <th class="hidden md:table-cell border border-2 px-4 py-2 text-secondary text-left">Alert</th>
              <th class="hidden md:table-cell border border-2 px-4 py-2 text-secondary text-left">Time</th>
            </tr>
          </thead>
          <tbody class="mb-8 p-6">
            <tr v-for="task in tasks" :key="task.id" class="hover:bg-gray-500" :class="task.status === 'overdue' ? 'bg-red-600'  :''">
              <td @click="router.push('/task/'+task.id)" class="border border-2 px-4 py-2 text-secondary" >{{ task.name }}</td>
              <td @click="router.push('/task/'+task.id)" class="hidden md:table-cell border border-2 px-4 py-2 text-secondary" >{{ task.description }}</td>
              <td @click="router.push('/task/'+task.id)" class="hidden md:table-cell border border-2 px-4 py-2 text-secondary" >{{ monthOptions[task.month_correlation  ?? '']|| 'N/A' }}</td>
              <td @click="router.push('/task/'+task.id)" class="border border-2 px-4 py-2 text-secondary" >{{ task.status }}</td>
              <td @click="router.push('/task/'+task.id)" class="hidden md:table-cell border border-2 px-4 py-2 text-secondary" >{{ task.location }}</td>
              <td @click="router.push('/task/'+task.id)" class="hidden md:table-cell border border-2 px-4 py-2 text-secondary" >{{ task.limit_value && task.sensor_unit ? task.limit_value + task.sensor_unit : 'N/A' }}</td>
              <td @click="router.push('/task/'+task.id)" class="hidden md:table-cell border border-2 px-4 py-2 text-secondary" >{{ task.time_correlation || 'N/A' }}</td>
            </tr>
          </tbody>
        </table>
        <div v-if="taskStore.tasks.length === 0" class="text-center mt-4">No tasks found.</div>
        <div class="glass-effect rounded-lg p-6 ml-4 mb-4 p-6 py-0 block space-x-4 md:ml-0 md:mt-4">
          <h1 class="text-2xl block font-bold mb-4 ">Tasks</h1>
          <div>
            <label for="orderMonth" class="block mb-1 font-semibold">Filter</label>
            <select id="orderMonth" v-model="selectMonth" @change="filter()" class="border-2 rounded m-1 ml-0 p-1 block bg-white/10">
              <option class="text-secondary" value="month" selected>Month</option>
              <option v-for="(monthName, monthNum) in monthOptions" :key="monthNum" :value="monthNum" class="text-secondary" >
                {{ monthName }}
              </option>
            </select>
            <select id="orderMonth" v-model="selectStatus" @change="filter()" class="border-2 rounded m-1 ml-0 p-1 block bg-white/10">
              <option class="text-secondary" value="status" name="status">Status</option>
              <option v-for="(status) in statusOptions" :key="status" :value="status" class="text-secondary" >
                {{ status }}
              </option>
            </select>
            <select id="orderStatus" v-model="selectSensor" @change="filter()" class="border-2 rounded m-1 ml-0 p-1 block bg-white/10">
              <option class="text-secondary" value="sensor" name="sensor">Sensor</option>
              <option v-for="(sensor_name) in [...new Set(taskStore.tasks.filter(task => task.sensor_name).map(task => task.sensor_name))]" :key="sensor_name" :value="sensor_name" class="text-secondary">
                {{ sensor_name }}
              </option>
            </select>
            <select id="orderGroup" v-model="selectGroup" @change="filter()" class="border-2 rounded m-1 p-1 ml-0 block bg-white/10">
              <option class="text-secondary"  value="group" name="group">Group</option>
              <option v-for="(group) in [...new Set(taskStore.tasks.filter(task => task.group).map(task => task.group))]" :key="group" :value="group" class="text-secondary" >
                {{ group }}
              </option>
            </select>
          </div>
          <button @click="showAddForm = true" class="mt-4 border border-2 rounded border-2 p-1 mb-5 bg-white/10 hover:bg-white/20">Create new task</button>
        </div>
      </div>

      <!-- Modal for adding new task -->
      <div v-if="showAddForm" class="fixed inset-0 flex itemd-center justify-center glass-effect bg-opacity-50 z-50 overflow-y-scroll p-1">
        <div class="bg-white/10 text-secondary rounded-lg shadow-lg primary-bg p-6 w-full max-w-md md:mt-60 ml:mt-0">
          <h2 class="text-xl font-bold mb-4">Add New Task</h2>
          <form @submit.prevent="addTask" class="space-y-1 text-content_font">
            <div>
              <label for="name" class="block font-semibold mb-1">Name</label>
              <input id="name" v-model="newTask.name" type="text" required class="w-full border border-2 rounded p-2 bg-white/10" />
            </div>
            <div>
              <label for="group" class="block font-semibold mb-1">Task group</label>
              <input id="group" v-model="newTask.group" type="text" required class="w-full border border-2 rounded p-2 bg-white/10" />
            </div>
            <div>
              <label for="description" class="block font-semibold mb-1">Description</label>
              <textarea id="description" v-model="newTask.description" rows="3" class="w-full border border-2 rounded p-2 bg-white/10"></textarea>
            </div>
            <div>
              <label for="location" class="block font-semibold mb-1">Location</label>
              <input id="location" v-model="newTask.location" type="text" class="w-full border border-2 rounded p-2 bg-white/10" />
            </div>
            <div>
              <label for="status" class="block font-semibold mb-1">Status</label>
              <select id="status" v-model="newTask.status" class="w-full border border-2 rounded p-2 bg-white/10">
                <option class="text-secondary" value="waiting">Waiting</option>
                <option class="text-secondary" value="in progress">In Progress</option>
                <option class="text-secondary" value="done">Done</option>
                <option class="text-secondary" value="overdue">Overdue</option>
              </select>
            </div>
            <div>
              <label for="month_correlation" class="block font-semibold mb-1">Month</label>
              <select id="month_correlation" v-model="newTask.month_correlation" class="w-full border border-2 rounded p-2 bg-white/10">
              <option class="text-secondary" :value="null">Select Month</option>
              <option class="text-secondary" v-for="(monthName, monthNum) in monthOptions" :key="monthNum" :value="monthNum">
                {{ monthName }}
              </option>
              </select>
            </div>
            <div>
              <label for="status" class="block font-semibold mb-1">Sensor</label>
              <select id="status" v-model="newTask.sensor" class="w-full border border-2 rounded p-2 bg-white/10 text-content_font">
                <option class="text-secondary" v-for="(sensor) in sensorStore.sensors" :key="sensor.id" :value="sensor.id">{{ sensor.name }}</option>
      
              </select>
            </div>
            <div>
              <label for="limit_value" class="block font-semibold mb-1">Limit Value</label>
              <input id="limit_value" v-model.number="newTask.limit_value" type="number" class="w-full border border-2 rounded p-2 bg-white/10 text-content_font" />
            </div>
            <div>
              <label for="time_correlation" class="block font-semibold mb-1">Time Correlation</label>
              <input id="time_correlation" v-model="newTask.time_correlation" type="date" class="w-full border border-2 rounded p-2 bg-white/10 text-content_font" />
            </div>
            <div>
              <label for="additional_info" class="block font-semibold mb-1">Additional Info</label>
              <textarea id="additional_info" v-model="newTask.additional_info" rows="2" class="w-full border border-2 rounded p-2 bg-white/10 text-content_font"></textarea>
            </div>
            <div class="flex justify-end space-x-4">
              <button type="button" @click="cancelAdd" class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">Cancel</button>
              <button type="submit" :disabled="adding" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                {{ adding ? 'Adding...' : 'Add Task' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
