<template>
  <div class="dashboard">
    <header class="header">
      <div>
        <h1 style="margin: 0; color: var(--text-main);">Gestión de Encargados</h1>
        <p style="margin: 0.2rem 0 0; color: var(--text-muted);">Administración del Personal Asignado por Departamento</p>
      </div>
      <button class="btn btn-primary" @click="openCreateModal">+ Nuevo Encargado</button>
    </header>

    <!-- Filtros de Departamento (Pestañas) -->
    <div class="depto-tabs-wrapper">
      <div v-if="authState.isAdminData" class="depto-tabs">
        <button class="tab-btn active">📊 Requerimientos Data</button>
      </div>
      <div v-else-if="authState.isAdminHelpDesk" class="depto-tabs">
        <button class="tab-btn active">💻 HelpDesk Soporte TI</button>
      </div>
      <div v-else class="depto-tabs">
        <button 
          class="tab-btn" 
          :class="{ active: filterDepto === '' }" 
          @click="selectDepto('')">
          Todos los Encargados
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: filterDepto === 'BI' }" 
          @click="selectDepto('BI')">
          📊 Requerimientos Data
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: filterDepto === 'HELPDESK' }" 
          @click="selectDepto('HELPDESK')">
          💻 HelpDesk Soporte TI
        </button>
      </div>
    </div>

    <!-- Tabla Desktop (>= 768px) -->
    <div class="table-container card hidden-mobile">
      <table class="table">
        <thead>
          <tr>
            <th>Nombre del Encargado</th>
            <th>Departamento Destino</th>
            <th>Fecha de Registro</th>
            <th style="text-align: right;">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="encargado in encargados" :key="encargado.id">
            <td style="font-weight: 600; color: var(--text-main);">{{ encargado.nombre }}</td>
            <td>
              <span :class="encargado.departamento_destino === 'HELPDESK' ? 'badge badge-info' : 'badge badge-secondary'">
                {{ encargado.departamento_destino === 'HELPDESK' ? 'HELPDESK' : 'DATA' }}
              </span>
            </td>
            <td style="font-size: 0.85rem; color: var(--text-muted);">{{ formatDate(encargado.created_at) }}</td>
            <td style="text-align: right;">
              <button class="btn btn-danger-link btn-sm" @click="confirmDelete(encargado)">
                🗑️ Eliminar
              </button>
            </td>
          </tr>
          <tr v-if="encargados.length === 0">
            <td colspan="4" class="text-center" style="padding: 3rem; color: var(--text-muted); text-align: center;">
              No hay encargados registrados en este departamento.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Lista Móvil (< 768px) -->
    <div class="mobile-encargados-list hidden-desktop">
      <div v-for="encargado in encargados" :key="encargado.id" class="encargado-card card">
        <div class="encargado-card-header">
          <strong class="encargado-name">{{ encargado.nombre }}</strong>
          <span :class="encargado.departamento_destino === 'HELPDESK' ? 'badge badge-info' : 'badge badge-secondary'">
            {{ encargado.departamento_destino === 'HELPDESK' ? 'HELPDESK' : 'DATA' }}
          </span>
        </div>
        <div class="encargado-card-footer">
          <span class="encargado-date">📅 {{ formatDate(encargado.created_at) }}</span>
          <button class="btn btn-danger-link btn-sm" @click="confirmDelete(encargado)">
            🗑️ Eliminar
          </button>
        </div>
      </div>

      <div v-if="encargados.length === 0" class="card empty-card">
        <p>No hay encargados registrados.</p>
      </div>
    </div>

    <!-- Modal Formulario de Nuevo Encargado -->
    <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
      <div class="modal-content card">
        <div class="modal-header">
          <h2>Registrar Nuevo Encargado</h2>
          <button class="close-btn" @click="showForm = false">&times;</button>
        </div>

        <form @submit.prevent="handleCreateEncargado" class="form-wrapper">
          <div class="modal-scroll-body">
            <div v-if="errorMsg" class="alert-error">{{ errorMsg }}</div>

            <div class="form-group">
              <label>Nombre Completo del Encargado</label>
              <input 
                type="text" 
                v-model="form.nombre" 
                class="form-control" 
                placeholder="Ej: Carlos Rodríguez" 
                required 
              />
            </div>

            <!-- Selector de departamento para Super Admin -->
            <div v-if="authState.isAdmin" class="form-group">
              <label>Departamento Destino</label>
              <select v-model="form.departamento_destino" class="form-control" required>
                <option value="" disabled>Seleccione departamento...</option>
                <option value="BI">📊 Requerimientos Data (BI)</option>
                <option value="HELPDESK">💻 HelpDesk Soporte TI (HELPDESK)</option>
              </select>
            </div>
            <!-- Indicador fijo para Admins de Departamento -->
            <div v-else class="form-group">
              <label>Departamento Destino</label>
              <input 
                type="text" 
                :value="authState.isAdminData ? '📊 Requerimientos Data' : '💻 HelpDesk Soporte TI'" 
                class="form-control" 
                readonly 
                style="background-color: #f4f4f6; cursor: not-allowed; font-weight: 600;" 
              />
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showForm = false">Cancelar</button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Guardando...' : 'Guardar Encargado' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de Confirmación de Eliminación -->
    <div v-if="encargadoToDelete" class="modal-overlay" @click.self="encargadoToDelete = null">
      <div class="modal-content card" style="max-width: 440px;">
        <div class="modal-header">
          <h2 style="color: var(--danger-color);">Confirmar Eliminación</h2>
          <button class="close-btn" @click="encargadoToDelete = null">&times;</button>
        </div>
        <div style="padding: 0.5rem 0;">
          <p style="margin: 0; color: var(--text-main);">
            ¿Está seguro de que desea eliminar a <strong>{{ encargadoToDelete.nombre }}</strong> de la lista de encargados?
          </p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="encargadoToDelete = null">Cancelar</button>
          <button type="button" class="btn btn-danger" @click="executeDelete" :disabled="loading">
            {{ loading ? 'Eliminando...' : 'Eliminar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { encargadoService } from '../services/api'
import { authState } from '../store/auth'

const encargados = ref([])
const showForm = ref(false)
const loading = ref(false)
const errorMsg = ref('')
const filterDepto = ref('')
const encargadoToDelete = ref(null)

const form = reactive({
  nombre: '',
  departamento_destino: ''
})

const fetchEncargados = async () => {
  try {
    encargados.value = await encargadoService.getEncargados(filterDepto.value)
  } catch (err) {
    console.error('Error fetching encargados:', err)
  }
}

const selectDepto = (depto) => {
  filterDepto.value = depto
  fetchEncargados()
}

const openCreateModal = () => {
  errorMsg.value = ''
  form.nombre = ''
  if (authState.isAdminData) {
    form.departamento_destino = 'BI'
  } else if (authState.isAdminHelpDesk) {
    form.departamento_destino = 'HELPDESK'
  } else {
    form.departamento_destino = 'HELPDESK'
  }
  showForm.value = true
}

const handleCreateEncargado = async () => {
  try {
    loading.value = true
    errorMsg.value = ''
    await encargadoService.createEncargado({
      nombre: form.nombre,
      departamento_destino: form.departamento_destino
    })
    showForm.value = false
    fetchEncargados()
  } catch (err) {
    errorMsg.value = err.message || 'Error al guardar el encargado'
  } finally {
    loading.value = false
  }
}

const confirmDelete = (encargado) => {
  encargadoToDelete.value = encargado
}

const executeDelete = async () => {
  if (!encargadoToDelete.value) return
  try {
    loading.value = true
    await encargadoService.deleteEncargado(encargadoToDelete.value.id)
    encargadoToDelete.value = null
    fetchEncargados()
  } catch (err) {
    alert(err.message || 'Error al eliminar encargado')
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  if (authState.isAdminData) {
    filterDepto.value = 'BI'
  } else if (authState.isAdminHelpDesk) {
    filterDepto.value = 'HELPDESK'
  }
  fetchEncargados()
})
</script>

<style scoped>
.dashboard { max-width: 1400px; margin: 0 auto; }
.header { margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center; gap: 1rem; }
.table-container { overflow-x: auto; }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 1rem 1.25rem; border-bottom: 1px solid var(--border-color); text-align: left; }
.table th { background-color: #faf9fb; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); }

/* Depto Tabs */
.depto-tabs-wrapper {
  margin-bottom: 1.5rem;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
.depto-tabs { display: flex; gap: 0.5rem; white-space: nowrap; }
.tab-btn {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background: var(--surface-color);
  color: var(--text-muted);
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
  min-height: 44px;
}
.tab-btn:hover { background: rgba(164, 132, 82, 0.05); color: var(--text-main); }
.tab-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

/* Modals */
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(8, 6, 13, 0.6); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.modal-content {
  background: #fff; width: 480px; max-width: 90%; padding: 1.75rem; border-radius: 12px;
  display: flex; flex-direction: column; max-height: 90vh;
}
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; }
.modal-header h2 { margin: 0; font-size: 1.25rem; color: var(--text-main); }
.close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-muted); min-width: 44px; min-height: 44px; }
.form-wrapper { display: flex; flex-direction: column; flex: 1; overflow: hidden; }
.modal-scroll-body { overflow-y: auto; padding-right: 0.25rem; flex: 1; }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; margin-bottom: 0.4rem; font-weight: 500; font-size: 0.9rem; }
.modal-footer { margin-top: 1.25rem; display: flex; justify-content: flex-end; gap: 0.5rem; }
.alert-error { color: var(--danger-color); margin-bottom: 1rem; font-size: 0.875rem; }

.btn-danger {
  background-color: var(--danger-color);
  color: white;
  border-color: var(--danger-color);
}
.btn-danger:hover {
  background-color: #bb2d3b;
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

/* Mobile Encargados List */
.mobile-encargados-list { display: flex; flex-direction: column; gap: 0.75rem; }
.encargado-card { padding: 1rem; }
.encargado-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem; }
.encargado-name { font-size: 1.05rem; color: var(--text-main); }
.encargado-card-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 0.6rem; border-top: 1px solid var(--border-color); }
.encargado-date { font-size: 0.8rem; color: var(--text-muted); }
.empty-card { padding: 2.5rem; text-align: center; color: var(--text-muted); }

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
