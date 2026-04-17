import { ref } from 'vue'

export function useLoading() {
  const isLoading = ref(false)
  const error = ref(null)

  async function withLoading(fn) {
    isLoading.value = true
    error.value = null
    try {
      return await fn()
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      isLoading.value = false
    }
  }

  return {
    isLoading,
    error,
    withLoading,
  }
}
