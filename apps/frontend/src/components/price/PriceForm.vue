<template>
  <form @submit.prevent="submit" class="grid grid-cols-1 md:grid-cols-2 gap-5">
    <div class="md:col-span-2">
      <label class="form-label" for="coffeeTypeSelect">Coffee Type · የቡና አይነት</label>
      <select v-model="form.coffee_type" class="form-select" id="coffeeTypeSelect">
        <optgroup v-for="group in COFFEE_TYPES" :key="group.label" :label="group.label">
          <option v-for="opt in group.options" :key="opt" :value="opt">{{ opt }}</option>
        </optgroup>
      </select>
    </div>

    <div>
      <label class="form-label" for="yearInput">Year · ዓመት</label>
      <input v-model.number="form.year" type="number" class="form-input" id="yearInput" min="2024" max="2030">
    </div>

    <div>
      <label class="form-label" for="monthSelect">Month · ወር</label>
      <select v-model.number="form.month" class="form-select" id="monthSelect">
        <option v-for="m in 12" :key="m" :value="m">{{ getMonthName(m) }}</option>
      </select>
    </div>

    <div>
      <label class="form-label" for="weekInput">Week (optional) · ሳምንት</label>
      <input v-model.number="form.week" type="number" class="form-input" id="weekInput" min="1" max="53" placeholder="e.g. 26">
    </div>

    <div>
      <label class="form-label" for="processingSelect">Processing · አሰራር</label>
      <select v-model="form.processing" class="form-select" id="processingSelect">
        <option v-for="p in PROCESSING_METHODS" :key="p" :value="p">{{ p }}</option>
      </select>
    </div>

    <div>
      <label class="form-label" for="ecxGradeSelect">ECX Grade · ደረጃ</label>
      <select v-model.number="form.ecx_grade" class="form-select" id="ecxGradeSelect">
        <option v-for="g in ECX_GRADES" :key="g.value" :value="g.value">{{ g.label }}</option>
      </select>
    </div>

    <div>
      <label class="form-label" for="exporterTypeSelect">Exporter Type · ላኪ አይነት</label>
      <select v-model="form.exporter_type" class="form-select" id="exporterTypeSelect">
        <option v-for="e in EXPORTER_TYPES" :key="e" :value="e">{{ e }}</option>
      </select>
    </div>

    <div class="md:col-span-2 mt-2">
      <AppButton
        type="submit"
        :loading="loading"
        text="Predict Price · ዋጋ ተንብይ"
      />
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import AppButton from '../common/AppButton.vue'
import {
  COFFEE_TYPES,
  PROCESSING_METHODS,
  EXPORTER_TYPES,
  ECX_GRADES,
} from '../../constants/coffeeTypes.js'

defineProps({
  loading: { type: Boolean, default: false }
})

const emit = defineEmits(['submit'])

const form = reactive({
  coffee_type: 'Yirgachefe',
  year: new Date().getFullYear(),
  month: new Date().getMonth() + 1,
  week: null,
  processing: 'Washed',
  ecx_grade: 3,
  exporter_type: 'Commercial',
})

const monthNames = [
  'January (ጥር)', 'February (የካቲት)', 'March (መጋቢት)', 'April (ሚያዝያ)',
  'May (ግንቦት)', 'June (ሰኔ)', 'July (ሐምሌ)', 'August (ነሐሴ)',
  'September (መስከረም)', 'October (ጥቅምት)', 'November (ህዳር)', 'December (ታህሳስ)',
]

function getMonthName(m) {
  return monthNames[m - 1]
}

function submit() {
  emit('submit', { ...form })
}
</script>
