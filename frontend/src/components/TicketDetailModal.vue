<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Detalle de Solicitud - {{ ticket.id.substring(0, 8) }}</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <div class="ticket-details">
        <div class="detail-row">
          <span class="label">Estado:</span>
          <span :class="getBadgeClass(ticket.estado)">{{ ticket.estado }}</span>
        </div>
        <p><strong>Solicitante:</strong> {{ ticket.nombre_solicitante }}</p>
        <p><strong>Correo Creador:</strong> {{ ticket.creator_email || 'No asociado' }}</p>
        <p><strong>Depto:</strong> {{ ticket.departamento }} | <strong>Empresa:</strong> {{ ticket.empresa }}</p>
        <p><strong>Tipo de Solicitud:</strong> {{ ticket.tipo_solicitud }}</p>
        <p><strong>Prioridad:</strong> {{ ticket.prioridad || 'No asignada' }}</p>
        <p><strong>Encargado:</strong> {{ ticket.encargado || 'Sin asignar' }}</p>
        
        <div class="description-box">
          <strong>Descripción original:</strong>
          <p>{{ ticket.descripcion }}</p>
        </div>
      </div>
      
      <hr />

      <div class="comments-section" v-if="ticket.motivo_justificacion">
        <h3>Comentarios / Justificación</h3>
        <div class="comment-box">
          <p>{{ ticket.motivo_justificacion }}</p>
        </div>
      </div>
      <div class="comments-section" v-else>
        <p style="color: var(--text-muted); font-style: italic;">Sin comentarios adicionales por parte de la administración.</p>
      </div>
        
      <div class="modal-footer">
        <button type="button" class="btn btn-primary" @click="$emit('close')">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  ticket: Object
})
defineEmits(['close'])

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
</script>

<style scoped>
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex; justify-content: center; align-items: center;
  z-index: 1000;
}
.modal-content {
  background: #fff; padding: 2rem; border-radius: 8px; width: 100%; max-width: 550px;
  max-height: 90vh; overflow-y: auto;
}
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.modal-header h2 { margin: 0; color: var(--text-main); font-size: 1.25rem; }
.close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-muted); }

.ticket-details { font-size: 0.95rem; margin-bottom: 1.5rem; color: var(--text-main); line-height: 1.6; }
.ticket-details p { margin: 0.4rem 0; }
.detail-row { margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }
.label { font-weight: 600; }

.description-box {
  background: var(--bg-color); padding: 1rem; border-radius: 8px; margin-top: 1rem;
}
.description-box p { margin: 0.5rem 0 0 0; white-space: pre-wrap; }

hr { margin: 1.5rem 0; border: 0; border-top: 1px solid var(--border-color); }

.comments-section h3 { font-size: 1.05rem; margin: 0 0 1rem 0; color: var(--primary-color); }
.comment-box { background: rgba(164, 132, 82, 0.1); border-left: 4px solid var(--primary-color); padding: 1rem; border-radius: 0 8px 8px 0; }
.comment-box p { margin: 0; white-space: pre-wrap; color: var(--text-main); }

.modal-footer { margin-top: 2rem; display: flex; justify-content: flex-end; }
</style>
