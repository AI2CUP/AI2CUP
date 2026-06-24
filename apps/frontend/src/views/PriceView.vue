<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">
        Coffee Price Prediction · የቡና ዋጋ ትንበያ
      </h1>
      <p class="text-gray-600 text-lg max-w-3xl">
        AI-predicted prices in USD & ETB based on ECX market data, coffee type,
        grade, processing method, and exporter type.
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
              <h3 class="font-semibold text-gray-800 mb-4">
                Price Factors Analysis
              </h3>
              <p class="text-gray-600 text-sm mb-4">
                Prices are predicted by a HistGradientBoosting model trained on
                25,000+ real weekly export records from the Ethiopian Coffee
                Organization (ECO). Key pricing factors:
              </p>
              <ul class="space-y-2 text-sm text-gray-700">
                <li class="flex items-start gap-2">
                  <span class="text-emerald-500 mt-0.5">●</span>
                  <span><strong>Coffee Type:</strong> {{ result.inputs.coffee_type }} commands a specific market premium based on its origin reputation and cup profile.</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-emerald-500 mt-0.5">●</span>
                  <span><strong>ECX Grade:</strong> Grade {{ result.inputs.ecx_grade }} affects defect tolerance and export eligibility, directly influencing international pricing.</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-emerald-500 mt-0.5">●</span>
                  <span><strong>Processing Method:</strong> {{ result.inputs.processing }} method impacts flavor profile and production cost, with Naturals typically commanding a premium over Washed.</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-emerald-500 mt-0.5">●</span>
                  <span><strong>Seasonality:</strong> Month {{ result.inputs.month }} captures harvest cycle supply dynamics — prices tend to be higher early in the season.</span>
                </li>
              </ul>
            </div>
          </div>

          <div v-else :key="'empty'" class="h-full min-h-[400px] flex flex-col items-center justify-center border-2 border-dashed border-gray-200 rounded-2xl bg-gray-50/50 p-8 text-center text-gray-500">
            <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mb-6">
              <svg class="w-10 h-10 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="text-lg font-medium text-gray-700 mb-2">Awaiting Prediction Parameters</h3>
            <p class="max-w-md text-sm">Select coffee type, grade, and processing preferences and click Predict to see the AI estimated market value.</p>
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
