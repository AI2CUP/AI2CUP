import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor — attach JWT token to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('ai2cup_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor — handle errors and 401s
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    // If 401, the token is expired or invalid
    if (error.response?.status === 401) {
      localStorage.removeItem('ai2cup_token')
      // Redirect to login if not already there
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    const message = error.response?.data?.detail || error.response?.data?.error || error.message || 'Network error occurred'
    console.error('API Error:', message, error)
    return Promise.reject(new Error(message))
  }
)

export default api
