<template>
  <form @submit.prevent="submit" class="grid grid-cols-1 md:grid-cols-2 gap-5">
    <div>
      <label class="form-label" for="regionSelect">Region · ክልል</label>
      <select v-model="form.region" class="form-select" id="regionSelect">
        <option value="Yirgacheffe">Yirgacheffe (ይርጋጨፌ)</option>
        <option value="Sidamo">Sidamo (ሲዳሞ)</option>
        <option value="Harar">Harar (ሐረር)</option>
        <option value="Jimma">Jimma (ጅማ)</option>
        <option value="Limu">Limu (ሊሙ)</option>
        <option value="Guji">Guji (ጉጂ)</option>
        <option value="Wellega">Wellega (ወለጋ)</option>
        <option value="Bench Maji">Bench Maji (ቤንች ማጂ)</option>
      </select>
    </div>
    
    <div>
      <label class="form-label" for="monthSelect">Month · ወር</label>
      <select v-model.number="form.month" class="form-select" id="monthSelect">
        <option v-for="m in 12" :key="m" :value="m">{{ getMonthName(m) }}</option>
      </select>
    </div>
    
    <div>
      <label class="form-label" for="altitudeInput">Altitude (m)</label>
      <input v-model.number="form.altitude" type="number" class="form-input" id="altitudeInput" min="1000" max="3000" step="50">
    </div>
    
    <div>
      <label class="form-label" for="rainfallInput">Rainfall (mm)</label>
      <input v-model.number="form.rainfall" type="number" class="form-input" id="rainfallInput" min="0" max="500" step="10">
    </div>
    
    <div>
      <label class="form-label" for="varietySelect">Variety · ዝርያ</label>
      <select v-model="form.variety" class="form-select" id="varietySelect">
        <option value="Heirloom">Heirloom (የአገር ቤት)</option>
        <option value="Typica">Typica</option>
        <option value="Bourbon">Bourbon</option>
        <option value="Gesha">Gesha (ገሻ)</option>
        <option value="74110">74110 (JARC)</option>
        <option value="74112">74112 (JARC)</option>
      </select>
    </div>
    
    <div>
      <label class="form-label" for="processingSelect">Processing</label>
      <select v-model="form.processing" class="form-select" id="processingSelect">
        <option value="Washed">Washed (ውኃ ያጠበ)</option>
        <option value="Natural">Natural / Sun-dried (ፀሐይ ያደረቀ)</option>
        <option value="Honey">Honey Process</option>
      </select>
    </div>
    
    <div class="md:col-span-2">
      <label class="form-label" for="ecxGradeSelect">ECX Grade · ደረጃ</label>
      <select v-model.number="form.ecx_grade" class="form-select" id="ecxGradeSelect">
        <option value="1">Grade 1 - Specialty (ልዩ)</option>
        <option value="2">Grade 2 - Very Good (በጣም ጥሩ)</option>
        <option value="3">Grade 3 - Good (ጥሩ)</option>
        <option value="4">Grade 4 - Commercial (ንግድ)</option>
        <option value="5">Grade 5 - Below Standard</option>
      </select>
    </div>
    
    <div class="md:col-span-2 mt-2">
      <AppButton 
        type="submit" 
        :loading="loading" 
        text="🔮 Predict Price · ዋጋ ተንብይ" 
      />
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import AppButton from '../common/AppButton.vue'

const props = defineProps({
  loading: { type: Boolean, default: false }
})

const emit = defineEmits(['submit'])

const form = reactive({
  region: 'Yirgacheffe',
  month: new Date().getMonth() + 1,
  altitude: 1800,
  rainfall: 120,
  variety: 'Heirloom',
  processing: 'Washed',
  ecx_grade: 3
})

const monthNames = [
  'January (ጥር)', 'February (የካቲት)', 'March (መጋቢት)', 'April (ሚያዝያ)',
  'May (ግንቦት)', 'June (ሰኔ)', 'July (ሐምሌ)', 'August (ነሐሴ)',
  'September (መስከረም)', 'October (ጥቅምት)', 'November (ህዳር)', 'December (ታህሳስ)'
]

function getMonthName(m) {
  return monthNames[m - 1]
}

function submit() {
  emit('submit', { ...form })
}
</script>
