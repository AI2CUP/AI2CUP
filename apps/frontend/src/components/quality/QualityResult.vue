<template>
  <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
    <div class="p-6 border-b border-gray-100" :class="ecxInfo.color">
      <div class="flex items-start justify-between">
        <div>
          <div class="flex items-center gap-2 mb-1">
            <span class="text-sm font-bold uppercase tracking-wider opacity-80">Final Grade</span>
          </div>
          <h2 class="text-3xl font-bold flex items-center gap-3">
            {{ result.ecx_grade }} - {{ result.ecx_label }}
            <span class="text-2xl opacity-90">{{ result.ecx_amharic }}</span>
          </h2>
        </div>
        
        <div v-if="result.export_eligible" class="bg-white/20 px-3 py-1 rounded-full text-sm font-semibold flex items-center gap-1">
          🌍 Export Eligible
        </div>
        <div v-else class="bg-black/10 px-3 py-1 rounded-full text-sm font-semibold flex items-center gap-1">
          🇪🇹 Domestic Only
        </div>
      </div>
    </div>
    
    <div class="p-6">
      <p class="text-gray-700 text-lg mb-8 leading-relaxed">
        {{ result.description }}
      </p>
      
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
        <div class="bg-gray-50 p-4 rounded-xl border border-gray-100">
          <span class="block text-gray-500 text-xs uppercase tracking-wider font-semibold mb-1">Defect Assessment</span>
          <span class="font-medium text-gray-900">{{ result.defect_count }}</span>
        </div>
        
        <div class="bg-gray-50 p-4 rounded-xl border border-gray-100">
          <span class="block text-gray-500 text-xs uppercase tracking-wider font-semibold mb-1">Est. SCAA Score</span>
          <span class="font-medium text-gray-900">{{ result.scaa_score_range }}</span>
        </div>
      </div>
      
      <div class="space-y-5">
        <h3 class="font-semibold text-gray-900 text-sm uppercase tracking-wider mb-2">AI Analysis Metrics</h3>
        
        <ConfidenceBar 
          label="Overall Confidence" 
          :score="result.confidence" 
        />
        
        <ConfidenceBar 
          label="Color Uniformity" 
          :score="result.details.color_uniformity" 
        />
        
        <ConfidenceBar 
          label="Warmth Index (Drying Quality)" 
          :score="result.details.warmth_index" 
        />
        
        <div class="text-xs text-gray-400 text-right mt-2">
          Image size: {{ result.details.image_size }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import ConfidenceBar from '../common/ConfidenceBar.vue'
import { useEcxGrades } from '../../composables/useEcxGrades'

const props = defineProps({
  result: { type: Object, required: true }
})

const { getGradeInfo } = useEcxGrades()

const ecxInfo = computed(() => {
  return getGradeInfo(props.result.ecx_grade)
})
</script>
