<template>
  <div class="dashboard">
    <header class="header">
      <div>
        <h1 style="margin: 0; color: var(--text-main);">Gestión de Usuarios</h1>
        <p style="margin: 0.2rem 0 0; color: var(--text-muted);">Administración del Sistema</p>
      </div>
      <button class="btn btn-primary" @click="showForm = true">+ Nuevo Usuario</button>
    </header>

    <!-- Tabla Desktop (>= 768px) -->
    <div class="table-container card hidden-mobile">
      <table class="table">
        <thead>
          <tr>
            <th>Nombre Completo</th>
            <th>Correo Electrónico</th>
            <th>Empresa / Ubicación</th>
            <th>Departamento / Sede</th>
            <th style="white-space: nowrap;">Rol</th>
            <th style="white-space: nowrap; font-size: 0.8rem;">Fecha de Creación</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td style="font-weight: 500;">{{ user.full_name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.empresa || '-' }}</td>
            <td>{{ user.departamento || '-' }}</td>
            <td style="white-space: nowrap;">
              <span :class="getRoleBadgeClass(user.role)" :style="getRoleBadgeStyle(user.role)" style="padding: 0.4rem 0.95rem; white-space: nowrap; font-size: 0.8rem;">
                {{ user.role }}
              </span>
            </td>
            <td style="font-size: 0.8rem; color: var(--text-muted); white-space: nowrap;">{{ formatDate(user.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Lista de Usuarios en Tarjetas Móviles (< 768px) -->
    <div class="mobile-users-list hidden-desktop">
      <div v-for="user in users" :key="user.id" class="user-card card">
        <div class="user-card-header">
          <strong class="user-name">{{ user.full_name }}</strong>
          <span :class="getRoleBadgeClass(user.role)" :style="getRoleBadgeStyle(user.role)" class="user-badge">
            {{ user.role }}
          </span>
        </div>
        <div class="user-card-body">
          <p>✉️ {{ user.email }}</p>
          <p v-if="user.empresa || user.departamento">🏢 {{ user.empresa || '-' }} - {{ user.departamento || '-' }}</p>
          <p class="user-date">📅 {{ formatDate(user.created_at) }}</p>
        </div>
      </div>
    </div>

    <!-- Modal Form -->
    <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
      <div class="modal-content card">
        <div class="modal-header">
          <h2 style="margin: 0;">Crear Nuevo Usuario</h2>
          <button class="close-btn" @click="showForm = false">&times;</button>
        </div>
        <form @submit.prevent="handleCreateUser" class="form-wrapper">
          <div class="modal-scroll-body">
            <div v-if="errorMsg" class="alert alert-danger" style="color: red; margin-bottom: 1rem;">{{ errorMsg }}</div>
            
            <div class="form-group" style="margin-bottom: 1rem;">
              <label>Nombre Completo</label>
              <input type="text" v-model="form.full_name" class="form-control" required />
            </div>

            <div class="form-group" style="margin-bottom: 1rem;">
              <label>Correo Electrónico</label>
              <input type="email" v-model="form.email" class="form-control" required />
            </div>

            <div class="form-group" style="margin-bottom: 1rem;">
              <label>Contraseña</label>
              <input type="password" v-model="form.password" class="form-control" required />
            </div>

            <div class="form-group" style="margin-bottom: 1rem;">
              <label>Empresa / Ubicación</label>
              <input type="text" v-model="form.empresa" class="form-control" placeholder="Ej: Arturos / Grupo IFSA / Paica" />
            </div>

            <div class="form-group" style="margin-bottom: 1rem;">
              <label>Departamento / Sede</label>
              <input type="text" v-model="form.departamento" class="form-control" placeholder="Ej: Análisis de Datos / Sambil Candelaria" />
            </div>

            <div class="form-group" style="margin-bottom: 1rem;">
              <label>Rol de Usuario</label>
              <select v-model="form.role" class="form-control" required>
                <option value="Usuario IFSA">Usuario IFSA</option>
                <option value="Usuario Arturos">Usuario Arturos</option>
                <option value="Administrador">Administrador (Super Admin)</option>
                <option value="Admin Data">Admin Data</option>
                <option value="Admin HelpDesk">Admin HelpDesk</option>
              </select>
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showForm = false">Cancelar</button>
            <button type="submit" class="btn btn-primary" :disabled="loading">{{ loading ? 'Creando...' : 'Crear Usuario' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { userService } from '../services/api'

const users = ref([])
const showForm = ref(false)
const loading = ref(false)
const errorMsg = ref('')

const form = ref({
  full_name: '',
  email: '',
  password: '',
  role: 'Usuario IFSA',
  empresa: '',
  departamento: ''
})

const fetchUsers = async () => {
  try {
    users.value = await userService.getUsers()
  } catch (err) {
    console.error(err)
  }
}

const handleCreateUser = async () => {
  try {
    loading.value = true
    errorMsg.value = ''
    await userService.createUser(form.value)
    showForm.value = false
    form.value = { full_name: '', email: '', password: '', role: 'Usuario IFSA', empresa: '', departamento: '' }
    fetchUsers()
  } catch (err) {
    errorMsg.value = err.message || 'Error al crear usuario'
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString()
}

const getRoleBadgeClass = (role) => {
  if (role === 'Administrador' || role === 'Admin Data' || role === 'Admin HelpDesk') {
    return 'badge'
  }
  return 'badge badge-secondary'
}

const getRoleBadgeStyle = (role) => {
  if (role === 'Administrador') {
    return { backgroundColor: '#A48452', color: '#FFFFFF' }
  }
  if (role === 'Admin Data' || role === 'Admin HelpDesk') {
    return { backgroundColor: '#1C1C34', color: '#FFFFFF' }
  }
  return {}
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.dashboard { max-width: 1400px; margin: 0 auto; }
.header { margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center; gap: 1rem; }
.table-container { overflow-x: auto; }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 1rem 1.25rem; border-bottom: 1px solid var(--border-color); text-align: left; }
.table th { background-color: #faf9fb; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); }

.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(8, 6, 13, 0.6); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.modal-content {
  background: #fff; width: 480px; max-width: 90%; padding: 1.75rem; border-radius: 12px;
  display: flex; flex-direction: column; max-height: 90vh;
}
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-muted); min-width: 44px; min-height: 44px; }
.form-wrapper { display: flex; flex-direction: column; flex: 1; overflow: hidden; }
.modal-scroll-body { overflow-y: auto; padding-right: 0.25rem; flex: 1; }
.modal-footer { margin-top: 1.25rem; display: flex; justify-content: flex-end; gap: 0.5rem; }

.mobile-users-list { display: flex; flex-direction: column; gap: 0.75rem; }
.user-card { padding: 1rem; }
.user-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
.user-name { font-size: 1rem; color: var(--text-main); }
.user-badge { font-size: 0.75rem; padding: 0.3rem 0.7rem; }
.user-card-body p { margin: 0.25rem 0; font-size: 0.875rem; color: var(--text-muted); }
.user-date { font-size: 0.78rem !important; }

@media (max-width: 767px) {
  .header { flex-direction: column; align-items: flex-start; }
  .header .btn { width: 100%; }
  .modal-overlay { align-items: flex-end; }
  .modal-content {
    width: 100%; max-width: 100%; border-radius: 20px 20px 0 0;
    max-height: 88vh; padding: 1.25rem 1.25rem 0 1.25rem;
  }
  .modal-footer {
    position: sticky; bottom: 0; background: var(--surface-color);
    padding: 1rem 0; border-top: 1px solid var(--border-color); margin-top: auto;
    width: 100%; z-index: 10;
  }
  .modal-footer .btn { flex: 1; }
}
</style>
