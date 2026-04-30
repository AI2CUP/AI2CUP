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
  const displayName = computed(() => user.value?.username || '')

  // ── Actions ──
  async function login(username, password) {
    loading.value = true
    error.value = null
    try {
      const data = await authService.login(username, password)
      token.value = data.access_token
      localStorage.setItem('ai2cup_token', data.access_token)
      await fetchUser()
      return true
    } catch (err) {
      error.value = err.message || 'Login failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(username, email, password) {
    loading.value = true
    error.value = null
    try {
      await authService.register(username, email, password)
      // Auto-login after successful registration
      return await login(username, password)
    } catch (err) {
      error.value = err.message || 'Registration failed'
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
      // Token is invalid/expired — clear everything
      logout()
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('ai2cup_token')
  }

  // Hydrate user on app start if we have a token
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
  }
})
