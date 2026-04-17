<template>
  <div class="card p-5 md:p-6 transition-all hover:shadow-md">
    <div v-if="title || $slots.header" class="flex items-center gap-3 mb-4 pb-3 border-b border-gray-100">
      <slot name="icon">
        <span v-if="icon" class="text-xl">{{ icon }}</span>
      </slot>
      <h3 v-if="title" class="font-semibold text-gray-900 m-0">{{ title }}</h3>
      <slot name="header"></slot>
    </div>
    
    <div class="mt-2">
      <slot></slot>
    </div>
    
    <div v-if="$slots.footer" class="mt-5 pt-4 border-t border-gray-50 flex justify-between items-center text-sm">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: '' },
  icon: { type: String, default: '' }
})
</script>
