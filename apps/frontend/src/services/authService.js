import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

/**
 * Auth service — uses a separate axios instance (no interceptors)
 * to avoid circular redirect loops on 401 during login/register.
 */
const authApi = axios.create({
  baseURL: API_URL,
  timeout: 15000,
})

export const authService = {
  /**
   * Login with username and password.
   * FastAPI OAuth2 expects form-data, not JSON.
   */
  async login(username, password) {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)

    const response = await authApi.post('/auth/token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    return response.data
  },

  /**
   * Register a new user account.
   */
  async register(username, email, password) {
    const response = await authApi.post('/auth/register', {
      username,
      email,
      password,
    })
    return response.data
  },

  /**
   * Get the currently authenticated user's profile.
   */
  async getMe(token) {
    const response = await authApi.get('/auth/me', {
      headers: { Authorization: `Bearer ${token}` },
    })
    return response.data
  },
}
