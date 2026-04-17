<template>
  <div class="fixed top-20 right-4 z-50 flex flex-col gap-2 pointer-events-none w-full max-w-sm">
    <transition-group name="toast">
      <div 
        v-for="toast in toasts" 
        :key="toast.id"
        class="pointer-events-auto w-full bg-white shadow-lg rounded-lg border-l-4 p-4 flex items-start gap-3 transition-all duration-300 transform"
        :class="[
          toast.type === 'success' ? 'border-emerald-500' : 
          toast.type === 'error' ? 'border-red-500' : 'border-blue-500'
        ]"
      >
        <div class="flex-shrink-0 mt-0.5">
          <span v-if="toast.type === 'success'" class="text-emerald-500">✅</span>
          <span v-else-if="toast.type === 'error'" class="text-red-500">❌</span>
          <span v-else class="text-blue-500">ℹ️</span>
        </div>
        <div class="flex-1">
          <p class="text-sm font-medium text-gray-900">{{ toast.message }}</p>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { useToast } from '../../composables/useToast'

const { toasts } = useToast()
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
