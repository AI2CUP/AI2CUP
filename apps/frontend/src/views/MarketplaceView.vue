<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">
          Coffee Marketplace · የቡና ገበያ
        </h1>
        <p class="text-gray-600 text-lg max-w-2xl">
          Browse available Ethiopian coffee lots from suppliers and exporters across the country.
        </p>
      </div>
      <router-link
        v-if="authStore.isAuthenticated"
        to="/marketplace/create"
        class="shrink-0 inline-flex items-center gap-2 bg-amber-600 hover:bg-amber-700 text-white font-semibold py-3 px-6 rounded-xl shadow-md hover:shadow-lg transition-all"
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Post a Listing
      </router-link>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      <!-- Filters Sidebar -->
      <div class="lg:col-span-3 self-start lg:sticky lg:top-24">
        <div class="section-panel bg-gradient-to-br from-white to-gray-50 !mb-0">
          <h3 class="font-bold text-gray-900 text-lg mb-5">Filter Listings</h3>

          <div class="space-y-4">
            <div>
              <label class="form-label text-xs uppercase tracking-wider font-semibold text-gray-500" for="filterRegion">Region</label>
              <select v-model="filters.region" class="form-select text-sm py-2" id="filterRegion" @change="fetchListings">
                <option value="">All Regions</option>
                <option value="Yirgacheffe">Yirgacheffe</option>
                <option value="Sidamo">Sidamo</option>
                <option value="Harar">Harar</option>
                <option value="Jimma">Jimma</option>
                <option value="Limu">Limu</option>
                <option value="Guji">Guji</option>
                <option value="Wellega">Wellega</option>
                <option value="Bench Maji">Bench Maji</option>
                <option value="Unknown">Unknown</option>
              </select>
            </div>

            <div>
              <label class="form-label text-xs uppercase tracking-wider font-semibold text-gray-500" for="filterGrade">Max ECX Grade</label>
              <select v-model="filters.max_grade" class="form-select text-sm py-2" id="filterGrade" @change="fetchListings">
                <option value="">Any Grade</option>
                <option value="1">Grade 1 (Top)</option>
                <option value="2">Grade 1–2</option>
                <option value="3">Grade 1–3</option>
                <option value="4">Grade 1–4</option>
                <option value="0">No Grade (None)</option>
              </select>
            </div>

            <button
              v-if="filters.region || filters.max_grade"
              @click="clearFilters"
              class="text-sm text-amber-700 hover:text-amber-900 font-medium transition-colors"
            >
              Clear Filters
            </button>
          </div>
        </div>

        <div v-if="!authStore.isAuthenticated" class="mt-6 p-5 border border-amber-100 bg-amber-50/50 rounded-xl">
          <h4 class="font-medium text-amber-900 mb-2">Are you a supplier?</h4>
          <p class="text-sm text-amber-800/80 leading-relaxed mb-3">
            Create an account to post your coffee listings and connect with buyers worldwide.
          </p>
          <router-link to="/register" class="text-sm font-semibold text-amber-700 hover:text-amber-900 transition-colors">
            Create Account →
          </router-link>
        </div>
      </div>

      <!-- Listings Grid -->
      <div class="lg:col-span-9">
        <div v-if="loading" class="flex justify-center py-20">
          <LoadingSpinner class="w-8 h-8 text-amber-500" />
        </div>

        <div v-else-if="listings.length > 0">
          <div class="flex items-center justify-between mb-5">
            <p class="text-sm text-gray-500">{{ listings.length }} listing{{ listings.length !== 1 ? 's' : '' }} found</p>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
            <ListingCard
              v-for="listing in listings"
              :key="listing.id"
              :listing="listing"
            />
          </div>
        </div>

        <div v-else class="flex flex-col items-center justify-center py-20 bg-white rounded-2xl border-2 border-dashed border-gray-200 text-center">
          <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-2.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
            </svg>
          </div>
          <h3 class="text-gray-900 font-medium mb-1">No listings found</h3>
          <p class="text-gray-500 text-sm max-w-sm">Try adjusting your filters, or check back later for new listings.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import ListingCard from '../components/marketplace/ListingCard.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import { listingService } from '../services/listingService'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'

const authStore = useAuthStore()
const toast = useToast()
const loading = ref(true)
const listings = ref([])

const filters = reactive({
  region: '',
  max_grade: '',
})

async function fetchListings() {
  loading.value = true
  try {
    listings.value = await listingService.getListings(filters)
  } catch (err) {
    toast.error('Failed to load listings')
  } finally {
    loading.value = false
  }
}

function clearFilters() {
  filters.region = ''
  filters.max_grade = ''
  fetchListings()
}

onMounted(fetchListings)
</script>
