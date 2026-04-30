<template>
  <div>
    <!-- Hero Section -->
    <div class="relative overflow-hidden bg-white">
      <div class="absolute inset-0 z-0">
        <div class="absolute inset-0 bg-gradient-to-tr from-emerald-900/90 to-emerald-800/80"></div>
        <img 
          src="https://images.unsplash.com/photo-1497935586351-b67a49e012bf?auto=format&fit=crop&q=80" 
          alt="Coffee field in Ethiopia" 
          class="w-full h-full object-cover mix-blend-overlay opacity-30" 
        />
      </div>
      
      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-32 flex flex-col items-center text-center">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 border border-white/20 text-emerald-50 text-sm font-medium mb-6 backdrop-blur-sm">
          The Future of Ethiopian Coffee Trade
        </div>
        
        <h1 class="text-4xl md:text-5xl lg:text-7xl font-extrabold text-white tracking-tight mb-6">
          AI2CUP <span class="text-emerald-400 font-light">Platform</span>
        </h1>
        
        <p class="text-xl md:text-2xl text-emerald-100 max-w-3xl mb-10 font-light leading-relaxed">
          Empowering Ethiopian farmers and global buyers with AI-driven price prediction, automated ECX quality grading, and smart matchmaking.
        </p>
        
        <div class="flex flex-col sm:flex-row items-center gap-4">
          <router-link to="/price" class="bg-emerald-500 hover:bg-emerald-400 text-white font-semibold py-3.5 px-8 rounded-xl shadow-lg hover:shadow-xl transition-all w-full sm:w-auto text-center border border-emerald-400/50">
            Try Price Prediction
          </router-link>
          <router-link to="/marketplace" class="bg-white/10 hover:bg-white/20 text-white font-semibold py-3.5 px-8 rounded-xl backdrop-blur-sm border border-white/30 transition-all w-full sm:w-auto text-center">
            Explore Marketplace
          </router-link>
        </div>
      </div>
    </div>
    
    <!-- Features Grid -->
    <div class="bg-gray-50 py-20 border-t border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">Core AI Capabilities</h2>
          <p class="text-gray-600 max-w-2xl mx-auto">Three integrated modules designed to increase transparency and eliminate intermediaries in the coffee supply chain.</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <router-link to="/price" class="group bg-white rounded-2xl p-8 shadow-sm border border-gray-100 hover:shadow-xl hover:border-emerald-200 transition-all duration-300 relative overflow-hidden flex flex-col items-center text-center group-hover:-translate-y-1">
            <div class="absolute inset-0 bg-gradient-to-b from-blue-50/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div class="w-20 h-20 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center mb-6 shadow-sm group-hover:scale-110 transition-transform">
              <svg class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3 relative z-10">Market Price Prediction</h3>
            <p class="text-gray-600 text-sm leading-relaxed relative z-10">Machine learning models trained on historical ECX data to forecast fair market prices based on region, quality, and seasonal factors.</p>
            <div class="mt-6 text-emerald-600 font-medium text-sm flex items-center gap-1 group-hover:gap-2 transition-all">Launch Module <span>→</span></div>
          </router-link>
          
          <!-- Feature 2 -->
          <router-link to="/quality" class="group bg-white rounded-2xl p-8 shadow-sm border border-gray-100 hover:shadow-xl hover:border-emerald-200 transition-all duration-300 relative overflow-hidden flex flex-col items-center text-center group-hover:-translate-y-1">
            <div class="absolute inset-0 bg-gradient-to-b from-amber-50/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div class="w-20 h-20 bg-amber-100 text-amber-600 rounded-2xl flex items-center justify-center mb-6 shadow-sm group-hover:scale-110 transition-transform">
              <svg class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.691.387a6 6 0 01-3.86.517l-2.387-.477a2 2 0 00-1.022.547l-1.162 1.162a2 2 0 00.597 3.321l1.664.333a4 4 0 002.573-.344l.69-.387a4 4 0 012.573-.344l1.664.333a2 2 0 002.597-3.321l-1.162-1.162z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11V5a2 2 0 00-2-2H9a2 2 0 00-2 2v6" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3 relative z-10">Computer Vision Quality</h3>
            <p class="text-gray-600 text-sm leading-relaxed relative z-10">Upload a photo of green coffee beans to instantly receive AI-calculated ECX Grade assessments (Grade 1-5) based on brightness and physical uniformity.</p>
            <div class="mt-6 text-emerald-600 font-medium text-sm flex items-center gap-1 group-hover:gap-2 transition-all">Launch Module <span>→</span></div>
          </router-link>
          
          <!-- Feature 3 -->
          <router-link to="/marketplace" class="group bg-white rounded-2xl p-8 shadow-sm border border-gray-100 hover:shadow-xl hover:border-emerald-200 transition-all duration-300 relative overflow-hidden flex flex-col items-center text-center group-hover:-translate-y-1">
            <div class="absolute inset-0 bg-gradient-to-b from-indigo-50/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div class="w-20 h-20 bg-indigo-100 text-indigo-600 rounded-2xl flex items-center justify-center mb-6 shadow-sm group-hover:scale-110 transition-transform">
              <svg class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3 relative z-10">Smart Matchmaking</h3>
            <p class="text-gray-600 text-sm leading-relaxed relative z-10">Algorithmic matching connecting local cooperatives with international buyers based on exact volume constraints, quality levels, and budget parity.</p>
            <div class="mt-6 text-emerald-600 font-medium text-sm flex items-center gap-1 group-hover:gap-2 transition-all">Launch Module <span>→</span></div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>
