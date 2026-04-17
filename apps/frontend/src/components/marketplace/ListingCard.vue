<template>
  <div class="card p-0 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
    <div class="p-5 border-b border-gray-100 flex items-start justify-between bg-white relative overflow-hidden">
      <!-- Decorator line based on quality -->
      <div class="absolute top-0 left-0 w-full h-1" :class="qualityColorClass"></div>
      
      <div>
        <div class="flex items-center gap-2 mb-1">
          <AppBadge customClass="uppercase tracking-wider" :color="roleColor">{{ roleText }}</AppBadge>
          <span class="text-xs text-gray-400 flex items-center gap-1">
            <span>{{ isSeller ? '🇪🇹' : entity.country.slice(-2) }}</span>
            {{ entity.region || entity.preferred_region || 'Any Region' }}
          </span>
        </div>
        <h3 class="font-bold text-gray-900 text-lg group-hover:text-emerald-600 transition-colors">{{ entity.name }}</h3>
        <p v-if="entity.name_amharic" class="text-xs text-emerald-700/80">{{ entity.name_amharic }}</p>
      </div>
      
      <div v-if="entity.match_score !== undefined" class="flex flex-col items-end">
        <div class="relative w-12 h-12 flex items-center justify-center">
          <svg class="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
            <path
              class="text-gray-100"
              stroke-dasharray="100, 100"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              fill="none" stroke="currentColor" stroke-width="3"
            />
            <path
              :class="matchScoreColorClass"
              :stroke-dasharray="`${entity.match_score}, 100`"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"
            />
          </svg>
          <div class="absolute inset-0 flex items-center justify-center flex-col">
            <span class="text-xs font-bold text-gray-700">{{ entity.match_score }}</span>
          </div>
        </div>
        <span class="text-[0.6rem] uppercase tracking-wider text-gray-400 mt-1 font-semibold">Match</span>
      </div>
      <div v-else class="flex flex-col items-center justify-center w-12 h-12 bg-gray-50 rounded-full border border-gray-100 font-bold text-gray-400 group-hover:text-emerald-500 group-hover:bg-emerald-50 group-hover:border-emerald-200 transition-colors">
        {{ entity.rating.toFixed(1) }}
        <span class="text-[0.5rem] mt-[-2px]">★</span>
      </div>
    </div>
    
    <div class="p-5 grid grid-cols-2 gap-y-4 gap-x-2 bg-gray-50/50">
      <div>
        <span class="block text-xs text-gray-500 font-medium mb-1">Quality</span>
        <div class="flex items-center gap-1.5">
          <AppBadge :color="qualityBgRole">Grade {{ entity.ecx_grade || entity.max_ecx_grade }}</AppBadge>
        </div>
      </div>
      
      <div>
        <span class="block text-xs text-gray-500 font-medium mb-1">Volume</span>
        <div class="font-medium text-gray-900 text-sm">
          {{ (entity.available_kg || entity.volume_needed_kg).toLocaleString() }} kg
        </div>
      </div>
      
      <div>
        <span class="block text-xs text-gray-500 font-medium mb-1">Price (ETB)</span>
        <div class="font-medium text-gray-900 text-sm">
          {{ entity.price_per_kg_etb || entity.max_price_per_kg_etb }} / kg
        </div>
      </div>
      
      <div>
        <span class="block text-xs text-gray-500 font-medium mb-1">Price (USD)</span>
        <div class="font-medium text-emerald-600 text-sm">
          ${{ (entity.price_per_kg_usd || entity.max_price_per_kg_usd).toFixed(2) }}
        </div>
      </div>
    </div>
    
    <div v-if="entity.match_reasons && entity.match_reasons.length > 0" class="px-5 py-3 bg-emerald-50/50 border-t border-emerald-100 flex items-start gap-2">
      <span class="text-emerald-600 text-sm mt-0.5">✨</span>
      <div class="flex flex-wrap gap-1">
        <span v-for="(reason, i) in entity.match_reasons" :key="i" class="text-xs font-medium text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-md">
          {{ reason }}
        </span>
      </div>
    </div>
    <div v-else-if="entity.certification && entity.certification.length > 0" class="px-5 py-3 border-t border-gray-100 flex items-center gap-2">
      <span class="text-blue-500 text-sm">🔖</span>
      <div class="text-xs text-gray-600 truncate flex-1 font-medium">
        {{ entity.certification.join(', ') }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import AppBadge from '../common/AppBadge.vue'

const props = defineProps({
  entity: { type: Object, required: true },
  role: { type: String, required: true } // 'seller' or 'buyer'
})

const isSeller = computed(() => props.role === 'seller')
const roleText = computed(() => isSeller.value ? 'Cooperative' : 'Importer')
const roleColor = computed(() => isSeller.value ? 'emerald' : 'blue')

const qualityBgRole = computed(() => {
  const grade = props.entity.ecx_grade || props.entity.max_ecx_grade
  if (grade === 1) return 'emerald'
  if (grade === 2) return 'emerald'
  if (grade === 3) return 'blue'
  if (grade === 4) return 'orange'
  return 'gray'
})

const qualityColorClass = computed(() => {
  const grade = props.entity.ecx_grade || props.entity.max_ecx_grade
  if (grade === 1) return 'bg-emerald-500'
  if (grade === 2) return 'bg-emerald-400'
  if (grade === 3) return 'bg-blue-400'
  return 'bg-orange-400'
})

const matchScoreColorClass = computed(() => {
  const score = props.entity.match_score
  if (!score) return 'text-gray-300'
  if (score >= 80) return 'text-emerald-500'
  if (score >= 60) return 'text-blue-500'
  return 'text-yellow-500'
})
</script>
