<template>
  <div class="bg-emerald-50 rounded-xl p-6 border border-emerald-100">
    <div class="flex items-center gap-2 text-emerald-800 font-semibold mb-6">
      <span class="text-xl">✅</span>
      <span>Prediction Result · የትንበያ ውጤት</span>
    </div>
    
    <div class="flex flex-col md:flex-row items-center justify-center gap-6 md:gap-12 mb-6">
      <div class="text-center">
        <div class="text-4xl font-bold text-gray-900 mb-1">
          {{ formatPrice(result.predicted_price_etb) }} {{ result.currency_primary }}
        </div>
        <div class="text-gray-500 text-sm">Ethiopian Birr {{ result.unit }}</div>
      </div>
      
      <div class="hidden md:block text-2xl text-emerald-300 font-light">≈</div>
      
      <div class="text-center">
        <div class="text-4xl font-bold text-emerald-600 mb-1">
          ${{ formatPrice(result.predicted_price_usd) }}
        </div>
        <div class="text-gray-500 text-sm">US Dollars {{ result.unit }}</div>
      </div>
    </div>
    
    <div class="text-center mb-6">
      <span class="inline-block bg-white px-4 py-2 rounded-full text-emerald-700 font-semibold shadow-sm border border-emerald-100">
        {{ result.ecx_grade_label }}
      </span>
    </div>
    
    <div class="bg-white rounded-lg p-4 text-sm text-gray-600 grid grid-cols-2 md:grid-cols-4 gap-4 border border-emerald-50">
      <div>
        <span class="block text-gray-400 text-xs mb-1">Region</span>
        <span class="font-medium">{{ result.inputs.region }}</span>
      </div>
      <div>
        <span class="block text-gray-400 text-xs mb-1">Variety</span>
        <span class="font-medium">{{ result.inputs.variety }}</span>
      </div>
      <div>
        <span class="block text-gray-400 text-xs mb-1">Processing</span>
        <span class="font-medium">{{ result.inputs.processing }}</span>
      </div>
      <div>
        <span class="block text-gray-400 text-xs mb-1">Model</span>
        <span class="font-medium truncate" :title="result.model_info">{{ result.model_info.split(' ')[0] }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  result: { type: Object, required: true }
})

function formatPrice(value) {
  return Number(value).toFixed(2)
}
</script>
