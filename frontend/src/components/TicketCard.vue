<template>
  <div class="ticket-card card">
    <!-- Header de Tarjeta -->
    <div class="card-header">
      <div class="header-left">
        <span class="ticket-id" :title="ticket.id">#{{ ticket.id.substring(0, 8) }}</span>
        <span v-if="!isAreaAdmin" :class="ticket.departamento_destino === 'HELPDESK' ? 'badge badge-info' : 'badge badge-secondary'">
          {{ ticket.departamento_destino === 'HELPDESK' ? 'HELPDESK' : 'DATA' }}
        </span>
      </div>
      <div class="header-right">
        <span v-if="ticket.prioridad" class="badge badge-priority">
          {{ ticket.prioridad }}
        </span>
        <span :class="getBadgeClass(ticket.estado)">
          {{ ticket.estado }}
        </span>
      </div>
    </div>

    <!-- Cuerpo de Tarjeta -->
    <div class="card-body">
      <h3 class="ticket-subject">{{ ticket.asunto || ticket.descripcion }}</h3>
      
      <div class="ticket-meta">
        <div class="meta-row">
          <span class="meta-icon">👤</span>
          <span class="meta-text"><strong>{{ ticket.nombre_solicitante }}</strong></span>
        </div>
        <div class="meta-row" v-if="ticket.departamento || ticket.empresa">
          <span class="meta-icon">🏢</span>
          <span class="meta-text">{{ ticket.empresa ? ticket.empresa + ' - ' : '' }}{{ ticket.departamento || '-' }}</span>
        </div>
        <div class="meta-row" v-if="ticket.tipo_solicitud">
          <span class="meta-icon">📌</span>
          <span class="meta-text">{{ ticket.tipo_solicitud }}</span>
        </div>
        <div class="meta-row" v-if="!isAreaAdmin && ticket.encargado">
          <span class="meta-icon">🛠️</span>
          <span class="meta-text">Encargado: <strong>{{ ticket.encargado }}</strong></span>
        </div>
      </div>
    </div>

    <!-- Pie de Tarjeta -->
    <div class="card-footer">
      <button v-if="canManage" class="btn btn-secondary action-btn" @click="$emit('open-admin', ticket)">
        Gestionar
      </button>
      <button v-else class="btn btn-secondary action-btn" @click="$emit('open-detail', ticket)">
        Ver Detalles
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  ticket: {
    type: Object,
    required: true
  },
  canManage: {
    type: Boolean,
    default: false
  },
  isAreaAdmin: {
    type: Boolean,
    default: false
  }
})

defineEmits(['open-admin', 'open-detail'])

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
</script>

<style scoped>
.ticket-card {
  padding: 1.2rem;
  margin-bottom: 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  background-color: var(--surface-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.ticket-card:active {
  transform: scale(0.99);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.header-left, .header-right {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.ticket-id {
  font-family: monospace;
  font-weight: 700;
  font-size: 0.85rem;
  color: var(--text-muted);
  background: rgba(0,0,0,0.05);
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
}

.badge-priority {
  background-color: rgba(164, 132, 82, 0.15);
  color: var(--primary-color);
  border: 1px solid rgba(164, 132, 82, 0.3);
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.ticket-subject {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.35;
}

.ticket-meta {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-muted);
}

.meta-icon {
  font-size: 0.9rem;
  opacity: 0.8;
}

.meta-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 0.6rem;
  border-top: 1px solid var(--border-color);
}

.action-btn {
  min-height: 44px;
  min-width: 120px;
  padding: 0.6rem 1.2rem;
  font-weight: 600;
  font-size: 0.9rem;
  border-radius: 8px;
}
</style>
