import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || '/api/v1'

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
   * Login with email or phone number + password.
   * FastAPI OAuth2 expects form-data, not JSON.
   * The `username` field accepts either email or phone.
   */
  async login(identifier, password) {
    const formData = new URLSearchParams()
    formData.append('username', identifier)
    formData.append('password', password)

    const response = await authApi.post('/auth/token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    return response.data
  },

  /**
   * Register a new user account.
   */
  async register(fullName, email, phoneNumber, password) {
    const response = await authApi.post('/auth/register', {
      full_name: fullName,
      email,
      phone_number: phoneNumber,
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

  /**
   * Update the user's profile.
   */
  async updateProfile(token, profileData) {
    const response = await authApi.put('/auth/me', profileData, {
      headers: { Authorization: `Bearer ${token}` },
    })
    return response.data
  },
}
