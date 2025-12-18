//Sensor types
export interface Sensor {
  id: string
  name: string
  type: 'temperature' | 'humidity' | 'pressure' | 'light' | 'motion' | 'air_quality'
  location: string
  description?: string
  status: 'active' | 'inactive' | 'error'
  last_reading?: number
  unit: string
  created_at: string
  updated_at: string
}

export interface ClaimSensor {
  sensor_id: string
  name: string
  type: 'temperature' | 'humidity' | 'pressure' | 'light' | 'motion' | 'air_quality'
  location: string
  description?: string
  status: 'active' | 'inactive' | 'error'
  unit: string
}


export interface SensorData {
  id: string
  sensor_id: string
  value: number
  timestamp: string
  metadata?: Record<string, any>
}

export interface ApiResponse<T> {
  results: T
  message?: string
  status: 'success' | 'error'
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  per_page: number
  total_pages: number
}


//Task types
export interface Task {
  id: string
  name: string
  description?: string
  group?: string
  additional_info?: string
  location: string
  status: 'done' | 'in progress' | 'waiting' | 'overdue'
  owner?: string 
  sensor?: string
  sensor_unit?: string
  sensor_name?: string
  created_at?: string
  updated_at?: string
  limit_value?: BigInteger
  month_correlation?: string
  time_correlation?: string
}

// Account type
export interface Account {
  id: string
  username: string
  email: string
  first_name?: string
  last_name?: string
  is_active: boolean
  created_at: string
  updated_at: string
  user_color: string
  access_to_cottage: string
  cottage_plan: string
}

export interface LoginResponse {
  account: Account
  token: string
  created: string
  message?: string
  cottageInstanceActive: string
  status: 'success' | 'error'
}

export interface signUpResponse {
  account: Account
  token: string
  created: string
  redirect: string
  cottageInstanceActive: string
  message?: { [key: string]: string[]; }
}

// Stats interface for Sensor-Dashboard
export interface Stats {
  total: number
  active: number
  inactive: number
  error: number
}


// Note type

export interface Note {
  id: string,
  noteClassName : string,
  notes: SingleNote[]
}

export interface SingleNote {
  id: string
  note: string
}

export interface Reservation {
  id?: string
  title: string
  start: string // ISO date string
  end: string   // ISO date string
  description?: string
  reservationOwner?: string 
  eventColor?: string
  ownerName?: string
}

export interface newReservation {
  id?: string
  title: string
  start: string // ISO date string
  end: string   // ISO date string
  reservationOwner?: string 
}


//Cottage types

export interface Cottage {
  id: string
  name: string
  owner: string
  ownerUsername: string
  address: string
  stripe_subscription: string
  stripe_payment_status_int: BigInteger
}
export interface cottagePaymentLink {
  payment_link:string,
}


