<template>
  <div class="w-full">
    <div class="flex justify-between items-end mb-1">
      <span class="text-sm font-medium text-gray-700">{{ label }}</span>
      <span class="text-sm font-bold text-gray-900">{{ percentage }}%</span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
      <div 
        class="h-2.5 rounded-full transition-all duration-1000 ease-out"
        :class="colorClass"
        :style="{ width: `${percentage}%` }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  score: {
    type: Number,
    required: true // 0.0 to 1.0 or 0 to 100
  },
  label: {
    type: String,
    default: 'Confidence'
  }
})

const percentage = computed(() => {
  const val = props.score <= 1.0 && props.score > 0 ? props.score * 100 : props.score
  return Math.round(val)
})

const colorClass = computed(() => {
  if (percentage.value >= 85) return 'bg-amber-500'
  if (percentage.value >= 70) return 'bg-blue-500'
  if (percentage.value >= 50) return 'bg-yellow-500'
  return 'bg-red-500'
})
</script>
