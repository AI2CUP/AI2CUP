<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">My Listings</h1>
        <p class="text-gray-600">Manage the coffee listings you've posted to the marketplace.</p>
      </div>
      <router-link
        to="/marketplace/create"
        class="shrink-0 inline-flex items-center gap-2 bg-amber-600 hover:bg-amber-700 text-white font-semibold py-3 px-6 rounded-xl shadow-md hover:shadow-lg transition-all"
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        New Listing
      </router-link>
    </div>

    <div v-if="loading" class="flex justify-center py-20">
      <LoadingSpinner class="w-8 h-8 text-amber-500" />
    </div>

    <div v-else-if="listings.length > 0" class="space-y-4">
      <div
        v-for="listing in listings"
        :key="listing.id"
        class="bg-white rounded-xl border border-gray-100 shadow-sm p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:shadow-md transition-shadow"
      >
        <div class="flex-1 min-w-0">
          <h3 class="font-bold text-gray-900 truncate">{{ listing.title }}</h3>
          <div class="flex flex-wrap gap-3 mt-1 text-sm text-gray-500">
            <span>{{ listing.region }}</span>
            <span>Grade {{ listing.ecx_grade }}</span>
            <span>{{ listing.available_kg.toLocaleString() }} kg</span>
            <span class="text-amber-700 font-medium">${{ listing.price_per_kg_usd.toFixed(2) }}/kg</span>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span
            class="text-xs px-2.5 py-1 rounded-full font-medium"
            :class="listing.is_active ? 'bg-green-50 text-green-700' : 'bg-gray-100 text-gray-500'"
          >
            {{ listing.is_active ? 'Active' : 'Inactive' }}
          </span>
          <button
            @click="handleDelete(listing.id)"
            class="p-2 rounded-lg text-gray-400 hover:text-red-500 hover:bg-red-50 transition-all"
            title="Delete listing"
          >
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div v-else class="flex flex-col items-center justify-center py-20 bg-white rounded-2xl border-2 border-dashed border-gray-200 text-center">
      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
        <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
        </svg>
      </div>
      <h3 class="text-gray-900 font-medium mb-1">No listings yet</h3>
      <p class="text-gray-500 text-sm mb-4">Post your first coffee listing to start connecting with buyers.</p>
      <router-link to="/marketplace/create" class="text-sm font-semibold text-amber-700 hover:text-amber-900 transition-colors">
        Post Your First Listing →
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import { listingService } from '../services/listingService'
import { useToast } from '../composables/useToast'

const toast = useToast()
const loading = ref(true)
const listings = ref([])

async function fetchMyListings() {
  loading.value = true
  try {
    listings.value = await listingService.getMyListings()
  } catch (err) {
    toast.error('Failed to load your listings')
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  if (!confirm('Are you sure you want to delete this listing?')) return

  try {
    await listingService.deleteListing(id)
    listings.value = listings.value.filter(l => l.id !== id)
    toast.success('Listing deleted')
  } catch (err) {
    toast.error('Failed to delete listing')
  }
}

onMounted(fetchMyListings)
</script>
