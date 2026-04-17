<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
        <span class="w-12 h-12 bg-indigo-100 text-indigo-600 rounded-xl flex items-center justify-center shadow-sm">🤝</span>
        Smart Marketplace · ስማርት ገበያ
      </h1>
      <p class="text-gray-600 text-lg max-w-3xl">
        AI-driven matching connects Ethiopian coffee cooperatives directly with international buyers based on matching profiles.
      </p>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      <!-- Left Sidebar: Filtering & Matchmaking Engine -->
      <div class="lg:col-span-4 self-start sticky top-24">
        <MatchFilter 
          :loading="isLoading"
          @search="handleMatchSearch"
        />
        
        <div v-if="!matches" class="mt-6 p-5 border border-blue-100 bg-blue-50/50 rounded-xl">
          <h4 class="font-medium text-blue-900 flex items-center gap-2 mb-2"><span class="text-lg">ℹ️</span> How it works</h4>
          <p class="text-sm text-blue-800/80 leading-relaxed">
            The AI considers regions, ECX grades, volume capacities, and certifications to score the best possible counterparties. 
            Adjust your profile to find better matches.
          </p>
        </div>
      </div>
      
      <!-- Right Main: Results Listing -->
      <div class="lg:col-span-8">
        <transition name="fade" mode="out-in">
          <!-- SEARCH RESULTS -->
          <div v-if="matches" :key="'matches'">
             <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-bold text-gray-900 flex items-center gap-2">
                  <span>🎯</span> Match Results
                </h2>
                <button @click="matches = null" class="text-sm text-gray-500 hover:text-emerald-600 font-medium">
                  Clear Search ✕
                </button>
             </div>
             
             <div v-if="matches.length === 0" class="flex flex-col items-center justify-center py-16 bg-white rounded-xl border border-gray-100 text-center">
                <span class="text-4xl mb-3 opacity-50">🕵️‍♀️</span>
                <h3 class="text-gray-900 font-medium mb-1">No perfect matches found</h3>
                <p class="text-gray-500 text-sm max-w-sm">Try broadening your search criteria (e.g. any region) to find more potential partners.</p>
             </div>
             
             <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                <ListingCard 
                  v-for="match in matches" 
                  :key="match.id" 
                  :entity="match" 
                  :role="lastSearchTargetRole" 
                />
             </div>
          </div>
          
          <!-- BROWSER VIEW (DEFAULT) -->
          <div v-else :key="'browse'">
            <div class="flex items-center justify-between mb-6">
               <h2 class="text-xl font-bold text-gray-900">Browse Directory</h2>
               <MarketTabs 
                 v-model="activeTab" 
                 :tabs="[
                   { id: 'sellers', label: 'Cooperatives', icon: '🇪🇹' },
                   { id: 'buyers', label: 'Importers', icon: '🌎' }
                 ]" 
                 class="w-auto mb-0"
               />
            </div>
            
            <div v-if="isListingsLoading" class="flex justify-center py-20">
              <LoadingSpinner class="w-8 h-8 text-emerald-500" />
            </div>
            
            <div v-else-if="allListings" class="grid grid-cols-1 sm:grid-cols-2 gap-5">
              <template v-if="activeTab === 'sellers'">
                <ListingCard 
                  v-for="seller in allListings.sellers" 
                  :key="seller.id" 
                  :entity="seller" 
                  role="seller" 
                />
              </template>
              <template v-else>
                <ListingCard 
                  v-for="buyer in allListings.buyers" 
                  :key="buyer.id" 
                  :entity="buyer" 
                  role="buyer" 
                />
              </template>
            </div>
            
            <div v-else class="py-12 text-center text-red-500 bg-red-50 rounded-xl">
               Failed to load marketplace data.
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MatchFilter from '../components/marketplace/MatchFilter.vue'
import MarketTabs from '../components/marketplace/MarketTabs.vue'
import ListingCard from '../components/marketplace/ListingCard.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import { matchService } from '../services/matchService'
import { useLoading } from '../composables/useLoading'
import { useToast } from '../composables/useToast'

const { isLoading, withLoading } = useLoading()
const toast = useToast()

const activeTab = ref('sellers')
const allListings = ref(null)
const isListingsLoading = ref(true)

const matches = ref(null)
const lastSearchTargetRole = ref(null)

onMounted(async () => {
  try {
    const data = await matchService.getListings()
    allListings.value = data
  } catch (err) {
    toast.error('Failed to connect to marketplace')
  } finally {
    isListingsLoading.value = false
  }
})

const handleMatchSearch = async (params) => {
  lastSearchTargetRole.value = params.role
  try {
    const res = await withLoading(() => matchService.findMatches(params))
    matches.value = res.matches
    toast.success(`Found ${res.total} matches`)
  } catch (err) {
    toast.error(err.message || 'Matching failed')
  }
}
</script>
