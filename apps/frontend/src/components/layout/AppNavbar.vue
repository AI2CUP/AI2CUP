<template>
  <nav class="w-full bg-white/90 backdrop-blur-md border-b border-gray-100 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <router-link to="/" class="flex-shrink-0 flex items-center gap-3">
            <span class="text-2xl" role="img" aria-label="coffee">☕</span>
            <div>
              <div class="font-bold text-xl text-gray-900 tracking-tight leading-none">AI2CUP</div>
              <div class="text-[0.65rem] uppercase tracking-wider text-emerald-600 font-semibold mt-0.5">AI for Ethiopian Coffee</div>
            </div>
          </router-link>
        </div>
        
        <div class="hidden sm:flex sm:space-x-8">
          <router-link 
            to="/price" 
            class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
            :class="[ $route.path === '/price' ? 'border-emerald-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700' ]"
          >
            📈 Price
          </router-link>
          <router-link 
            to="/quality" 
            class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
            :class="[ $route.path === '/quality' ? 'border-emerald-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700' ]"
          >
            🔬 Quality
          </router-link>
          <router-link 
            to="/marketplace" 
            class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
            :class="[ $route.path === '/marketplace' ? 'border-emerald-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700' ]"
          >
            🏪 Market
          </router-link>
        </div>
        
        <!-- Mobile menu button placeholder -->
        <div class="flex items-center sm:hidden">
          <button class="text-gray-500 hover:text-gray-700 p-2">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
// Navigation component utilizing Vue Router
</script>
