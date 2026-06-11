import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

export interface HealthCheckResponse {
  status: 'online' | 'offline'
  current_time: string
  total_words: number
  error?: string
}

export async function fetchHealthCheck(): Promise<HealthCheckResponse> {
  try {
    const { data } = await api.get<HealthCheckResponse>('/health')
    return data
  } catch (error: any) {
    if (error.response) {
      return error.response.data
    }
    return {
      status: 'offline',
      current_time: new Date().toISOString(),
      total_words: 0,
      error: error.message || 'Service unavailable',
    }
  }
}
