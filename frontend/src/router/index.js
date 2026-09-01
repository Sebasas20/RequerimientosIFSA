
import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../pages/Dashboard.vue'
import Login from '../pages/Login.vue'
import UsersAdmin from '../pages/UsersAdmin.vue'
import { authState } from '../store/auth'

const routes = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/usuarios', name: 'UsersAdmin', component: UsersAdmin, meta: { requiresAuth: true, requiresAdmin: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !authState.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresAdmin && !authState.isAdmin) {
    next('/')
  } else if (to.path === '/login' && authState.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
