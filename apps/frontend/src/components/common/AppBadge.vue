<template>
  <span 
    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border"
    :class="[colorClass, customClass]"
  >
    <slot></slot>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  color: {
    type: String,
    default: 'gray', // 'gray', 'emerald', 'blue', 'orange', 'red', 'yellow'
  },
  customClass: {
    type: String,
    default: ''
  }
})

const colorClass = computed(() => {
  const map = {
    gray: 'bg-gray-100 text-gray-800 border-gray-200',
    emerald: 'bg-emerald-100 text-emerald-800 border-emerald-200',
    blue: 'bg-blue-100 text-blue-800 border-blue-200',
    orange: 'bg-orange-100 text-orange-800 border-orange-200',
    red: 'bg-red-100 text-red-800 border-red-200',
    yellow: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  }
  
  // Directly passed tailwind classes via useEcxGrades 
  if (props.color.includes('bg-')) {
    return props.color
  }
  
  return map[props.color] || map.gray
})
</script>
