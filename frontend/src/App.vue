
<template>
  <div v-if="authState.isAuthenticated" class="app-shell">
    <aside class="sidebar">
      <div class="sidebar-logo">
        <img src="./assets/logo-grupo-ifsa-1.png" alt="IFSA Logo" />
      </div>
      
      <div class="sidebar-user" style="margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.1);">
        <div style="font-weight: 600; font-size: 0.95rem;">{{ authState.user?.full_name }}</div>
        <div style="font-size: 0.8rem; color: rgba(255,255,255,0.6);">{{ authState.user?.role }}</div>
      </div>

      <nav class="sidebar-nav">
        <div class="nav-item" :class="{ active: $route.path === '/' }" @click="$router.push('/')">
          Dashboard
        </div>
        
        <div v-if="authState.isAdmin" class="nav-item" :class="{ active: $route.path === '/usuarios' }" @click="$router.push('/usuarios')">
          Gestión de Usuarios
        </div>

        <div style="margin-top: 1.5rem;">
          <button class="btn btn-primary" style="width: 100%; display: flex; align-items: center; justify-content: center; gap: 0.5rem;" @click="openNewRequest">
            Nueva Solicitud
          </button>
        </div>
      </nav>
      
      <div style="margin-top: auto; padding-top: 1rem;">
        <button class="btn" style="width: 100%; background: transparent; color: rgba(255,255,255,0.7); border: 1px solid rgba(255,255,255,0.2);" @click="handleLogout">
          Cerrar Sesión
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
import { useRouter } from 'vue-router'
import { uiState } from './store/ui'
import { authState } from './store/auth'

const router = useRouter()

const openNewRequest = () => {
  uiState.showForm = true
}

const handleLogout = () => {
  authState.logout()
  router.push('/login')
}
</script>
