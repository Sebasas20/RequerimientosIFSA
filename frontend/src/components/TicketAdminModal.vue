<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Gestión - #{{ ticket.id.substring(0, 8) }}</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <form @submit.prevent="updateTicket" class="form-wrapper">
        <div class="modal-scroll-body">
          <div class="ticket-details">
            <p><strong>Área Destino:</strong> <span class="badge badge-info">{{ ticket.departamento_destino === 'HELPDESK' ? 'HELPDESK' : 'DATA' }}</span></p>
            <p><strong>Solicitante:</strong> {{ ticket.nombre_solicitante }}</p>
            <p v-if="ticket.detalles_adicionales?.contacto"><strong>Contacto:</strong> {{ ticket.detalles_adicionales.contacto }}</p>
            <p><strong>Correo Creador:</strong> {{ ticket.creator_email || 'No asociado' }}</p>
            <p><strong>Empresa / Depto:</strong> {{ ticket.empresa }} - {{ ticket.departamento }}</p>
            <p><strong>Asunto:</strong> {{ ticket.asunto || ticket.descripcion.substring(0, 50) }}</p>
            <p v-if="ticket.tipo_solicitud"><strong>Tipo Solicitud:</strong> {{ ticket.tipo_solicitud }}</p>
            <p v-if="ticket.detalles_adicionales?.caso"><strong>Caso HelpDesk:</strong> {{ ticket.detalles_adicionales.caso }}</p>
            <p><strong>Descripción:</strong> {{ ticket.descripcion }}</p>
          </div>
          
          <hr />

          <!-- Campo adicional para HelpDesk: Asignación de Caso -->
          <div v-if="ticket.departamento_destino === 'HELPDESK'" class="form-group">
            <label>Clasificación del Caso (HelpDesk)</label>
            <select v-model="form.caso" class="form-control">
              <option value="">Seleccione clasificación...</option>
              <option v-for="casoOpt in opcionesCasoHelpDesk" :key="casoOpt" :value="casoOpt">{{ casoOpt }}</option>
            </select>
          </div>

          <div class="form-group">
            <label>Asignar Prioridad</label>
            <select v-model="form.prioridad" class="form-control">
              <option value="">Ninguna</option>
              <option value="Prioridad 1">Prioridad 1</option>
              <option value="Prioridad 2">Prioridad 2</option>
              <option value="Prioridad 3">Prioridad 3</option>
              <option value="Prioridad 4">Prioridad 4</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>Encargado / Técnico</label>
            <input type="text" v-model="form.encargado" class="form-control" placeholder="Nombre del encargado o técnico" />
          </div>

          <div class="form-group">
            <label>Actualizar Estado</label>
            <select v-model="form.estado" class="form-control" required>
              <option value="Creado / Esperando Asignación">Creado / Esperando Asignación</option>
              <option value="Asignado/Desarrollo">Asignado / En progreso</option>
              <option value="Información Requerida">Información Requerida</option>
              <option value="Pausado">Pausado</option>
              <option value="Cerrado/Resuelto">Cerrado / Resuelto</option>
              <option value="Rechazado/Fuera de Alcance">Rechazado/Fuera de Alcance</option>
            </select>
          </div>
          
          <div class="form-group" v-if="requiresJustification">
            <label>Motivo / Comentarios de Resolución (Requerido)</label>
            <textarea v-model="form.motivo_justificacion" class="form-control" rows="3" required></textarea>
          </div>
          
          <div v-if="error" class="alert-error">{{ error }}</div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancelar</button>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Actualizando...' : 'Guardar Cambios' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ticketService } from '../services/api'

const props = defineProps({
  ticket: Object
})
const emit = defineEmits(['close', 'ticket-updated'])

const opcionesCasoHelpDesk = [
  'Impresión de Facturas',
  'Factura Duplicada',
  'Odoo',
  'Merchant',
  'Printer Fiscal',
  'Confirmación de Zelle',
  'Diferencia Fiscal',
  'Gerencia',
  'Error en el Formato de Impresión de la Factura',
  'Biométrico',
  'Conexión con Bases de Datos',
  'POS de venta',
  'Error en el Contenido de la Factura',
  'Conexión de Red',
  'Impresora',
  'Otros'
]

const form = reactive({
  caso: props.ticket.detalles_adicionales?.caso || '',
  prioridad: props.ticket.prioridad || '',
  encargado: props.ticket.encargado || '',
  estado: props.ticket.estado || 'Creado / Esperando Asignación',
  motivo_justificacion: props.ticket.motivo_justificacion || ''
})

const loading = ref(false)
const error = ref('')

const requiresJustification = computed(() => {
  return ['Rechazado/Fuera de Alcance', 'Pausado', 'Información Requerida', 'Cerrado/Resuelto'].includes(form.estado)
})

const updateTicket = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const payload = {
      prioridad: form.prioridad,
      encargado: form.encargado,
      estado: form.estado,
      motivo_justificacion: form.motivo_justificacion,
      caso: form.caso
    }
    const res = await ticketService.updateTicket(props.ticket.id, payload)
    emit('ticket-updated', res)
    emit('close')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
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
  background: #fff; padding: 1.75rem; border-radius: 12px; width: 100%; max-width: 540px;
  max-height: 90vh; display: flex; flex-direction: column;
}
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.modal-header h2 { margin: 0; font-size: 1.25rem; color: var(--text-main); }
.close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-muted); min-width: 44px; min-height: 44px; }
.form-wrapper { display: flex; flex-direction: column; flex: 1; overflow: hidden; }
.modal-scroll-body { overflow-y: auto; padding-right: 0.25rem; flex: 1; }
.ticket-details { font-size: 0.9rem; margin-bottom: 1rem; color: var(--text-main); line-height: 1.5; }
.ticket-details p { margin: 0.3rem 0; }
hr { margin: 1rem 0; border: 0; border-top: 1px solid var(--border-color); }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; margin-bottom: 0.4rem; font-weight: 500; font-size: 0.9rem; }
.modal-footer { margin-top: 1.25rem; display: flex; justify-content: flex-end; gap: 0.5rem; }
.alert-error { color: red; margin-top: 0.75rem; font-size: 0.875rem; }

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
}
</style>
