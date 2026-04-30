import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '../services/authService'

export const useAuthStore = defineStore('auth', () => {
  // ── State ──
  const user = ref(null)
  const token = ref(localStorage.getItem('ai2cup_token') || null)
  const loading = ref(false)
  const error = ref(null)

  // ── Getters ──
  const isAuthenticated = computed(() => !!token.value)
  const displayName = computed(() => user.value?.full_name || '')

  // ── Actions ──
  async function login(identifier, password) {
    loading.value = true
    error.value = null
    try {
      const data = await authService.login(identifier, password)
      token.value = data.access_token
      localStorage.setItem('ai2cup_token', data.access_token)
      await fetchUser()
      return true
    } catch (err) {
      const detail = err.response?.data?.detail
      error.value = detail || err.message || 'Login failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(fullName, email, phoneNumber, password) {
    loading.value = true
    error.value = null
    try {
      await authService.register(fullName, email, phoneNumber, password)
      // Auto-login after successful registration
      return await login(email, password)
    } catch (err) {
      const detail = err.response?.data?.detail
      error.value = detail || err.message || 'Registration failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    if (!token.value) return
    try {
      const userData = await authService.getMe(token.value)
      user.value = userData
    } catch {
      logout()
    }
  }

  async function updateProfile(profileData) {
    loading.value = true
    error.value = null
    try {
      const userData = await authService.updateProfile(token.value, profileData)
      user.value = userData
      return true
    } catch (err) {
      const detail = err.response?.data?.detail
      error.value = detail || err.message || 'Profile update failed'
      return false
    } finally {
      loading.value = false
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('ai2cup_token')
  }

  async function initialize() {
    if (token.value) {
      await fetchUser()
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    displayName,
    login,
    register,
    logout,
    fetchUser,
    initialize,
    updateProfile,
  }
})
