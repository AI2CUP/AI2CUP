<template>
  <div class="card p-0 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 overflow-hidden">
    <!-- Grade indicator bar -->
    <div class="h-1" :class="gradeColorClass"></div>

    <div class="p-5">
      <!-- Header -->
      <div class="flex items-start justify-between gap-3 mb-3">
        <div class="flex-1 min-w-0">
          <h3 class="font-bold text-gray-900 text-base leading-snug truncate">{{ listing.title }}</h3>
          <p v-if="listing.description" class="text-xs text-gray-500 mt-1 line-clamp-2">{{ listing.description }}</p>
        </div>
        <AppBadge :color="gradeBadgeColor">
          {{ listing.ecx_grade > 0 ? `Grade ${listing.ecx_grade}` : 'No Grade' }}
        </AppBadge>
      </div>

      <!-- Details Grid -->
      <div class="grid grid-cols-2 gap-y-3 gap-x-4 mb-4">
        <div>
          <span class="block text-xs text-gray-400 font-medium mb-0.5">Region</span>
          <span class="text-sm font-medium text-gray-800">{{ listing.region }}</span>
        </div>
        <div>
          <span class="block text-xs text-gray-400 font-medium mb-0.5">Volume</span>
          <span class="text-sm font-medium text-gray-800">{{ listing.available_kg.toLocaleString() }} kg</span>
        </div>
        <div>
          <span class="block text-xs text-gray-400 font-medium mb-0.5">Price (ETB)</span>
          <span class="text-sm font-medium text-gray-800">{{ listing.price_per_kg_etb }} / kg</span>
        </div>
        <div>
          <span class="block text-xs text-gray-400 font-medium mb-0.5">Price (USD)</span>
          <span class="text-sm font-medium text-amber-700">${{ listing.price_per_kg_usd.toFixed(2) }}</span>
        </div>
      </div>

      <!-- Tags -->
      <div class="flex flex-wrap gap-1.5 mb-4" v-if="listing.variety || listing.processing || listing.certification">
        <span v-if="listing.variety" class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md">{{ listing.variety }}</span>
        <span v-if="listing.processing" class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md">{{ listing.processing }}</span>
        <span v-if="listing.certification" class="text-xs bg-amber-50 text-amber-700 px-2 py-0.5 rounded-md font-medium">{{ listing.certification }}</span>
      </div>

      <!-- Contact -->
      <div class="pt-3 border-t border-gray-100">
        <div class="flex items-center gap-2 text-xs text-gray-500 mb-1.5">
          <svg class="w-3.5 h-3.5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <span class="font-medium text-gray-700 truncate">{{ listing.contact_name }}</span>
        </div>
        <div class="flex flex-wrap gap-3">
          <a v-if="listing.contact_phone" :href="'tel:' + listing.contact_phone" class="flex items-center gap-1 text-xs text-gray-500 hover:text-amber-700 transition-colors">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
            {{ listing.contact_phone }}
          </a>
          <a v-if="listing.contact_email" :href="'mailto:' + listing.contact_email" class="flex items-center gap-1 text-xs text-gray-500 hover:text-amber-700 transition-colors">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
            {{ listing.contact_email }}
          </a>
        </div>
      </div>
    </div>

    <!-- Timestamp footer -->
    <div v-if="listing.created_at" class="px-5 py-2 bg-gray-50 text-xs text-gray-400">
      Posted {{ formatDate(listing.created_at) }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import AppBadge from '../common/AppBadge.vue'

const props = defineProps({
  listing: { type: Object, required: true },
})

const gradeColorClass = computed(() => {
  const g = props.listing.ecx_grade
  if (g === 0) return 'bg-gray-300'
  if (g <= 1) return 'bg-emerald-500'
  if (g <= 2) return 'bg-emerald-400'
  if (g <= 3) return 'bg-blue-400'
  return 'bg-orange-400'
})

const gradeBadgeColor = computed(() => {
  const g = props.listing.ecx_grade
  if (g === 0) return 'gray'
  if (g <= 2) return 'emerald'
  if (g <= 3) return 'blue'
  return 'orange'
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const now = new Date()
  const diffMs = now - d
  const diffH = Math.floor(diffMs / 3600000)
  if (diffH < 1) return 'just now'
  if (diffH < 24) return `${diffH}h ago`
  const diffD = Math.floor(diffH / 24)
  if (diffD < 7) return `${diffD}d ago`
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>
