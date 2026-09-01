
<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Nueva Solicitud</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label>Nombre del Solicitante</label>
          <input type="text" v-model="form.nombre_solicitante" class="form-control" required />
        </div>
        <div class="form-group">
          <label>Empresa</label>
          <select v-model="form.empresa" class="form-control" required>
            <option value="" disabled>Seleccione empresa...</option>
            <option v-for="empresa in opcionesEmpresa" :key="empresa" :value="empresa">{{ empresa }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>Departamento</label>
          <input type="text" v-model="form.departamento" class="form-control" required />
        </div>
        <div class="form-group">
          <label>Tipo de Solicitud</label>
          <select v-model="form.tipo_solicitud" class="form-control" required>
            <option value="" disabled>Seleccione tipo...</option>
            <option v-for="tipo in opcionesTipoSolicitud" :key="tipo" :value="tipo">{{ tipo }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>Descripción</label>
          <textarea v-model="form.descripcion" class="form-control" rows="4" required></textarea>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancelar</button>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Guardando...' : 'Crear Ticket' }}
          </button>
        </div>
        <div v-if="error" class="alert-error">{{ error }}</div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ticketService } from '../services/api'

const emit = defineEmits(['close', 'ticket-created'])

const opcionesEmpresa = [
  'Arturos',
  'Grupo Maralac'
]

const opcionesTipoSolicitud = [
  'Creación de Dashboards',
  'Análisis profundo',
  'Modelos Estadísticos/ML',
  'Troubleshooting',
  'Otros requerimientos'
]

const form = reactive({
  nombre_solicitante: '',
  empresa: '',
  departamento: '',
  tipo_solicitud: '',
  descripcion: ''
})

const loading = ref(false)
const error = ref('')

const submitForm = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await ticketService.createTicket(form)
    emit('ticket-created', res)
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
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
.modal-footer { margin-top: 1.5rem; display: flex; justify-content: flex-end; gap: 0.5rem; }
.alert-error { color: red; margin-top: 1rem; font-size: 0.875rem; }
</style>
