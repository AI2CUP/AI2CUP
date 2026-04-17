<template>
  <button 
    :type="type" 
    class="btn-primary w-full relative overflow-hidden group"
    :disabled="disabled || loading"
    @click="$emit('click', $event)"
  >
    <div 
      v-if="loading" 
      class="absolute inset-0 flex items-center justify-center bg-emerald-500/80 backdrop-blur-sm z-10"
    >
      <LoadingSpinner class="w-5 h-5 text-white" />
    </div>
    
    <span class="flex items-center gap-2 justify-center transition-transform duration-200" :class="{ 'opacity-0': loading }">
      <slot name="icon"></slot>
      <slot>{{ text }}</slot>
    </span>
    
    <!-- Hover effect overlay -->
    <div class="absolute inset-0 bg-white/20 transform -translate-x-full group-hover:translate-x-0 transition-transform duration-300 ease-out skew-x-12 -ml-8 w-1/3"></div>
  </button>
</template>

<script setup>
import LoadingSpinner from './LoadingSpinner.vue'

defineProps({
  text: { type: String, default: 'Submit' },
  type: { type: String, default: 'button' },
  disabled: { type: Boolean, default: false },
  loading: { type: Boolean, default: false }
})

defineEmits(['click'])
</script>
