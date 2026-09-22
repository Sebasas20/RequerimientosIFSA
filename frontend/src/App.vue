<template>
  <div v-if="authState.isAuthenticated" class="app-shell">
    <!-- Header Superior Fijo (Mobile Only < 768px) -->
    <header class="mobile-header">
      <button class="hamburger-btn" @click="toggleMobileMenu" aria-label="Abrir menú de navegación">
        ☰
      </button>

      <div class="mobile-header-brand">
        <img v-if="authState.user?.role === 'Usuario Arturos'" src="./assets/logo-arturos.png" alt="Arturos" class="mobile-header-logo" />
        <img v-else src="./assets/logo-grupo-ifsa-1.png" alt="IFSA" class="mobile-header-logo" />
        <span class="mobile-header-title">{{ currentRouteTitle }}</span>
      </div>

      <div class="mobile-user-avatar" :title="authState.user?.full_name">
        {{ userInitial }}
      </div>
    </header>

    <!-- Backdrop del Off-Canvas Menu -->
    <div 
      class="drawer-backdrop" 
      :class="{ active: mobileMenuOpen }" 
      @click="closeMobileMenu">
    </div>

    <!-- Barra Lateral (Desktop Fija / Mobile Drawer Off-Canvas) -->
    <aside class="sidebar" :class="{ open: mobileMenuOpen }">
      <div class="sidebar-logo">
        <img v-if="authState.user?.role === 'Usuario Arturos'" src="./assets/logo-arturos.png" alt="Arturos Logo" class="arturos-logo" style="filter: drop-shadow(0px 3px 6px rgba(0,0,0,0.3));" />
        <img v-else src="./assets/logo-grupo-ifsa-1.png" alt="IFSA Logo" />
      </div>
      
      <div class="sidebar-user" style="margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.1);">
        <div style="font-weight: 600; font-size: 0.95rem;">{{ authState.user?.full_name }}</div>
        <div style="font-size: 0.8rem; color: rgba(255,255,255,0.6);">{{ authState.user?.role }}</div>
      </div>

      <nav class="sidebar-nav">
        <div class="nav-item" :class="{ active: $route.path === '/' }" @click="navigate('/')">
          <span style="font-size: 1.1rem;">📊</span> Dashboard
        </div>

        <div v-if="authState.canManageTickets" class="nav-item" :class="{ active: $route.path === '/categorias' }" @click="navigate('/categorias')">
          <span style="font-size: 1.1rem;">🏷️</span> Gestión de Categorías
        </div>

        <div v-if="authState.canManageTickets" class="nav-item" :class="{ active: $route.path === '/encargados' }" @click="navigate('/encargados')">
          <span style="font-size: 1.1rem;">🛠️</span> Gestión de Encargados
        </div>
        
        <div v-if="authState.isAdmin" class="nav-item" :class="{ active: $route.path === '/usuarios' }" @click="navigate('/usuarios')">
          <span style="font-size: 1.1rem;">👥</span> Gestión de Usuarios
        </div>

        <div style="margin-top: 1.5rem;">
          <button class="btn btn-primary" style="width: 100%; display: flex; align-items: center; justify-content: center; gap: 0.5rem;" @click="handleOpenNewRequest">
            ➕ Nueva Solicitud
          </button>
        </div>
      </nav>
      
      <div style="margin-top: auto; padding-top: 1rem;">
        <button class="btn" style="width: 100%; background: transparent; color: rgba(255,255,255,0.7); border: 1px solid rgba(255,255,255,0.2);" @click="handleLogout">
          🚪 Cerrar Sesión
        </button>
      </div>
    </aside>
    
    <main class="main-content">
      <router-view />
    </main>
  </div>
  <div v-else>
    <router-view />
  </div>
</template>

<script setup>
import { ref, computed, watchEffect } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { uiState } from './store/ui'
import { authState } from './store/auth'

const router = useRouter()
const route = useRoute()

const mobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

const navigate = (path) => {
  closeMobileMenu()
  router.push(path)
}

const handleOpenNewRequest = () => {
  closeMobileMenu()
  uiState.showForm = true
}

const userInitial = computed(() => {
  if (!authState.user?.full_name) return 'U'
  return authState.user.full_name.charAt(0).toUpperCase()
})

const currentRouteTitle = computed(() => {
  if (route.path === '/usuarios') return 'Usuarios'
  if (route.path === '/encargados') return 'Encargados'
  if (route.path === '/categorias') return 'Categorías'
  return 'Dashboard'
})

watchEffect(() => {
  if (authState.isAuthenticated) {
    if (authState.user?.role === 'Usuario Arturos') {
      document.documentElement.setAttribute('data-theme', 'arturos')
    } else {
      document.documentElement.setAttribute('data-theme', 'ifsa')
    }
  }
})

const handleLogout = () => {
  closeMobileMenu()
  authState.logout()
  router.push('/login')
}
</script>
