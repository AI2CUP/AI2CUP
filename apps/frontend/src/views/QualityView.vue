<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
        <span class="w-12 h-12 bg-amber-100 text-amber-600 rounded-xl flex items-center justify-center shadow-sm">🔬</span>
        Quality Detection · የጥራት ምርመራ
      </h1>
      <p class="text-gray-600 text-lg max-w-3xl">
        Upload photos of green coffee beans to automatically assess their ECX Grade and export eligibility using computer vision.
      </p>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Left side: Form -->
      <div class="flex flex-col gap-6">
        <div class="section-panel !mb-0 h-full flex flex-col">
          <h3 class="font-semibold text-gray-800 mb-4">Upload Bean Sample Image</h3>
          
          <ImageUploader 
            class="flex-1 mb-6"
            @file-selected="onFileSelected"
            @cleared="onFileCleared"
          />
          
          <AppButton 
            class="w-full"
            :disabled="!selectedFile"
            :loading="isLoading"
            text="🔍 Analyze Quality · ጥራት መርምር"
            @click="handleAnalyze"
          />
        </div>
      </div>
      
      <!-- Right side: Results -->
      <div>
        <transition name="fade" mode="out-in">
          <div v-if="result" :key="'result'">
            <QualityResult :result="result" />
          </div>
          
          <div v-else :key="'empty'" class="h-full min-h-[400px] flex flex-col items-center justify-center border-2 border-dashed border-gray-200 rounded-2xl bg-white p-8 text-center text-gray-500 shadow-sm relative overflow-hidden">
            <!-- Decorative background elements -->
            <div class="absolute -right-10 -top-10 text-9xl opacity-5 pointer-events-none">☕</div>
            <div class="absolute -left-10 -bottom-10 text-9xl opacity-5 pointer-events-none">🔬</div>
            
            <div class="relative z-10 flex flex-col items-center max-w-sm mx-auto">
              <span class="text-5xl mb-6 opacity-30 drop-shadow-sm">📷</span>
              <h3 class="text-xl font-semibold text-gray-800 mb-3">ECX Quality Analysis</h3>
              <p class="text-gray-500 text-sm leading-relaxed mb-6">
                Our AI model evaluates color uniformity, brightness, warmth, and defect indicators to estimate structural bean quality.
              </p>
              
              <div class="w-full bg-gray-50 rounded-lg p-4 border border-gray-100 text-left">
                <span class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Instructions:</span>
                <ul class="text-sm text-gray-600 space-y-2">
                  <li class="flex items-center gap-2"><span class="text-emerald-500">✓</span> Good lighting (bright, indirect)</li>
                  <li class="flex items-center gap-2"><span class="text-emerald-500">✓</span> High contrast background</li>
                  <li class="flex items-center gap-2"><span class="text-emerald-500">✓</span> Single layer of beans</li>
                </ul>
              </div>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppButton from '../components/common/AppButton.vue'
import ImageUploader from '../components/quality/ImageUploader.vue'
import QualityResult from '../components/quality/QualityResult.vue'
import { qualityService } from '../services/qualityService'
import { useLoading } from '../composables/useLoading'
import { useToast } from '../composables/useToast'

const selectedFile = ref(null)
const result = ref(null)
const { isLoading, withLoading } = useLoading()
const toast = useToast()

const onFileSelected = (file) => {
  selectedFile.value = file
  result.value = null // reset prior results when a new image is added
}

const onFileCleared = () => {
  selectedFile.value = null
  result.value = null
}

const handleAnalyze = async () => {
  if (!selectedFile.value) return
  
  try {
    result.value = await withLoading(() => qualityService.analyze(selectedFile.value))
    toast.success('Analysis complete')
  } catch (err) {
    toast.error(err.message || 'Analysis failed')
  }
}
</script>
