<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-2xl mx-auto">
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <!-- Header -->
        <div class="bg-amber-600 px-8 py-8 text-white">
          <router-link to="/marketplace" class="inline-flex items-center gap-1 text-amber-100 hover:text-white text-sm mb-4 transition-colors">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back to Marketplace
          </router-link>
          <h1 class="text-2xl font-bold">Post a Coffee Listing</h1>
          <p class="text-amber-100 mt-1 text-sm">Share your available coffee lots with buyers worldwide</p>
        </div>

        <!-- Form -->
        <div class="p-8">
          <transition name="slide-fade">
            <div v-if="error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl flex items-center gap-3">
              <span class="text-red-500 text-lg">⚠️</span>
              <p class="text-red-700 text-sm font-medium">{{ error }}</p>
            </div>
          </transition>

          <form @submit.prevent="handleSubmit" class="space-y-6">
            <!-- Region & Grade -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label for="listing-region" class="block text-sm font-semibold text-gray-700 mb-1.5">Region</label>
                <select id="listing-region" v-model="form.region" required class="form-select">
                  <option value="" disabled>Select region</option>
                  <option value="Yirgacheffe">Yirgacheffe</option>
                  <option value="Sidamo">Sidamo</option>
                  <option value="Harar">Harar</option>
                  <option value="Jimma">Jimma</option>
                  <option value="Limu">Limu</option>
                  <option value="Guji">Guji</option>
                  <option value="Wellega">Wellega</option>
                  <option value="Bench Maji">Bench Maji</option>
                  <option value="Unknown">Unknown (ያልታወቀ)</option>
                </select>
              </div>
              <div>
                <label for="listing-grade" class="block text-sm font-semibold text-gray-700 mb-1.5">ECX Grade</label>
                <select id="listing-grade" v-model.number="form.ecx_grade" required class="form-select">
                  <option value="" disabled>Select grade</option>
                  <option :value="1">Grade 1</option>
                  <option :value="2">Grade 2</option>
                  <option :value="3">Grade 3</option>
                  <option :value="4">Grade 4</option>
                  <option :value="5">Grade 5</option>
                  <option :value="0">None (ደረጃ የለውም)</option>
                </select>
              </div>
            </div>

            <!-- Variety & Processing -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label for="listing-variety" class="block text-sm font-semibold text-gray-700 mb-1.5">Variety <span class="text-gray-400 font-normal">(optional)</span></label>
                <select id="listing-variety" v-model="form.variety" class="form-select">
                  <option value="">Select variety</option>
                  <option value="Heirloom">Heirloom (የአገር ቤት)</option>
                  <option value="Typica">Typica</option>
                  <option value="Bourbon">Bourbon</option>
                  <option value="Gesha">Gesha (ገሻ)</option>
                  <option value="74110">74110 (JARC)</option>
                  <option value="74112">74112 (JARC)</option>
                  <option value="Unknown">Unknown (ያልታወቀ)</option>
                </select>
              </div>
              <div>
                <label for="listing-processing" class="block text-sm font-semibold text-gray-700 mb-1.5">Processing <span class="text-gray-400 font-normal">(optional)</span></label>
                <select id="listing-processing" v-model="form.processing" class="form-select">
                  <option value="">Select processing</option>
                  <option value="Washed">Washed</option>
                  <option value="Natural">Natural</option>
                  <option value="Honey">Honey</option>
                </select>
              </div>
            </div>

            <!-- Pricing -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label for="listing-etb" class="block text-sm font-semibold text-gray-700 mb-1.5">Price (ETB/kg)</label>
                <input id="listing-etb" v-model.number="form.price_per_kg_etb" type="number" step="0.01" min="0" required placeholder="380" class="w-full px-4 py-3 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500/40 focus:border-amber-500 transition-all bg-gray-50/50 hover:bg-white" />
              </div>
              <div>
                <label for="listing-vol" class="block text-sm font-semibold text-gray-700 mb-1.5">Available (kg)</label>
                <input id="listing-vol" v-model.number="form.available_kg" type="number" min="1" required placeholder="10000" class="w-full px-4 py-3 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500/40 focus:border-amber-500 transition-all bg-gray-50/50 hover:bg-white" />
              </div>
            </div>

            <!-- Description -->
            <div>
              <label for="listing-desc" class="block text-sm font-semibold text-gray-700 mb-1.5">Description <span class="text-gray-400 font-normal">(optional)</span></label>
              <textarea id="listing-desc" v-model="form.description" rows="3" placeholder="Describe your coffee lot, cupping notes, harvest year, etc." class="w-full px-4 py-3 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500/40 focus:border-amber-500 transition-all bg-gray-50/50 hover:bg-white resize-none"></textarea>
            </div>

            <!-- Certification -->
            <div>
              <label for="listing-cert" class="block text-sm font-semibold text-gray-700 mb-1.5">Certifications <span class="text-gray-400 font-normal">(optional)</span></label>
              <input id="listing-cert" v-model="form.certification" type="text" placeholder="e.g. Organic, Fair Trade, Rainforest Alliance" class="w-full px-4 py-3 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500/40 focus:border-amber-500 transition-all bg-gray-50/50 hover:bg-white" />
            </div>

            <div class="border-t border-gray-100 pt-6">
              <h3 class="text-sm font-semibold text-gray-900 mb-4">Contact Information</h3>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label for="listing-cname" class="block text-sm font-semibold text-gray-700 mb-1.5">Name</label>
                  <input id="listing-cname" v-model="form.contact_name" type="text" required placeholder="Your name" class="w-full px-4 py-3 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500/40 focus:border-amber-500 transition-all bg-gray-50/50 hover:bg-white" />
                </div>
                <div>
                  <label for="listing-cphone" class="block text-sm font-semibold text-gray-700 mb-1.5">Phone</label>
                  <input id="listing-cphone" v-model="form.contact_phone" type="tel" placeholder="+251 911..." class="w-full px-4 py-3 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500/40 focus:border-amber-500 transition-all bg-gray-50/50 hover:bg-white" />
                </div>
                <div>
                  <label for="listing-cemail" class="block text-sm font-semibold text-gray-700 mb-1.5">Email</label>
                  <input id="listing-cemail" v-model="form.contact_email" type="email" placeholder="you@example.com" class="w-full px-4 py-3 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500/40 focus:border-amber-500 transition-all bg-gray-50/50 hover:bg-white" />
                </div>
              </div>
            </div>

            <!-- Submit -->
            <div class="pt-4 flex justify-end gap-3 border-t border-gray-100">
              <router-link to="/marketplace" class="px-6 py-3 text-gray-600 hover:text-gray-900 font-medium transition-colors">
                Cancel
              </router-link>
              <button
                type="submit"
                :disabled="submitting"
                class="px-8 py-3 bg-amber-600 hover:bg-amber-700 active:bg-amber-800 text-white font-semibold rounded-xl shadow-md shadow-amber-500/25 hover:shadow-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none flex items-center justify-center gap-2"
              >
                <svg v-if="submitting" class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                <span>{{ submitting ? 'Posting...' : 'Post Listing' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { listingService } from '../services/listingService'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const submitting = ref(false)
const error = ref('')

const form = reactive({
  description: '',
  region: '',
  ecx_grade: '',
  variety: '',
  processing: '',
  price_per_kg_etb: null,
  available_kg: null,
  certification: '',
  contact_name: '',
  contact_phone: '',
  contact_email: '',
})

onMounted(() => {
  // Pre-fill contact info from user profile
  if (authStore.user) {
    form.contact_name = authStore.user.full_name || ''
    form.contact_phone = authStore.user.phone_number || ''
    form.contact_email = authStore.user.email || ''
  }
})

async function handleSubmit() {
  error.value = ''
  submitting.value = true

  try {
    await listingService.createListing(form)
    toast.success('Listing posted successfully!')
    router.push('/marketplace')
  } catch (err) {
    const detail = err.response?.data?.detail
    error.value = Array.isArray(detail)
      ? detail.map(d => d.msg).join(', ')
      : detail || err.message || 'Failed to post listing'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
</style>
