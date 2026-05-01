<template>
  <footer class="w-full bg-slate-900 text-slate-300 pt-16 pb-8 border-t border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-16">
        <!-- Brand Section -->
        <div class="flex flex-col gap-6">
          <router-link to="/" class="flex items-center gap-3 group">
            <span class="text-3xl transition-transform group-hover:scale-110">☕</span>
            <div>
              <div class="font-bold text-2xl text-white tracking-tight leading-none">AI2CUP</div>
              <div class="text-[0.65rem] uppercase tracking-wider text-amber-500 font-bold mt-1">Smart Coffee Platform</div>
            </div>
          </router-link>
          <p class="text-sm leading-relaxed text-slate-400 max-w-xs">
            Revolutionizing the Ethiopian coffee supply chain through AI-driven transparency, quality assessment, and direct market access.
          </p>
          <div class="flex items-center gap-4">
            <a href="#" class="w-9 h-9 rounded-full bg-slate-800 flex items-center justify-center hover:bg-amber-600 hover:text-white transition-all shadow-sm" aria-label="Twitter">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M22.46,6C21.69,6.35 20.86,6.58 20,6.69C20.88,6.16 21.56,5.32 21.88,4.31C21.05,4.81 20.13,5.16 19.16,5.36C18.37,4.5 17.26,4 16,4C13.59,4 11.64,5.95 11.64,8.35C11.64,8.69 11.67,9.03 11.76,9.36C8.12,9.17 4.91,7.43 2.77,4.77C2.4,5.4 2.19,6.13 2.19,6.91C2.19,8.42 2.96,9.75 4.13,10.53C3.41,10.51 2.74,10.31 2.16,10C2.16,10.03 2.16,10.05 2.16,10.08C2.16,12.18 3.66,13.93 5.65,14.33C5.28,14.43 4.9,14.48 4.5,14.48C4.22,14.48 3.95,14.45 3.68,14.4C4.24,16.12 5.83,17.37 7.73,17.4C6.25,18.56 4.38,19.26 2.34,19.26C1.98,19.26 1.64,19.24 1.3,19.2C3.21,20.43 5.49,21.15 7.93,21.15C15.89,21.15 20.23,14.56 20.23,8.85C20.23,8.66 20.23,8.47 20.22,8.28C21.06,7.67 21.79,6.89 22.46,6Z" /></svg>
            </a>
            <a href="#" class="w-9 h-9 rounded-full bg-slate-800 flex items-center justify-center hover:bg-amber-600 hover:text-white transition-all shadow-sm" aria-label="LinkedIn">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M19,3A2,2 0 0,1 21,5V19A2,2 0 0,1 19,21H5A2,2 0 0,1 3,19V5A2,2 0 0,1 5,3H19M18.5,18.5V13.2A3.26,3.26 0 0,0 15.24,9.94C13.93,9.94 13,10.63 12.59,11.24V10.13H10.13V18.5H12.59V13.85C12.59,12.59 13.06,12.14 13.74,12.14C14.41,12.14 14.79,12.59 14.79,13.85V18.5H17.26V18.5M8.76,10.13H6.29V18.5H8.76V10.13M7.52,6.07A1.3,1.3 0 0,0 6.22,7.37A1.3,1.3 0 0,0 7.52,8.67A1.3,1.3 0 0,0 8.82,7.37A1.3,1.3 0 0,0 7.52,6.07Z" /></svg>
            </a>
            <a href="#" class="w-9 h-9 rounded-full bg-slate-800 flex items-center justify-center hover:bg-amber-600 hover:text-white transition-all shadow-sm" aria-label="Instagram">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M7.8 2h8.4C19.4 2 22 4.6 22 7.8v8.4a5.8 5.8 0 0 1-5.8 5.8H7.8C4.6 22 2 19.4 2 16.2V7.8A5.8 5.8 0 0 1 7.8 2m-.2 2A3.6 3.6 0 0 0 4 7.6v8.8C4 18.39 5.61 20 7.6 20h8.8a3.6 3.6 0 0 0 3.6-3.6V7.6C20 5.61 18.39 4 16.4 4H7.6m9.65 1.5a1.25 1.25 0 0 1 1.25 1.25A1.25 1.25 0 0 1 17.25 8 1.25 1.25 0 0 1 16 6.75a1.25 1.25 0 0 1 1.25-1.25M12 7a5 5 0 0 1 5 5 5 5 0 0 1-5 5 5 5 0 0 1-5-5 5 5 0 0 1 5-5m0 2a3 3 0 0 0-3 3 3 3 0 0 0 3 3 3 3 0 0 0 3-3 3 3 0 0 0-3-3z"/></svg>
            </a>
            <a href="https://github.com/AI2CUP" target="_blank" class="w-9 h-9 rounded-full bg-slate-800 flex items-center justify-center hover:bg-amber-600 hover:text-white transition-all shadow-sm" aria-label="GitHub">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5c.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34c-.46-1.16-1.11-1.47-1.11-1.47c-.91-.62.07-.6.07-.6c1 .08 1.53 1.03 1.53 1.03c.87 1.52 2.34 1.07 2.91.83c.09-.65.35-1.09.63-1.34c-2.22-.25-4.55-1.11-4.55-4.92c0-1.11.38-2 1.03-2.71c-.1-.25-.45-1.29.1-2.64c0 0 .84-.27 2.75 1.02c.79-.22 1.65-.33 2.5-.33c.85 0 1.71.11 2.5.33c1.91-1.29 2.75-1.02 2.75-1.02c.55 1.35.2 2.39.1 2.64c.65.71 1.03 1.6 1.03 2.71c0 3.82-2.34 4.66-4.57 4.91c.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/></svg>
            </a>
          </div>
        </div>

        <!-- Navigation Section -->
        <div>
          <h4 class="text-white font-bold mb-6 text-lg">Platform</h4>
          <ul class="space-y-4 text-sm">
            <li><router-link to="/price" class="hover:text-amber-400 transition-colors">Price Prediction</router-link></li>
            <li><router-link to="/quality" class="hover:text-amber-400 transition-colors">Quality Detection</router-link></li>
            <li><router-link to="/marketplace" class="hover:text-amber-400 transition-colors">Smart Marketplace</router-link></li>
            <li><router-link to="/register" class="hover:text-amber-400 transition-colors">Partner Registration</router-link></li>
          </ul>
        </div>

        <!-- Resources Section -->
        <div>
          <h4 class="text-white font-bold mb-6 text-lg">Support</h4>
          <ul class="space-y-4 text-sm">
            <li><a href="#" class="hover:text-amber-400 transition-colors">Help Center</a></li>
            <li><a href="#" class="hover:text-amber-400 transition-colors">ECX Grading Standards</a></li>
            <li><a href="#" class="hover:text-amber-400 transition-colors">Documentation</a></li>
            <li><a href="#" class="hover:text-amber-400 transition-colors">API Access</a></li>
          </ul>
        </div>

        <!-- Contact Section -->
        <div>
          <h4 class="text-white font-bold mb-6 text-lg">Get in Touch</h4>
          <ul class="space-y-4 text-sm">
            <li class="flex items-start gap-3">
              <svg class="w-5 h-5 text-amber-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
              <span>Addis Ababa, Ethiopia<br/><span class="text-slate-500 text-xs">Kirkos Sub-City, Kazanchis</span></span>
            </li>
            <li class="flex items-center gap-3">
              <svg class="w-5 h-5 text-amber-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
              <a href="tel:+251911234567" class="hover:text-amber-400 transition-colors">+251 911 234 567</a>
            </li>
            <li class="flex items-center gap-3">
              <svg class="w-5 h-5 text-amber-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
              <a href="mailto:hello@ai2cup.com" class="hover:text-amber-400 transition-colors">hello@ai2cup.com</a>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="pt-8 border-t border-slate-800 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-slate-500">
        <div class="flex items-center gap-6">
          <p>© {{ new Date().getFullYear() }} AI2CUP. All rights reserved.</p>
          <div class="hidden sm:flex items-center gap-4">
            <a href="#" class="hover:text-slate-300 transition-colors">Privacy Policy</a>
            <a href="#" class="hover:text-slate-300 transition-colors">Terms of Service</a>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>
          <span class="text-slate-400">System Live: Ethiopian Market Data Integrated</span>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>
