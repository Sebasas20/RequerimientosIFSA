<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h2>{{ modalTitle }}</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <form @submit.prevent="submitForm" class="form-wrapper">
        <div class="form-body">
          <div class="form-group">
            <label>Nombre del Solicitante</label>
            <input type="text" v-model="form.nombre_solicitante" class="form-control" placeholder="Nombre completo" required />
          </div>
          
          <!-- Solo para HelpDesk: Contacto -->
          <div v-if="departamentoDestino === 'HELPDESK'" class="form-group">
            <label>Contacto</label>
            <input type="text" v-model="form.contacto" class="form-control" placeholder="Ej: Tlf 0414-XXXXXXX / Teams / Ext. 102" required />
          </div>

          <div class="form-group">
            <label>Empresa / Ubicación</label>
            <input type="text" v-model="form.empresa" class="form-control readonly-input" readonly placeholder="Cargando empresa..." style="background-color: #f4f4f6; cursor: not-allowed; font-weight: 500;" />
          </div>

          <div class="form-group">
            <label>Departamento / Sede</label>
            <input type="text" v-model="form.departamento" class="form-control readonly-input" readonly placeholder="Cargando departamento..." style="background-color: #f4f4f6; cursor: not-allowed; font-weight: 500;" />
          </div>

          <div class="form-group">
            <label>Asunto</label>
            <input type="text" v-model="form.asunto" class="form-control" placeholder="Resumen corto de la solicitud o falla" required />
          </div>

          <!-- Para DATA y TRADE: Tipo de solicitud dinámico -->
          <div v-if="departamentoDestino === 'DATA' || departamentoDestino === 'TRADE'" class="form-group">
            <label>{{ departamentoDestino === 'TRADE' ? 'Tipo de Solicitud' : 'Tipo de Solicitud Data' }}</label>
            <select v-model="form.tipo_solicitud" class="form-control" required>
              <option value="" disabled>Seleccione tipo...</option>
              <option v-for="tipo in opcionesTipoSolicitud" :key="tipo" :value="tipo">{{ tipo }}</option>
            </select>
          </div>

          <!-- Solo para TRADE: Medidas (Si Aplica) -->
          <div v-if="departamentoDestino === 'TRADE'" class="form-group">
            <label>Medidas (Si Aplica)</label>
            <input type="text" v-model="form.medidas" class="form-control" placeholder="Ej: 2m x 1.5m (Opcional)" />
          </div>

          <div class="form-group">
            <label>Descripción detallada</label>
            <textarea v-model="form.descripcion" class="form-control" rows="4" placeholder="Describa a detalle su requerimiento o falla..." required></textarea>
          </div>

          <div v-if="error" class="alert-error">{{ error }}</div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancelar</button>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Guardando...' : 'Crear Ticket' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ticketService, categoriaService } from '../services/api'
import { authState } from '../store/auth'

const props = defineProps({
  departamentoDestino: {
    type: String,
    default: 'DATA'
  }
})

const emit = defineEmits(['close', 'ticket-created'])

const modalTitle = computed(() => {
  if (props.departamentoDestino === 'HELPDESK') return 'Nuevo Ticket - HelpDesk / Soporte TI'
  if (props.departamentoDestino === 'TRADE') return 'Nueva Solicitud - Trade Marketing'
  return 'Nueva Solicitud - Requerimientos Data'
})

const opcionesTipoSolicitud = ref([])

const form = reactive({
  departamento_destino: props.departamentoDestino,
  nombre_solicitante: '',
  empresa: '',
  departamento: '',
  contacto: '',
  medidas: '',
  asunto: '',
  tipo_solicitud: ['DATA', 'TRADE'].includes(props.departamentoDestino) ? '' : null,
  descripcion: ''
})

onMounted(async () => {
  if (authState.user) {
    if (authState.user.full_name) form.nombre_solicitante = authState.user.full_name
    if (authState.user.empresa) form.empresa = authState.user.empresa
    if (authState.user.departamento) form.departamento = authState.user.departamento
  }

  if (props.departamentoDestino === 'DATA' || props.departamentoDestino === 'TRADE') {
    try {
      const list = await categoriaService.getCategorias(props.departamentoDestino)
      if (list && list.length > 0) {
        opcionesTipoSolicitud.value = list.map(c => c.nombre)
      } else if (props.departamentoDestino === 'TRADE') {
        opcionesTipoSolicitud.value = ['Fachada Interna', 'Fachada Externa', 'Material POP', 'Vallas', 'Otros']
      }
    } catch (err) {
      console.error(`Error al cargar categorías de ${props.departamentoDestino}:`, err)
      if (props.departamentoDestino === 'TRADE') {
        opcionesTipoSolicitud.value = ['Fachada Interna', 'Fachada Externa', 'Material POP', 'Vallas', 'Otros']
      }
    }
  }
})

const loading = ref(false)
const error = ref('')

const submitForm = async () => {
  loading.value = true
  error.value = ''
  try {
    const detalles_adicionales = {}
    if (props.departamentoDestino === 'HELPDESK' && form.contacto) {
      detalles_adicionales.contacto = form.contacto
    }
    if (props.departamentoDestino === 'TRADE' && form.medidas && form.medidas.trim() !== '') {
      detalles_adicionales.medidas = form.medidas.trim()
    }

    const payload = {
      departamento_destino: props.departamentoDestino,
      nombre_solicitante: form.nombre_solicitante,
      empresa: form.empresa,
      departamento: form.departamento,
      asunto: form.asunto,
      descripcion: form.descripcion,
      tipo_solicitud: ['DATA', 'TRADE'].includes(props.departamentoDestino) ? form.tipo_solicitud : null,
      detalles_adicionales
    }

    const res = await ticketService.createTicket(payload)
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
  background: rgba(8, 6, 13, 0.6);
  backdrop-filter: blur(4px);
  display: flex; justify-content: center; align-items: center;
  z-index: 1000;
}
.modal-content {
  background: #fff; padding: 1.75rem; border-radius: 12px; width: 100%; max-width: 520px;
  max-height: 90vh; display: flex; flex-direction: column;
}
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; }
.modal-header h2 { margin: 0; font-size: 1.25rem; color: var(--text-main); }
.close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-muted); min-width: 44px; min-height: 44px; }
.form-wrapper { display: flex; flex-direction: column; flex: 1; overflow: hidden; }
.form-body { overflow-y: auto; padding-right: 0.25rem; flex: 1; }
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
