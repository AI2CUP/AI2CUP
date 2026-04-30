<template>
  <nav class="w-full bg-white/90 backdrop-blur-md border-b border-gray-100 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <router-link to="/" class="flex-shrink-0 flex items-center gap-3">
            <span class="text-2xl" role="img" aria-label="coffee">☕</span>
            <div>
              <div class="font-bold text-xl text-gray-900 tracking-tight leading-none">AI2CUP</div>
              <div class="text-[0.65rem] uppercase tracking-wider text-emerald-600 font-semibold mt-0.5">AI for Ethiopian Coffee</div>
            </div>
          </router-link>
        </div>
        
        <div class="hidden sm:flex sm:items-center sm:space-x-6">
          <!-- Nav Links -->
          <div class="flex space-x-6">
            <router-link 
              to="/price" 
              class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
              :class="[ $route.path === '/price' ? 'border-emerald-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700' ]"
            >
              Price
            </router-link>
            <router-link 
              to="/quality" 
              class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
              :class="[ $route.path === '/quality' ? 'border-emerald-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700' ]"
            >
              Quality
            </router-link>
            <router-link 
              to="/marketplace" 
              class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
              :class="[ $route.path === '/marketplace' ? 'border-emerald-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700' ]"
            >
              Market
            </router-link>
          </div>

          <!-- Auth Section -->
          <div class="flex items-center pl-6 border-l border-gray-200">
            <template v-if="authStore.isAuthenticated">
              <!-- User Dropdown -->
              <div class="relative" @click="dropdownOpen = !dropdownOpen" v-click-outside="() => dropdownOpen = false">
                <div class="flex items-center gap-2 px-3 py-1.5 bg-emerald-50 rounded-lg border border-emerald-100 cursor-pointer hover:bg-emerald-100 transition-colors">
                  <div class="w-6 h-6 bg-emerald-500 rounded-full flex items-center justify-center text-white text-xs font-bold">
                    {{ authStore.displayName.charAt(0).toUpperCase() }}
                  </div>
                  <span class="text-sm font-medium text-emerald-800 max-w-[100px] truncate">{{ authStore.displayName }}</span>
                  <svg class="w-4 h-4 text-emerald-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
                
                <!-- Dropdown Menu -->
                <transition name="slide-fade">
                  <div v-if="dropdownOpen" class="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg shadow-black/10 border border-gray-100 py-2 z-50">
                    <router-link to="/profile" @click="dropdownOpen = false" class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors">
                      <svg class="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      My Profile
                    </router-link>
                    <button @click="handleLogout" class="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors text-left">
                      <svg class="w-4 h-4 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      Sign out
                    </button>
                  </div>
                </transition>
              </div>
            </template>
            <template v-else>
              <router-link
                to="/login"
                class="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors mr-3"
              >
                Sign In
              </router-link>
              <router-link
                to="/register"
                class="text-sm font-semibold text-white bg-emerald-600 hover:bg-emerald-700 px-4 py-2 rounded-lg transition-colors shadow-sm"
              >
                Sign Up
              </router-link>
            </template>
          </div>
        </div>
        
        <!-- Mobile menu button -->
        <div class="flex items-center sm:hidden gap-2">
          <!-- Mobile Auth -->
          <template v-if="authStore.isAuthenticated">
            <div class="w-7 h-7 bg-emerald-500 rounded-full flex items-center justify-center text-white text-xs font-bold">
              {{ authStore.displayName.charAt(0).toUpperCase() }}
            </div>
          </template>
          <template v-else>
            <router-link to="/login" class="text-emerald-600 text-sm font-medium">
              Sign In
            </router-link>
          </template>

          <button @click="mobileOpen = !mobileOpen" class="text-gray-500 hover:text-gray-700 p-2">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="!mobileOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <transition name="slide-down">
      <div v-if="mobileOpen" class="sm:hidden bg-white border-t border-gray-100 shadow-lg">
        <div class="px-4 py-4 space-y-2">
          <router-link @click="mobileOpen = false" to="/price" class="block px-4 py-2.5 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors"
            :class="$route.path === '/price' ? 'bg-emerald-50 text-emerald-700' : 'text-gray-700'">
            Price Prediction
          </router-link>
          <router-link @click="mobileOpen = false" to="/quality" class="block px-4 py-2.5 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors"
            :class="$route.path === '/quality' ? 'bg-emerald-50 text-emerald-700' : 'text-gray-700'">
            Quality Detection
          </router-link>
          <router-link @click="mobileOpen = false" to="/marketplace" class="block px-4 py-2.5 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors"
            :class="$route.path === '/marketplace' ? 'bg-emerald-50 text-emerald-700' : 'text-gray-700'">
            Marketplace
          </router-link>

          <div class="border-t border-gray-100 pt-3 mt-3">
            <template v-if="authStore.isAuthenticated">
              <div class="flex items-center justify-between px-4 py-2">
                <div class="flex items-center gap-2">
                  <div class="w-8 h-8 bg-emerald-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                    {{ authStore.displayName.charAt(0).toUpperCase() }}
                  </div>
                  <span class="text-sm font-medium text-gray-800">{{ authStore.displayName }}</span>
                </div>
                <button @click="handleLogout" class="text-sm text-red-500 font-medium">
                  Sign Out
                </button>
              </div>
            </template>
            <template v-else>
              <router-link @click="mobileOpen = false" to="/login" class="block px-4 py-2.5 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50">
                Sign In
              </router-link>
              <router-link @click="mobileOpen = false" to="/register" class="block px-4 py-2.5 rounded-lg text-sm font-semibold text-white bg-emerald-600 text-center mt-1">
                Create Account
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const mobileOpen = ref(false)
const dropdownOpen = ref(false)

// Custom directive for clicking outside dropdown
const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = function (event) {
      if (!(el == event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent)
  },
}

function handleLogout() {
  dropdownOpen.value = false
  authStore.logout()
  mobileOpen.value = false
  router.push('/')
}
</script>

<style scoped>
.slide-down-enter-active {
  transition: all 0.2s ease-out;
}
.slide-down-leave-active {
  transition: all 0.15s ease-in;
}
.slide-down-enter-from {
  transform: translateY(-8px);
  opacity: 0;
}
.slide-down-leave-to {
  transform: translateY(-4px);
  opacity: 0;
}
</style>
