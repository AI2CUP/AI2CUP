<template>
  <div class="min-h-screen flex flex-col items-center w-full">
    <AppNavbar />
    
    <div class="w-full relative">
      <AppToast />
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
    
    <AppFooter />
  </div>
</template>

<script setup>
import AppNavbar from './components/layout/AppNavbar.vue'
import AppFooter from './components/layout/AppFooter.vue'
import AppToast from './components/layout/AppToast.vue'
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
