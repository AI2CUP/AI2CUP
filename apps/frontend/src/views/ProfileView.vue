<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-2xl mx-auto">
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <!-- Header -->
        <div class="bg-emerald-600 px-8 py-8 text-center text-white relative">
          <div class="w-20 h-20 bg-white rounded-full mx-auto flex items-center justify-center text-3xl font-bold text-emerald-600 shadow-md mb-4">
            {{ authStore.user?.full_name?.charAt(0).toUpperCase() || 'U' }}
          </div>
          <h1 class="text-2xl font-bold">{{ authStore.user?.full_name }}</h1>
          <p class="text-emerald-100 mt-1 text-sm">Manage your personal information</p>
        </div>

        <!-- Form Section -->
        <div class="p-8">
          <transition name="slide-fade">
            <div v-if="successMessage" class="mb-6 p-4 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center gap-3">
              <span class="text-emerald-500 text-lg">✅</span>
              <p class="text-emerald-800 text-sm font-medium">{{ successMessage }}</p>
            </div>
          </transition>

          <transition name="slide-fade">
            <div v-if="authStore.error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl flex items-center gap-3">
              <span class="text-red-500 text-lg">⚠️</span>
              <p class="text-red-700 text-sm font-medium">{{ authStore.error }}</p>
            </div>
          </transition>

          <form @submit.prevent="handleUpdateProfile" class="space-y-6">
            <!-- Full Name -->
            <div>
              <label for="profile-name" class="block text-sm font-semibold text-gray-700 mb-1.5">Full Name</label>
              <div class="relative">
                <input
                  id="profile-name"
                  v-model="form.full_name"
                  type="text"
                  required
                  placeholder="e.g. Abebe Kebede"
                  class="w-full px-4 py-3 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/40 focus:border-emerald-500 transition-all bg-gray-50/50 hover:bg-white"
                />
              </div>
            </div>

            <!-- Email -->
            <div>
              <label for="profile-email" class="block text-sm font-semibold text-gray-700 mb-1.5">Email Address</label>
              <div class="relative">
                <input
                  id="profile-email"
                  v-model="form.email"
                  type="email"
                  required
                  placeholder="you@example.com"
                  class="w-full px-4 py-3 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/40 focus:border-emerald-500 transition-all bg-gray-50/50 hover:bg-white"
                />
              </div>
            </div>

            <!-- Phone Number -->
            <div>
              <label for="profile-phone" class="block text-sm font-semibold text-gray-700 mb-1.5">Phone Number</label>
              <div class="relative">
                <input
                  id="profile-phone"
                  v-model="form.phone_number"
                  type="tel"
                  required
                  placeholder="e.g. 0911234567"
                  class="w-full px-4 py-3 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/40 focus:border-emerald-500 transition-all bg-gray-50/50 hover:bg-white"
                />
              </div>
            </div>

            <!-- Submit -->
            <div class="pt-4 flex justify-end gap-3 border-t border-gray-100 mt-6">
              <router-link to="/" class="px-6 py-3 text-gray-600 hover:text-gray-900 font-medium transition-colors">
                Cancel
              </router-link>
              <button
                type="submit"
                :disabled="authStore.loading || !hasChanges"
                class="px-8 py-3 bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 text-white font-semibold rounded-xl shadow-md shadow-emerald-500/25 hover:shadow-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none flex items-center justify-center gap-2"
              >
                <svg v-if="authStore.loading" class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                <span>{{ authStore.loading ? 'Saving...' : 'Save Changes' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const form = ref({
  full_name: '',
  email: '',
  phone_number: '',
})

const successMessage = ref('')

onMounted(() => {
  if (authStore.user) {
    form.value = {
      full_name: authStore.user.full_name || '',
      email: authStore.user.email || '',
      phone_number: authStore.user.phone_number || '',
    }
  }
})

const hasChanges = computed(() => {
  if (!authStore.user) return false
  return (
    form.value.full_name !== authStore.user.full_name ||
    form.value.email !== authStore.user.email ||
    form.value.phone_number !== authStore.user.phone_number
  )
})

async function handleUpdateProfile() {
  successMessage.value = ''
  
  // Only send changed fields
  const payload = {}
  if (form.value.full_name !== authStore.user.full_name) payload.full_name = form.value.full_name
  if (form.value.email !== authStore.user.email) payload.email = form.value.email
  if (form.value.phone_number !== authStore.user.phone_number) payload.phone_number = form.value.phone_number

  const success = await authStore.updateProfile(payload)
  if (success) {
    successMessage.value = 'Profile updated successfully!'
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  }
}
</script>

<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
</style>
