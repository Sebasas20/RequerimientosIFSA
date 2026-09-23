<template>
  <div class="dashboard">
    <header class="header">
      <div>
        <h1 style="margin: 0; color: var(--text-main);">Gestión de Tickets</h1>
        <p style="margin: 0.2rem 0 0; color: var(--text-muted);">
          {{ authState.canManageTickets ? 'Vista Administrador - Sistema de Servicios IFSA' : 'Mis Solicitudes' }}
        </p>
      </div>
    </header>

    <!-- KPI Cards para Administradores -->
    <div v-if="authState.canManageTickets" class="stats-container">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">{{ kpiStats.total }}</div>
          <div class="stat-label">Total Solicitudes</div>
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
    </div>
    
    <!-- Filtros de Departamento Destino (Pestañas) -->
    <div class="depto-tabs-wrapper">
      <div v-if="authState.isAdminData" class="depto-tabs">
        <button class="tab-btn active">📊 Requerimientos Data</button>
      </div>
      <div v-else-if="authState.isAdminHelpDesk" class="depto-tabs">
        <button class="tab-btn active">💻 HelpDesk Soporte TI</button>
      </div>
      <div v-else class="depto-tabs">
        <button 
          v-if="!isArturosUser"
          class="tab-btn" 
          :class="{ active: filterDeptoDestino === '' }" 
          @click="selectDeptoDestino('')">
          Todos los Servicios
        </button>
        <button 
          v-if="!isArturosUser"
          class="tab-btn" 
          :class="{ active: filterDeptoDestino === 'BI' }" 
          @click="selectDeptoDestino('BI')">
          📊 Requerimientos Data
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: filterDeptoDestino === 'HELPDESK' }" 
          @click="selectDeptoDestino('HELPDESK')">
          💻 HelpDesk Soporte TI
        </button>
      </div>
    </div>

    <!-- Barra de Búsqueda y Estado -->
    <div class="filters card">
      <div class="search-box">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" style="color: var(--text-muted); flex-shrink: 0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" v-model="searchQuery" @input="debounceSearch" placeholder="Buscar por Solicitante, Asunto o ID..." class="form-control search-input" />
      </div>
      
      <div class="filter-divider"></div>
      
      <div class="status-select-box">
        <select v-model="filterEstado" @change="fetchTickets" class="form-control filter-input">
          <option value="">Todos los Estados</option>
          <option value="Creado / Esperando Asignación">Creado / Esperando Asignación</option>
          <option value="Asignado/Desarrollo">Asignado / En progreso</option>
          <option value="Información Requerida">Información Requerida</option>
          <option value="Pausado">Pausado</option>
          <option value="Cerrado/Resuelto">Cerrado / Resuelto</option>
          <option value="Rechazado/Fuera de Alcance">Rechazado/Fuera de Alcance</option>
        </select>
      </div>
    </div>

    <!-- Tabla Principal de Tickets (Desktop >= 768px) -->
    <div class="table-container card hidden-mobile">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th v-if="!authState.isAreaAdmin">Área</th>
            <th>Solicitante</th>
            <th>Departamento</th>
            <th>Asunto</th>
            <th>Tipo / Caso</th>
            <th>Prioridad</th>
            <th v-if="!authState.isAreaAdmin">Encargado</th>
            <th>Estado</th>
            <th style="text-align: right;">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ticket in tickets" :key="ticket.id">
            <td :title="ticket.id" style="font-family: monospace; color: var(--text-muted);">#{{ ticket.id.substring(0,8) }}</td>
            <td v-if="!authState.isAreaAdmin">
              <span :class="ticket.departamento_destino === 'HELPDESK' ? 'badge badge-info' : 'badge badge-secondary'">
                {{ formatAreaBadge(ticket.departamento_destino) }}
              </span>
            </td>
            <td style="font-weight: 500;">{{ ticket.nombre_solicitante }}</td>
            <td>{{ ticket.departamento || '-' }}</td>
            <td style="font-weight: 500; color: var(--text-main);">{{ ticket.asunto || ticket.descripcion.substring(0,40) }}</td>
            <td>{{ ticket.tipo_solicitud || '-' }}</td>
            <td>{{ ticket.prioridad || '-' }}</td>
            <td v-if="!authState.isAreaAdmin">{{ ticket.encargado || '-' }}</td>
            <td>
              <span :class="getBadgeClass(ticket.estado)">
                {{ ticket.estado }}
              </span>
            </td>
            <td style="text-align: right;">
              <button v-if="authState.canManageTickets" class="btn btn-secondary btn-sm" @click="openAdminModal(ticket)">Gestionar</button>
              <button v-else class="btn btn-secondary btn-sm" @click="openDetailModal(ticket)">Ver Detalles</button>
            </td>
          </tr>
          <tr v-if="tickets.length === 0">
            <td :colspan="authState.isAreaAdmin ? 8 : 10" class="text-center" style="padding: 3rem; color: var(--text-muted); text-align: center;">No hay tickets que coincidan con la búsqueda.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Vista de Tarjetas Móviles (< 768px) -->
    <div class="mobile-tickets-list hidden-desktop">
      <TicketCard
        v-for="ticket in tickets"
        :key="ticket.id"
        :ticket="ticket"
        :canManage="authState.canManageTickets"
        :isAreaAdmin="authState.isAreaAdmin"
        @open-admin="openAdminModal"
        @open-detail="openDetailModal"
      />
      <div v-if="tickets.length === 0" class="card empty-mobile-card">
        <p>No hay tickets que coincidan con la búsqueda.</p>
      </div>
    </div>

    <!-- Modales de Flujo -->
    <!-- 1. Modal Catálogo de Servicios -->
    <ServiceCatalogModal 
      v-if="uiState.showForm && !selectedService" 
      :userRole="authState.user?.role"
      @close="uiState.showForm = false" 
      @select-service="handleSelectService" 
    />

    <!-- 2. Modal Formulario de Ticket Adaptativo -->
    <TicketForm 
      v-if="uiState.showForm && selectedService" 
      :departamentoDestino="selectedService"
      @close="resetFormState" 
      @ticket-created="handleTicketCreated" 
    />

    <!-- 3. Modales de Gestión / Detalle -->
    <TicketAdminModal v-if="selectedTicket && authState.canManageTickets" :ticket="selectedTicket" @close="selectedTicket = null" @ticket-updated="fetchTickets" />
    <TicketDetailModal v-if="selectedTicketDetail && !authState.canManageTickets" :ticket="selectedTicketDetail" @close="selectedTicketDetail = null" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ticketService } from '../services/api'
import ServiceCatalogModal from '../components/ServiceCatalogModal.vue'
import TicketForm from '../components/TicketForm.vue'
import TicketAdminModal from '../components/TicketAdminModal.vue'
import TicketDetailModal from '../components/TicketDetailModal.vue'
import TicketCard from '../components/TicketCard.vue'
import { uiState } from '../store/ui'
import { authState } from '../store/auth'

const tickets = ref([])
const selectedTicket = ref(null)
const selectedTicketDetail = ref(null)
const selectedService = ref(null)
const searchQuery = ref('')
const filterEstado = ref('')
const filterDeptoDestino = ref('')
let searchTimeout = null

const kpiStats = computed(() => {
  return {
    total: tickets.value.length,
    enDesarrollo: tickets.value.filter(t => t.estado === 'Asignado/Desarrollo' || t.estado === 'Asignado / En progreso').length,
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
    if (filterDeptoDestino.value) filters.departamento_destino = filterDeptoDestino.value
    tickets.value = await ticketService.getTickets(filters)
  } catch (error) {
    console.error("Error fetching tickets:", error)
  }
}

const selectDeptoDestino = (depto) => {
  filterDeptoDestino.value = depto
  fetchTickets()
}

const handleSelectService = (service) => {
  selectedService.value = service
}

const resetFormState = () => {
  uiState.showForm = false
  selectedService.value = null
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
  resetFormState()
  fetchTickets()
}

watch(() => uiState.showForm, (newVal) => {
  if (!newVal) {
    selectedService.value = null
  }
})

watch(() => uiState.triggerRefresh, () => {
  fetchTickets()
})

const getBadgeClass = (estado) => {
  switch(estado) {
    case 'Creado / Esperando Asignación': 
      return 'badge badge-status badge-info'
    case 'Asignado/Desarrollo':
    case 'Asignado / En progreso':
    case 'Información Requerida': 
      return 'badge badge-status badge-warning'
    case 'Pausado':
    case 'Rechazado/Fuera de Alcance': 
      return 'badge badge-status badge-danger'
    case 'Cerrado/Resuelto': 
      return 'badge badge-status badge-success'
    default: 
      return 'badge badge-status badge-secondary'
  }
}

const formatAreaBadge = (depto) => (depto === 'HELPDESK' ? 'HELPDESK' : 'DATA')

const isArturosUser = computed(() => authState.user?.role === 'Usuario Arturos')

onMounted(() => {
  if (authState.isAdminData) {
    filterDeptoDestino.value = 'BI'
  } else if (authState.isAdminHelpDesk || isArturosUser.value) {
    filterDeptoDestino.value = 'HELPDESK'
  }
  fetchTickets()
})
</script>

<style scoped>
.dashboard { max-width: 1400px; margin: 0 auto; }
.header { margin-bottom: 1.5rem; }
.table-container { overflow-x: auto; }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 1rem 1rem; border-bottom: 1px solid var(--border-color); text-align: left; font-size: 0.9rem; }
.table th { background-color: #faf9fb; font-weight: 600; font-size: 0.825rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); }
.table tbody tr { transition: var(--transition); }
.table tbody tr:hover { background-color: #faf9fb; }
.btn-sm { padding: 0.4rem 0.8rem; font-size: 0.85rem; }

/* Tabs de departamento */
.depto-tabs-wrapper {
  margin-bottom: 1rem;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  padding-bottom: 0.25rem;
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

/* KPI Stats */
.stats-container {
  margin-bottom: 1.5rem;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
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
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-main);
  line-height: 1.1;
  margin-bottom: 0.4rem;
}
.stat-label {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

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
.status-select-box {
  width: 250px;
}
.filter-input {
  border: none;
  background: transparent;
  box-shadow: none;
  min-height: auto;
}

/* Mobile Tickets List */
.mobile-tickets-list {
  display: flex;
  flex-direction: column;
}
.empty-mobile-card {
  padding: 2.5rem 1rem;
  text-align: center;
  color: var(--text-muted);
}

/* Responsive Overrides (< 768px) */
@media (max-width: 767px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }
  .stat-card {
    padding: 1rem 0.75rem;
  }
  .stat-value {
    font-size: 1.5rem;
  }
  .filters {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
    padding: 0.85rem;
  }
  .filter-divider {
    display: none;
  }
  .status-select-box {
    width: 100%;
    border-top: 1px solid var(--border-color);
    padding-top: 0.6rem;
  }
  .search-input, .filter-input {
    font-size: 16px !important;
  }
}
</style>
