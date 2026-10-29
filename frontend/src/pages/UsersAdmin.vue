<template>
  <div class="dashboard">
    <header class="header">
      <div>
        <h1 style="margin: 0; color: var(--text-main);">Gestión de Usuarios</h1>
        <p style="margin: 0.2rem 0 0; color: var(--text-muted);">Administración del Sistema</p>
      </div>
      <button class="btn btn-primary" @click="openCreateModal">+ Nuevo Usuario</button>
    </header>

    <!-- Barra de Búsqueda por Correo y Filtro por Rol -->
    <div class="filters card">
      <div class="search-box">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" style="color: var(--text-muted); flex-shrink: 0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input 
          type="text" 
          v-model="searchEmail" 
          placeholder="Buscar usuario por nombre o correo electrónico..." 
          class="form-control search-input" 
        />
      </div>
      
      <div class="filter-divider"></div>
      
      <div class="role-select-box">
        <select v-model="filterRole" class="form-control filter-input">
          <option value="">Todos los Roles</option>
          <option value="Usuario IFSA">Usuario IFSA</option>
          <option value="Usuario Arturos">Usuario Arturos</option>
          <option value="Usuario Planta">Usuario Planta</option>
          <option value="Administrador">Administrador (Super Admin)</option>
          <option value="Admin Data">Admin Data</option>
          <option value="Admin HelpDesk">Admin HelpDesk</option>
          <option value="Admin Trade">Admin Trade</option>
        </select>
      </div>
    </div>

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
            <th style="text-align: right;">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
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
            <td style="text-align: right; white-space: nowrap;">
              <div class="actions-group">
                <button class="btn btn-action-link btn-sm" @click="openPasswordModal(user)" title="Cambiar contraseña">
                  🔑 Contraseña
                </button>
                <button 
                  v-if="user.id !== authState.user?.id"
                  class="btn btn-danger-link btn-sm" 
                  @click="confirmDelete(user)" 
                  title="Eliminar usuario">
                  🗑️ Eliminar
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredUsers.length === 0">
            <td colspan="7" style="padding: 3rem; color: var(--text-muted); text-align: center;">
              No se encontraron usuarios que coincidan con los filtros seleccionados.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Lista de Usuarios en Tarjetas Móviles (< 768px) -->
    <div class="mobile-users-list hidden-desktop">
      <div v-for="user in filteredUsers" :key="user.id" class="user-card card">
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
        <div class="user-card-footer">
          <button class="btn btn-action-link btn-sm" @click="openPasswordModal(user)">
            🔑 Cambiar Contraseña
          </button>
          <button 
            v-if="user.id !== authState.user?.id"
            class="btn btn-danger-link btn-sm" 
            @click="confirmDelete(user)">
            🗑️ Eliminar
          </button>
        </div>
      </div>

      <div v-if="filteredUsers.length === 0" class="card empty-card">
        <p>No se encontraron usuarios que coincidan con los filtros seleccionados.</p>
      </div>
    </div>

    <!-- Modal Crear Nuevo Usuario -->
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
                <option value="Usuario Planta">Usuario Planta</option>
                <option value="Administrador">Administrador (Super Admin)</option>
                <option value="Admin Data">Admin Data</option>
                <option value="Admin HelpDesk">Admin HelpDesk</option>
                <option value="Admin Trade">Admin Trade</option>
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

    <!-- Modal Cambiar Contraseña -->
    <div v-if="userForPassword" class="modal-overlay" @click.self="closePasswordModal">
      <div class="modal-content card" style="max-width: 440px;">
        <div class="modal-header">
          <h2 style="margin: 0;">Cambiar Contraseña</h2>
          <button class="close-btn" @click="closePasswordModal">&times;</button>
        </div>
        <form @submit.prevent="handleUpdatePassword" class="form-wrapper">
          <div class="modal-scroll-body">
            <div v-if="passwordErrorMsg" class="alert alert-danger" style="color: var(--danger-color); margin-bottom: 1rem;">
              {{ passwordErrorMsg }}
            </div>

            <p style="margin: 0 0 1rem 0; font-size: 0.9rem; color: var(--text-muted);">
              Asignar nueva contraseña para <strong>{{ userForPassword.full_name }}</strong> ({{ userForPassword.email }}):
            </p>

            <div class="form-group" style="margin-bottom: 1rem;">
              <label>Nueva Contraseña</label>
              <input 
                type="password" 
                v-model="newPassword" 
                class="form-control" 
                placeholder="Ingrese la nueva contraseña..." 
                required 
              />
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closePasswordModal">Cancelar</button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Guardando...' : 'Actualizar Contraseña' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Confirmar Eliminación de Usuario -->
    <div v-if="userToDelete" class="modal-overlay" @click.self="userToDelete = null">
      <div class="modal-content card" style="max-width: 440px;">
        <div class="modal-header">
          <h2 style="margin: 0; color: var(--danger-color);">Confirmar Eliminación</h2>
          <button class="close-btn" @click="userToDelete = null">&times;</button>
        </div>
        <div style="padding: 0.5rem 0;">
          <div v-if="deleteErrorMsg" style="color: var(--danger-color); margin-bottom: 0.75rem; font-size: 0.875rem;">
            {{ deleteErrorMsg }}
          </div>
          <p style="margin: 0; color: var(--text-main); line-height: 1.5;">
            ¿Está seguro de que desea eliminar al usuario <strong>{{ userToDelete.full_name }}</strong> ({{ userToDelete.email }})?
          </p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="userToDelete = null">Cancelar</button>
          <button type="button" class="btn btn-danger" @click="executeDeleteUser" :disabled="loading">
            {{ loading ? 'Eliminando...' : 'Eliminar Usuario' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { userService } from '../services/api'
import { authState } from '../store/auth'

const users = ref([])
const showForm = ref(false)
const loading = ref(false)
const errorMsg = ref('')

const searchEmail = ref('')
const filterRole = ref('')

const userForPassword = ref(null)
const newPassword = ref('')
const passwordErrorMsg = ref('')

const userToDelete = ref(null)
const deleteErrorMsg = ref('')

const form = ref({
  full_name: '',
  email: '',
  password: '',
  role: 'Usuario IFSA',
  empresa: '',
  departamento: ''
})

const filteredUsers = computed(() => {
  const query = searchEmail.value.trim().toLowerCase()
  return users.value.filter(u => {
    const matchesSearch = !query || 
      (u.email && u.email.toLowerCase().includes(query)) ||
      (u.full_name && u.full_name.toLowerCase().includes(query))
    const matchesRole = !filterRole.value || u.role === filterRole.value
    return matchesSearch && matchesRole
  })
})

const fetchUsers = async () => {
  try {
    users.value = await userService.getUsers()
  } catch (err) {
    console.error(err)
  }
}

const openCreateModal = () => {
  errorMsg.value = ''
  showForm.value = true
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

const openPasswordModal = (user) => {
  userForPassword.value = user
  newPassword.value = ''
  passwordErrorMsg.value = ''
}

const closePasswordModal = () => {
  userForPassword.value = null
  newPassword.value = ''
  passwordErrorMsg.value = ''
}

const handleUpdatePassword = async () => {
  if (!userForPassword.value || !newPassword.value.trim()) return
  try {
    loading.value = true
    passwordErrorMsg.value = ''
    await userService.updatePassword(userForPassword.value.id, newPassword.value.trim())
    closePasswordModal()
  } catch (err) {
    passwordErrorMsg.value = err.message || 'Error al actualizar la contraseña'
  } finally {
    loading.value = false
  }
}

const confirmDelete = (user) => {
  deleteErrorMsg.value = ''
  userToDelete.value = user
}

const executeDeleteUser = async () => {
  if (!userToDelete.value) return
  try {
    loading.value = true
    deleteErrorMsg.value = ''
    await userService.deleteUser(userToDelete.value.id)
    userToDelete.value = null
    fetchUsers()
  } catch (err) {
    deleteErrorMsg.value = err.message || 'Error al eliminar usuario'
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString()
}

const getRoleBadgeClass = (role) => {
  if (['Administrador', 'Admin Data', 'Admin HelpDesk', 'Admin Trade'].includes(role)) {
    return 'badge'
  }
  return 'badge badge-secondary'
}

const getRoleBadgeStyle = (role) => {
  if (role === 'Administrador') {
    return { backgroundColor: '#A48452', color: '#FFFFFF' }
  }
  if (['Admin Data', 'Admin HelpDesk', 'Admin Trade'].includes(role)) {
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

/* Filters Card */
.filters {
  padding: 1rem;
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: center;
}
.search-box {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}
.search-input {
  border: none;
  box-shadow: none;
  background: transparent;
  padding: 0;
  min-height: auto;
}
.filter-divider {
  width: 1px;
  height: 24px;
  background: var(--border-color);
}
.role-select-box {
  width: 250px;
}
.filter-input {
  border: none;
  background: transparent;
  box-shadow: none;
  min-height: auto;
}

/* Action buttons */
.actions-group {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.btn-action-link {
  background: transparent;
  color: var(--primary-color);
  border: none;
  font-weight: 500;
  cursor: pointer;
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
}
.btn-action-link:hover {
  background-color: rgba(164, 132, 82, 0.12);
}
.btn-danger-link {
  background: transparent;
  color: var(--danger-color);
  border: none;
  font-weight: 500;
  cursor: pointer;
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
}
.btn-danger-link:hover {
  background-color: rgba(220, 53, 69, 0.1);
}
.btn-danger {
  background-color: var(--danger-color);
  color: white;
  border-color: var(--danger-color);
}
.btn-danger:hover {
  background-color: #bb2d3b;
}

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
.user-card-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  padding-top: 0.6rem;
  margin-top: 0.6rem;
  border-top: 1px solid var(--border-color);
}
.empty-card { padding: 2.5rem; text-align: center; color: var(--text-muted); }

@media (max-width: 767px) {
  .header { flex-direction: column; align-items: flex-start; }
  .header .btn { width: 100%; }
  .filters {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
    padding: 0.85rem;
  }
  .filter-divider { display: none; }
  .role-select-box {
    width: 100%;
    border-top: 1px solid var(--border-color);
    padding-top: 0.6rem;
  }
  .search-input, .filter-input {
    font-size: 16px !important;
  }
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
