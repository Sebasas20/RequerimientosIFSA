
<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <img src="../assets/logo-grupo-ifsa-1.png" alt="IFSA Logo" class="login-logo" />
        
        <!-- Banner horizontal de logos de empresas del grupo -->
        <div class="group-logos-banner">
          <img src="../assets/logo-01.png" alt="Arturos" class="banner-logo banner-logo-arturos" title="Arturos" />
          <img src="../assets/logo-maralac.png" alt="Grupo Maralac" class="banner-logo banner-logo-maralac" title="Grupo Maralac" />
          <img src="../assets/logo-protinal.png" alt="Protinal" class="banner-logo banner-logo-protinal" title="Protinal" />
        </div>

        <h2>Iniciar Sesión</h2>
        <p>Sistema de Gestión de Requerimientos</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
        
        <div class="form-group">
          <label>Correo Electrónico</label>
          <input type="email" v-model="email" class="form-control" required />
        </div>
        
        <div class="form-group" style="margin-top: 1rem;">
          <label>Contraseña</label>
          <input type="password" v-model="password" class="form-control" required />
        </div>
        
        <button type="submit" class="btn btn-primary login-btn" :disabled="loading">
          {{ loading ? 'Ingresando...' : 'Entrar' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../services/api'
import { authState } from '../store/auth'

const router = useRouter()
const email = ref('')
const password = ref('')
const errorMsg = ref('')
const loading = ref(false)

const handleLogin = async () => {
  try {
    loading.value = true
    errorMsg.value = ''
    const res = await authService.login(email.value, password.value)
    authState.login(res.token, res.user)
    router.push('/')
  } catch (err) {
    errorMsg.value = err.message || 'Credenciales inválidas'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-color);
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: #1C1C34;
  padding: 2.5rem;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-logo {
  max-width: 180px;
  margin-bottom: 0.5rem;
}

.group-logos-banner {
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  gap: 1.25rem;
  margin: 0.85rem 0 1.5rem 0;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
}

.banner-logo {
  width: auto;
  object-fit: contain;
  opacity: 0.95;
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.banner-logo-arturos {
  height: 34px;
  max-width: 95px;
}

.banner-logo-maralac {
  height: 28px;
  max-width: 110px;
}

.banner-logo-protinal {
  height: 32px;
  max-width: 95px;
}

.banner-logo:hover {
  opacity: 1;
  transform: scale(1.05);
}

.login-header h2 {
  margin: 0;
  color: #FFFFFF;
  font-size: 1.5rem;
}

.login-header p {
  color: rgba(255, 255, 255, 0.7);
  margin-top: 0.5rem;
  font-size: 0.9rem;
}

.form-group label {
  color: #FFFFFF;
}

.login-btn {
  width: 100%;
  margin-top: 2rem;
  padding: 0.8rem;
  font-size: 1rem;
}

.alert-danger {
  background: rgba(220,53,69,0.1);
  color: #dc3545;
  padding: 0.8rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  text-align: center;
}
</style>
