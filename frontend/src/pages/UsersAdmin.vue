
<template>
  <div class="dashboard">
    <header class="header">
      <div>
        <h1 style="margin: 0; color: var(--text-main);">Gestión de Usuarios</h1>
        <p style="margin: 0.2rem 0 0; color: var(--text-muted);">Administración del Sistema</p>
      </div>
      <button class="btn btn-primary" @click="showForm = true">+ Nuevo Usuario</button>
    </header>

    <div class="table-container card">
      <table class="table">
        <thead>
          <tr>
            <th>Nombre Completo</th>
            <th>Correo Electrónico</th>
            <th>Rol</th>
            <th>Fecha de Creación</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td style="font-weight: 500;">{{ user.full_name }}</td>
            <td>{{ user.email }}</td>
            <td>
              <span :class="user.role === 'Administrador' ? 'badge badge-primary' : 'badge badge-secondary'"
                    :style="user.role === 'Administrador' ? 'background-color: var(--primary-color); color: white;' : ''">
                {{ user.role }}
              </span>
            </td>
            <td>{{ formatDate(user.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Form -->
    <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
      <div class="modal-content card" style="width: 450px; max-width: 90%; padding: 2rem;">
        <h2 style="margin-top:0;">Crear Nuevo Usuario</h2>
        <form @submit.prevent="handleCreateUser">
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

          <div class="form-group" style="margin-bottom: 1.5rem;">
            <label>Rol de Usuario</label>
            <select v-model="form.role" class="form-control" required>
              <option value="Usuario">Usuario</option>
              <option value="Administrador">Administrador</option>
            </select>
          </div>

          <div style="display: flex; gap: 1rem; justify-content: flex-end;">
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
  role: 'Usuario'
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
    form.value = { full_name: '', email: '', password: '', role: 'Usuario' }
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

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.dashboard { max-width: 1400px; margin: 0 auto; }
.header { margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; }
.table-container { overflow-x: auto; }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 1rem 1.25rem; border-bottom: 1px solid var(--border-color); text-align: left; }
.table th { background-color: #faf9fb; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); }
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center; z-index: 1000;
}
</style>
