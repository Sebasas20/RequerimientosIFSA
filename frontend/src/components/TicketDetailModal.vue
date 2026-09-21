<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Detalle - #{{ ticket.id.substring(0, 8) }}</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <div class="modal-scroll-body">
        <div class="ticket-details">
          <div class="detail-row">
            <span class="label">Área:</span>
            <span :class="ticket.departamento_destino === 'HELPDESK' ? 'badge badge-info' : 'badge badge-secondary'">
              {{ ticket.departamento_destino === 'HELPDESK' ? 'HELPDESK' : 'DATA' }}
            </span>
            <span class="label" style="margin-left: 0.5rem;">Estado:</span>
            <span :class="getBadgeClass(ticket.estado)">{{ ticket.estado }}</span>
          </div>
          <p><strong>Asunto:</strong> {{ ticket.asunto || ticket.descripcion.substring(0, 50) }}</p>
          <p><strong>Solicitante:</strong> {{ ticket.nombre_solicitante }}</p>
          <p v-if="ticket.detalles_adicionales?.contacto"><strong>Contacto:</strong> {{ ticket.detalles_adicionales.contacto }}</p>
          <p><strong>Correo Creador:</strong> {{ ticket.creator_email || 'No asociado' }}</p>
          <p><strong>Empresa / Depto:</strong> {{ ticket.empresa }} - {{ ticket.departamento }}</p>
          <p v-if="ticket.tipo_solicitud"><strong>Tipo de Solicitud:</strong> {{ ticket.tipo_solicitud }}</p>
          <p v-if="ticket.detalles_adicionales?.caso"><strong>Clasificación del Caso:</strong> {{ ticket.detalles_adicionales.caso }}</p>
          <p><strong>Prioridad:</strong> {{ ticket.prioridad || 'No asignada' }}</p>
          <p><strong>Encargado / Técnico:</strong> {{ ticket.encargado || 'Sin asignar' }}</p>
          
          <div class="description-box">
            <strong>Descripción original:</strong>
            <p>{{ ticket.descripcion }}</p>
          </div>
        </div>
        
        <hr />

        <div class="comments-section" v-if="ticket.motivo_justificacion">
          <h3>Comentarios / Justificación / Solución</h3>
          <div class="comment-box">
            <p>{{ ticket.motivo_justificacion }}</p>
          </div>
        </div>
        <div class="comments-section" v-else>
          <p style="color: var(--text-muted); font-style: italic;">Sin comentarios adicionales por parte de la administración.</p>
        </div>
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
    case 'Cerrado/Resuelto': return 'badge badge-success'
    case 'Rechazado/Fuera de Alcance': return 'badge badge-danger'
    default: return 'badge badge-secondary'
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(8, 6, 13, 0.6);
  backdrop-filter: blur(4px);
  display: flex; justify-content: center; align-items: center;
  z-index: 1000;
}
.modal-content {
  background: #fff; padding: 1.75rem; border-radius: 12px; width: 100%; max-width: 550px;
  max-height: 90vh; display: flex; flex-direction: column;
}
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; }
.modal-header h2 { margin: 0; color: var(--text-main); font-size: 1.25rem; }
.close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-muted); min-width: 44px; min-height: 44px; }
.modal-scroll-body { overflow-y: auto; padding-right: 0.25rem; flex: 1; }

.ticket-details { font-size: 0.95rem; margin-bottom: 1.25rem; color: var(--text-main); line-height: 1.6; }
.ticket-details p { margin: 0.4rem 0; }
.detail-row { margin-bottom: 0.85rem; display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; }
.label { font-weight: 600; }

.description-box {
  background: var(--bg-color); padding: 1rem; border-radius: 8px; margin-top: 1rem;
}
.description-box p { margin: 0.5rem 0 0 0; white-space: pre-wrap; }

hr { margin: 1.25rem 0; border: 0; border-top: 1px solid var(--border-color); }

.comments-section h3 { font-size: 1.05rem; margin: 0 0 0.75rem 0; color: var(--primary-color); }
.comment-box { background: rgba(164, 132, 82, 0.1); border-left: 4px solid var(--primary-color); padding: 1rem; border-radius: 0 8px 8px 0; }
.comment-box p { margin: 0; white-space: pre-wrap; color: var(--text-main); }

.modal-footer { margin-top: 1.25rem; display: flex; justify-content: flex-end; }

@media (max-width: 767px) {
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
  .modal-footer .btn { width: 100%; }
}
</style>
