
<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Gestión de Ticket - {{ ticket.id.substring(0, 8) }}</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <div class="ticket-details">
        <p><strong>Solicitante:</strong> {{ ticket.nombre_solicitante }}</p>
        <p><strong>Correo del Creador:</strong> {{ ticket.creator_email || 'No asociado' }}</p>
        <p><strong>Depto:</strong> {{ ticket.departamento }} | <strong>Empresa:</strong> {{ ticket.empresa }}</p>
        <p><strong>Tipo:</strong> {{ ticket.tipo_solicitud }}</p>
        <p><strong>Descripción:</strong> {{ ticket.descripcion }}</p>
      </div>
      
      <hr />

      <form @submit.prevent="updateTicket">
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
          <label>Analista Encargado</label>
          <input type="text" v-model="form.encargado" class="form-control" placeholder="Nombre o ID del analista" />
        </div>

        <div class="form-group">
          <label>Actualizar Estado</label>
          <select v-model="form.estado" class="form-control" required>
            <option value="Creado / Esperando Asignación">Creado / Esperando Asignación</option>
            <option value="Asignado/Desarrollo">Asignado/Desarrollo</option>
            <option value="Información Requerida">Información Requerida</option>
            <option value="Pausado">Pausado</option>
            <option value="Rechazado/Fuera de Alcance">Rechazado/Fuera de Alcance</option>
          </select>
        </div>
        
        <div class="form-group" v-if="requiresJustification">
          <label>Motivo / Justificación (Requerido)</label>
          <textarea v-model="form.motivo_justificacion" class="form-control" rows="3" required></textarea>
        </div>
        
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancelar</button>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Actualizando...' : 'Guardar Cambios' }}
          </button>
        </div>
        <div v-if="error" class="alert-error">{{ error }}</div>
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

const form = reactive({
  prioridad: props.ticket.prioridad || '',
  encargado: props.ticket.encargado || '',
  estado: props.ticket.estado || 'Creado / Esperando Asignación',
  motivo_justificacion: props.ticket.motivo_justificacion || ''
})

const loading = ref(false)
const error = ref('')

const requiresJustification = computed(() => {
  return ['Rechazado/Fuera de Alcance', 'Pausado', 'Información Requerida'].includes(form.estado)
})

const updateTicket = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const res = await ticketService.updateTicket(props.ticket.id, form)
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
  background: rgba(0,0,0,0.5);
  display: flex; justify-content: center; align-items: center;
  z-index: 1000;
}
.modal-content {
  background: #fff; padding: 2rem; border-radius: 8px; width: 100%; max-width: 500px;
}
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; }
.ticket-details { font-size: 0.9rem; margin-bottom: 1.5rem; color: #555; }
.ticket-details p { margin: 0.2rem 0; }
hr { margin-bottom: 1.5rem; border: 0; border-top: 1px solid #eee; }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
.modal-footer { margin-top: 1.5rem; display: flex; justify-content: flex-end; gap: 0.5rem; }
.alert-error { color: red; margin-top: 1rem; font-size: 0.875rem; }
</style>
