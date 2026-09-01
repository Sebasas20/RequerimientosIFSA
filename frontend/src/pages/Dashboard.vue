<template>
  <div class="dashboard">
    <header class="header">
      <div>
        <h1 style="margin: 0; color: var(--text-main);">Gestión de Tickets</h1>
        <p style="margin: 0.2rem 0 0; color: var(--text-muted);">
          {{ authState.isAdmin ? 'Vista Administrador - Todos los tickets' : 'Mis Solicitudes' }}
        </p>
      </div>
    </header>

    <!-- KPI Cards para Administrador -->
    <div v-if="authState.isAdmin" class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{{ kpiStats.total }}</div>
        <div class="stat-label">En Backlog</div>
      </div>
      <div class="stat-card">
        <div class="stat-value" style="color: var(--info-color);">{{ kpiStats.enDesarrollo }}</div>
        <div class="stat-label">En Desarrollo</div>
      </div>
      <div class="stat-card">
        <div class="stat-value" style="color: var(--primary-color);">{{ kpiStats.prioridad1 }}</div>
        <div class="stat-label">Prioridad 1</div>
      </div>
      <div class="stat-card">
        <div class="stat-value" style="color: var(--secondary-color);">{{ kpiStats.pausados }}</div>
        <div class="stat-label">Pausados</div>
      </div>
      <div class="stat-card">
        <div class="stat-value" style="color: var(--warning-color);">{{ kpiStats.sinEncargado }}</div>
        <div class="stat-label">Sin Encargado</div>
      </div>
      <div class="stat-card">
        <div class="stat-value" style="color: var(--danger-color);">{{ kpiStats.nuevos }}</div>
        <div class="stat-label">Nuevos</div>
      </div>
    </div>
    
    <div class="filters card" style="padding: 1rem; display: flex; gap: 1rem; margin-bottom: 1.5rem; align-items: center;">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" style="color: var(--text-muted);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      <input type="text" v-model="searchQuery" @input="debounceSearch" placeholder="Buscar por Nombre o ID..." class="form-control search-input" style="border: none; box-shadow: none; background: transparent; padding: 0;" />
      
      <div style="width: 1px; height: 24px; background: var(--border-color);"></div>
      
      <select v-model="filterEstado" @change="fetchTickets" class="form-control filter-input" style="width: 250px; border: none; background: transparent; box-shadow: none;">
        <option value="">Todos los Estados</option>
        <option value="Creado / Esperando Asignación">Creado / Esperando Asignación</option>
        <option value="Asignado/Desarrollo">Asignado/Desarrollo</option>
        <option value="Información Requerida">Información Requerida</option>
        <option value="Pausado">Pausado</option>
        <option value="Rechazado/Fuera de Alcance">Rechazado/Fuera de Alcance</option>
      </select>
    </div>

    <div class="table-container card">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Solicitante</th>
            <th>Departamento</th>
            <th>Tipo Solicitud</th>
            <th>Prioridad</th>
            <th>Encargado</th>
            <th>Estado</th>
            <th style="text-align: right;">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ticket in tickets" :key="ticket.id">
            <td :title="ticket.id" style="font-family: monospace; color: var(--text-muted);">{{ ticket.id.substring(0,8) }}</td>
            <td style="font-weight: 500;">{{ ticket.nombre_solicitante }}</td>
            <td>{{ ticket.departamento }}</td>
            <td>{{ ticket.tipo_solicitud }}</td>
            <td>{{ ticket.prioridad || '-' }}</td>
            <td>{{ ticket.encargado || '-' }}</td>
            <td>
              <span :class="getBadgeClass(ticket.estado)">
                {{ ticket.estado }}
              </span>
            </td>
            <td style="text-align: right;">
              <button v-if="authState.isAdmin" class="btn btn-secondary btn-sm" @click="openAdminModal(ticket)">Gestionar</button>
              <button v-else class="btn btn-secondary btn-sm" @click="openDetailModal(ticket)">Ver Detalles</button>
            </td>
          </tr>
          <tr v-if="tickets.length === 0">
            <td colspan="8" class="text-center" style="padding: 3rem; color: var(--text-muted);">No hay tickets que coincidan con la búsqueda.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <TicketForm v-if="uiState.showForm" @close="uiState.showForm = false" @ticket-created="handleTicketCreated" />
    <TicketAdminModal v-if="selectedTicket && authState.isAdmin" :ticket="selectedTicket" @close="selectedTicket = null" @ticket-updated="fetchTickets" />
    <TicketDetailModal v-if="selectedTicketDetail && !authState.isAdmin" :ticket="selectedTicketDetail" @close="selectedTicketDetail = null" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ticketService } from '../services/api'
import TicketForm from '../components/TicketForm.vue'
import TicketAdminModal from '../components/TicketAdminModal.vue'
import TicketDetailModal from '../components/TicketDetailModal.vue'
import { uiState } from '../store/ui'
import { authState } from '../store/auth'

const tickets = ref([])
const selectedTicket = ref(null)
const selectedTicketDetail = ref(null)
const searchQuery = ref('')
const filterEstado = ref('')
let searchTimeout = null

const kpiStats = computed(() => {
  return {
    total: tickets.value.length,
    enDesarrollo: tickets.value.filter(t => t.estado === 'Asignado/Desarrollo').length,
    prioridad1: tickets.value.filter(t => t.prioridad === 'Prioridad 1').length,
    pausados: tickets.value.filter(t => t.estado === 'Pausado').length,
    sinEncargado: tickets.value.filter(t => !t.encargado || t.encargado.trim() === '' || t.encargado.toLowerCase() === 'sin asignar').length,
    nuevos: tickets.value.filter(t => t.estado === 'Creado / Esperando Asignación').length
  }
})

const fetchTickets = async () => {
  try {
    const filters = {}
    if (searchQuery.value) filters.search = searchQuery.value
    if (filterEstado.value) filters.estado = filterEstado.value
    tickets.value = await ticketService.getTickets(filters)
  } catch (error) {
    console.error("Error fetching tickets:", error)
  }
}

const debounceSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchTickets()
  }, 300)
}

const openAdminModal = (ticket) => {
  selectedTicket.value = ticket
}

const openDetailModal = (ticket) => {
  selectedTicketDetail.value = ticket
}

const handleTicketCreated = () => {
  fetchTickets()
}

// Watch triggerRefresh just in case we trigger it from outside
watch(() => uiState.triggerRefresh, () => {
  fetchTickets()
})

const getBadgeClass = (estado) => {
  switch(estado) {
    case 'Creado / Esperando Asignación': return 'badge badge-warning'
    case 'Asignado/Desarrollo': return 'badge badge-info'
    case 'Información Requerida': return 'badge badge-warning'
    case 'Pausado': return 'badge badge-secondary'
    case 'Rechazado/Fuera de Alcance': return 'badge badge-danger'
    default: return 'badge badge-secondary'
  }
}

onMounted(() => {
  fetchTickets()
})
</script>

<style scoped>
.dashboard { max-width: 1400px; margin: 0 auto; }
.header { margin-bottom: 2rem; }
.table-container { overflow-x: auto; }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 1rem 1.25rem; border-bottom: 1px solid var(--border-color); text-align: left; }
.table th { background-color: #faf9fb; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); }
.table tbody tr { transition: var(--transition); }
.table tbody tr:hover { background-color: #faf9fb; }
.btn-sm { padding: 0.4rem 0.8rem; font-size: 0.85rem; }

/* KPI Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.stat-card {
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-sm);
  padding: 1.25rem 1rem;
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
.stat-value {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-main);
  line-height: 1.1;
  margin-bottom: 0.5rem;
}
.stat-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
</style>
