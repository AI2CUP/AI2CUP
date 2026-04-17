<template>
  <div class="section-panel bg-gradient-to-br from-white to-gray-50 !mb-0">
    <div class="flex items-center gap-3 mb-6">
      <div class="w-10 h-10 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center">
        🔍
      </div>
      <h3 class="font-bold text-gray-900 text-lg">Find {{ oppositeRoleText }}s</h3>
    </div>
    
    <form @submit.prevent="submit" class="space-y-4">
      <div>
        <label class="form-label text-xs uppercase tracking-wider font-semibold text-gray-500">I am a...</label>
        <div class="grid grid-cols-2 gap-2 mt-1">
          <button 
            type="button" 
            class="py-2 px-3 text-sm font-medium rounded-lg border transition-all"
            :class="form.role === 'buyer' ? 'bg-emerald-50 border-emerald-200 text-emerald-800 ring-1 ring-emerald-500' : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'"
            @click="form.role = 'buyer'"
          >
            Buyer looking for Coffee
          </button>
          <button 
            type="button" 
            class="py-2 px-3 text-sm font-medium rounded-lg border transition-all"
            :class="form.role === 'seller' ? 'bg-emerald-50 border-emerald-200 text-emerald-800 ring-1 ring-emerald-500' : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'"
            @click="form.role = 'seller'"
          >
            Seller looking for Buyers
          </button>
        </div>
      </div>
      
      <div class="border-t border-gray-100 pt-4 mt-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="form-label" for="regionFilter">Region Preference</label>
          <select v-model="form.region" class="form-select text-sm py-2" id="regionFilter">
            <option value="">Any Region</option>
            <option value="Yirgacheffe">Yirgacheffe</option>
            <option value="Sidamo">Sidamo</option>
            <option value="Harar">Harar</option>
            <option value="Jimma">Jimma</option>
            <option value="Limu">Limu</option>
            <option value="Guji">Guji</option>
          </select>
        </div>
        
        <div>
          <label class="form-label" for="qualityFilter">Min. Quality</label>
          <select v-model="form.quality" class="form-select text-sm py-2" id="qualityFilter">
             <option value="">Any Quality</option>
             <option value="High">High (Grade 1-2)</option>
             <option value="Medium">Medium (Grade 3-4)</option>
             <option value="Low">Low (Grade 5)</option>
          </select>
        </div>
      </div>
      
      <div class="pt-2">
        <AppButton 
          type="submit" 
          :loading="loading" 
          :text="`Find Top Matches`" 
          class="w-full"
        />
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue'
import AppButton from '../common/AppButton.vue'

const props = defineProps({
  loading: { type: Boolean, default: false }
})

const emit = defineEmits(['search'])

const form = reactive({
  role: 'buyer', // User's role seeking the opposite
  region: '',
  quality: ''
})

const oppositeRoleText = computed(() => form.role === 'buyer' ? 'Seller' : 'Buyer')

const submit = () => {
  // If the user is a buyer, they are looking for sellers to match with
  // The API '/match/find' expects the parameter 'role' to be the type of target entity we want it to return.
  const targetRole = form.role === 'buyer' ? 'seller' : 'buyer'
  
  emit('search', {
    role: targetRole,
    ...form.region ? { region: form.region } : {},
    ...form.quality ? { quality: form.quality } : {}
  })
}
</script>
