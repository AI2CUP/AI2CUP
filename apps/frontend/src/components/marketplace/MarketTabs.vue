<template>
  <div class="flex space-x-1 bg-gray-100/50 p-1 rounded-xl w-full max-w-sm mb-6 border border-gray-200/50">
    <button
      v-for="tab in tabs"
      :key="tab.id"
      class="flex-1 py-2.5 px-4 rounded-lg text-sm font-medium transition-all duration-200 outline-none"
      :class="[
        modelValue === tab.id
          ? 'bg-white text-gray-900 shadow-sm ring-1 ring-gray-900/5'
          : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
      ]"
      @click="$emit('update:modelValue', tab.id)"
    >
      <span class="mr-2">{{ tab.icon }}</span>
      {{ tab.label }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  modelValue: { type: String, required: true },
  tabs: { type: Array, required: true }
})
defineEmits(['update:modelValue'])
</script>
