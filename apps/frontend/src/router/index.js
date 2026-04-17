import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
    meta: { title: 'AI2CUP - Ethiopian Coffee Trade Platform' },
  },
  {
    path: '/price',
    name: 'price',
    component: () => import('../views/PriceView.vue'),
    meta: { title: 'Price Prediction - AI2CUP' },
  },
  {
    path: '/quality',
    name: 'quality',
    component: () => import('../views/QualityView.vue'),
    meta: { title: 'Quality Detection - AI2CUP' },
  },
  {
    path: '/marketplace',
    name: 'marketplace',
    component: () => import('../views/MarketplaceView.vue'),
    meta: { title: 'Marketplace - AI2CUP' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  },
})

// Update page title
router.afterEach((to) => {
  document.title = to.meta.title || 'AI2CUP'
})

export default router
