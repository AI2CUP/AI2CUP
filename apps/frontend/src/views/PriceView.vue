<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
        <span class="w-12 h-12 bg-blue-100 text-blue-600 rounded-xl flex items-center justify-center shadow-sm">📈</span>
        Coffee Price Prediction · የቡና ዋጋ ትንበያ
      </h1>
      <p class="text-gray-600 text-lg max-w-3xl">
        AI-predicted prices in ETB & USD based on ECX market factors, region, and coffee characteristics.
      </p>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      <div class="lg:col-span-5 xl:col-span-4">
        <div class="section-panel">
          <PriceForm 
            :loading="isLoading" 
            @submit="handlePredict" 
          />
        </div>
      </div>
      
      <div class="lg:col-span-7 xl:col-span-8">
        <transition name="fade" mode="out-in">
          <div v-if="result" :key="'result'">
            <PriceResult :result="result" />
            
            <div class="mt-8 section-panel">
              <h3 class="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <span>💡</span> Price Factors Analysis
              </h3>
              <p class="text-gray-600 text-sm mb-4">
                The ML model determined this price based on historical Ethiopian Commodity Exchange (ECX) data. 
                Values shown are synthetic for the MVP but accurately reflect Ethiopian market dynamics.
              </p>
              <ul class="space-y-2 text-sm text-gray-700">
                <li class="flex items-start gap-2">
                  <span class="text-emerald-500 mt-0.5">●</span>
                  <span><strong>Altitude & Quality:</strong> {{ result.inputs.altitude }}m enables complex flavor development, raising the base price.</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-emerald-500 mt-0.5">●</span>
                  <span><strong>Seasonality:</strong> Month {{ result.inputs.month }} is factored into the harvest cycle supply curve.</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-emerald-500 mt-0.5">●</span>
                  <span><strong>Processing:</strong> {{ result.inputs.processing }} method commands specific market premiums.</span>
                </li>
              </ul>
            </div>
          </div>
          
          <div v-else :key="'empty'" class="h-full min-h-[400px] flex flex-col items-center justify-center border-2 border-dashed border-gray-200 rounded-2xl bg-gray-50/50 p-8 text-center text-gray-500">
            <span class="text-5xl mb-4 opacity-50">🔮</span>
            <h3 class="text-lg font-medium text-gray-700 mb-2">Awaiting Prediction Parameters</h3>
            <p class="max-w-md text-sm">Adjust the region, variety, and grade settings and click Predict to see the AI estimated market value.</p>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import PriceForm from '../components/price/PriceForm.vue'
import PriceResult from '../components/price/PriceResult.vue'
import { priceService } from '../services/priceService'
import { useLoading } from '../composables/useLoading'
import { useToast } from '../composables/useToast'

const result = ref(null)
const { isLoading, withLoading } = useLoading()
const toast = useToast()

const handlePredict = async (params) => {
  try {
    result.value = await withLoading(() => priceService.predict(params))
    toast.success('Price predicted successfully')
  } catch (err) {
    toast.error(err.message || 'Failed to predict price')
  }
}
</script>
