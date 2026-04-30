import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
    meta: { title: 'AI2CUP - Ethiopian Coffee Trade Platform' },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue'),
    meta: { title: 'Sign In - AI2CUP', guest: true },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue'),
    meta: { title: 'Create Account - AI2CUP', guest: true },
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
    meta: { title: 'Marketplace - AI2CUP', requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../views/ProfileView.vue'),
    meta: { title: 'My Profile - AI2CUP', requiresAuth: true },
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

// ── Navigation Guards ──
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Hydrate auth state on first navigation if token exists
  if (authStore.token && !authStore.user) {
    await authStore.initialize()
  }

  // Protected route — redirect to login if not authenticated
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }

  // Guest-only routes (login/register) — redirect home if already authenticated
  if (to.meta.guest && authStore.isAuthenticated) {
    return next({ name: 'home' })
  }

  next()
})

// Update page title
router.afterEach((to) => {
  document.title = to.meta.title || 'AI2CUP'
})

export default router
