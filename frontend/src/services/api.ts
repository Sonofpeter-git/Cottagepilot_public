import axios, { AxiosResponse, AxiosError } from 'axios'
import type { Sensor, SensorData, ApiResponse, Task, LoginResponse, Account, Note, Reservation, Cottage, cottagePaymentLink} from '../types'
import { useAccountStore } from '../stores/account'

const API_BASE_URL = "https://cottagepilot-production.up.railway.app/"//"http://localhost:8000/"// 


export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Enable sending cookies for session auth
})


// Add a request interceptor
api.interceptors.request.use((config) => {
  const accountStore = useAccountStore(); // Call inside interceptor (after Pinia is ready)
  const token = accountStore.authToken || localStorage.getItem('auth_token');
  if (token) {
    config.headers['Authorization'] = `Token ${token}`;
  } else {
    delete config.headers['Authorization'];
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

//api

// Response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    if (error.response) {
      if (error.response.status === 401) {
        const accountsStore = useAccountStore()
        accountsStore.logout()
        window.location.href = '/login'
      }
      //Access error message
      const data = error.response.data as { message?: string }
      const message = data?.message || 'An error occurred'
      
      return Promise.reject(new Error(message))
    }
    return Promise.reject(error)
  }
)

export const sensorService = {
  async getSensors(): Promise<Sensor[]> {
    const response = await api.get<ApiResponse<Sensor[]>>('/sensors/')
    return response.data.results
  },

  async getSensor(id: string): Promise<Sensor> {
    const response = await api.get<ApiResponse<Sensor>>(`/sensors/${id}/`)
    return response.data.results
  },

  async createSensor(sensor: Omit<Sensor, 'id' | 'created_at' | 'updated_at'>): Promise<Sensor> {
    const response = await api.post<ApiResponse<Sensor>>('/sensors/', sensor)
    return response.data.results
  },

  async updateSensor(id: string, updates: Partial<Sensor>): Promise<Sensor> {
    const response = await api.patch<ApiResponse<Sensor>>(`/sensors/${id}/`, updates)
    return response.data.results
  },

  async deleteSensor(id: string): Promise<void> {
    await api.delete(`/sensors/${id}/`)
  },

  async getSensorData(sensorId: string, timeRange?: string): Promise<SensorData[]> {
    const params = timeRange ? { time_range: timeRange } : {}
    const response = await api.get<ApiResponse<SensorData[]>>(`/sensors/${sensorId}/data/`, { params })
    return response.data.results
  },

  async createSensorData(sensorId: string, data: Omit<SensorData, 'id' | 'sensor_id' | 'timestamp'>): Promise<SensorData> {
    const response = await api.post<ApiResponse<SensorData>>(`/sensors/${sensorId}/data/`, data)
    return response.data.results
  },

  async postClaimSensor(sensorId: string): Promise<Sensor> {
    const response = await api.post<ApiResponse<Sensor>>('/sensors/claim_sensor/', { sensor_id: sensorId })
    return response.data.results
  }
}

//Task service
export const taskService = {
  async getTasks(): Promise<Task[]> {
    const response = await api.get<ApiResponse<Task[]>>('/task/')
    return response.data.results
  },

  async updateTask(id: string, updates: Partial<Task>): Promise<Task> {
    const response = await api.patch<ApiResponse<Task>>(`/task/${id}/`, updates)
    return response.data.results
  },

  async markTaskDone(id: string){
    api.post<ApiResponse<Task>>(`/task/${id}/mark_done/`)
  },


  async deleteTask(id: string): Promise<void> {
    await api.delete(`/task/${id}/`)
  },

  async createTask(task: Task): Promise<Task> {
    const response = await api.post<ApiResponse<Task>>('/task/', task)
    return response.data.results
  },
}
 
//Account service
export const accountService = {
  async get_csrf(): Promise<string>{
    const response = await api.get<{csrfToken: string}>('csrf/')
    const token = response.data.csrfToken
    // Manually set CSRF token header for future POSTs
    api.defaults.headers.common['X-CSRFToken'] = token
    return token
  },

  async login(username: string, password:string): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>('/login/', {username, password})
    return response.data
  },

  async getAccount(): Promise<Account> {
    const response = await api.get<ApiResponse<Account>>('/account/me/')
    // Removed console.log for cleaner code
    return response.data.results
  },

  async fetchCottageUsers(): Promise<Partial<Account[]>> {
    const response = await api.get<ApiResponse<Partial<Account[]>>>('/account/fetchCottageUsers/')
    // Removed console.log for cleaner code
    return response.data.results
  },

  async updateAccount(updates: Partial<Account>): Promise<Account>{
    const response = await api.post<ApiResponse<Account>>('/account/me/', updates);
    return response.data.results
  },
}

//CottageCreate
export const cottageService = {
   async getCottagePaymentLink(name: string, address:string, plan:string): Promise<cottagePaymentLink> {
    const response = await api.post<ApiResponse<cottagePaymentLink>>('/cottage/create-cottage-subscription/', {name, address, stripe_subscription: plan})
    return response.data.results
  },

  async getCottage(): Promise<Cottage> {
    const response = await api.get<ApiResponse<Cottage>>('/cottage/me/')
    return response.data.results
  },

  async updateCottage(updates: Partial<Cottage>): Promise<Cottage>{
    const response = await api.post<ApiResponse<Cottage>>('/cottage/me/', updates);
    return response.data.results
  },

}

//Note service
export const noteService = {
  async getNotes(): Promise<Note[]> {
    const response = await api.get<ApiResponse<Note[]>>('/notes/')
    return response.data.results
  },

  async addNote(classId: string, note: string): Promise<Note> {
    const response = await api.post<ApiResponse<Note>>(`/notes/${classId}/add_note/`, {'note': note})
    return response.data.results
  },

  async deleteNote(classId: string, noteId: string): Promise<void> {
    await api.post(`/notes/${classId}/delete_note/`, {'noteId': noteId})
  },

  async createNoteClass(name: string): Promise<Note> {
    const response = await api.post<ApiResponse<Note>>(`/notes/`, {'noteClassName' : name})
    return response.data.results
    
  },

  async deleteNoteClass(classId: string): Promise<void> {
    await api.delete(`/notes/${classId}/`)
  },
}

//Calendar service
export const calendarService = {
  async getReservations(): Promise<Reservation[]> {
    const response = await api.get<ApiResponse<Reservation[]>>('/calendar/')
    return response.data.results
  },

  async createReservations(newReservation: Reservation): Promise<Reservation> {
    const response = await api.post<ApiResponse<Reservation>>('/calendar/', newReservation)
    return response.data.results
  },

  async updateReservation(id: string, updates: Partial<Reservation>): Promise<Reservation> {
    const response = await api.patch<ApiResponse<Reservation>>(`/calendar/${id}/`, updates)
    return response.data.results
  },

  async deleteReservation(id: string): Promise<void> {
    await api.delete(`/calendar/${id}/`)
  },

}