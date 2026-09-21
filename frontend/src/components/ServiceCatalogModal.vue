<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content card catalog-modal">
      <div class="modal-header">
        <h2>Catálogo de Servicios</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      <p class="catalog-subtitle">Selecciona el área encargada de atender tu solicitud:</p>

      <div class="catalog-grid">
        <!-- Tarjeta DATA (Oculta si es Usuario Arturos) -->
        <div 
          v-if="!isArturosUser"
          class="service-card" 
          @click="$emit('select-service', 'BI')">
          <div class="service-icon">📊</div>
          <div class="service-content">
            <h3>Solicitudes de Datos y Analítica</h3>
            <p>Creación de dashboards, análisis profundo, modelos de ML, troubleshooting de datos y reportes.</p>
          </div>
          <span class="btn-select">Crear Solicitud Data &rarr;</span>
        </div>

        <!-- Tarjeta HelpDesk -->
        <div class="service-card" @click="$emit('select-service', 'HELPDESK')">
          <div class="service-icon">💻</div>
          <div class="service-content">
            <h3>HelpDesk & Soporte TI</h3>
            <p>Asistencia con impresoras fiscales, Merchant, Odoo, hardware, red, biométrico o POS en tienda y oficina.</p>
          </div>
          <span class="btn-select">Crear Ticket HelpDesk &rarr;</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  userRole: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close', 'select-service'])

const isArturosUser = computed(() => props.userRole === 'Usuario Arturos')
</script>

<style scoped>
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(8, 6, 13, 0.6);
  backdrop-filter: blur(4px);
  display: flex; justify-content: center; align-items: center;
  z-index: 1000;
}
.catalog-modal {
  width: 90%; max-width: 700px; padding: 2rem; border-radius: 16px;
}
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
.modal-header h2 { margin: 0; font-size: 1.35rem; color: var(--text-main); }
.close-btn { background: none; border: none; font-size: 1.75rem; cursor: pointer; color: var(--text-muted); min-width: 44px; min-height: 44px; }
.catalog-subtitle { color: var(--text-muted); margin-bottom: 1.5rem; }

.catalog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.25rem;
}

.service-card {
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.25s ease-in-out;
  display: flex;
  flex-direction: column;
  background-color: var(--surface-color);
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-color);
}

.service-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.service-content {
  flex-grow: 1;
}

.service-card h3 {
  margin: 0 0 0.5rem 0;
  color: var(--text-main);
  font-size: 1.15rem;
}

.service-card p {
  color: var(--text-muted);
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 1.5rem;
}

.btn-select {
  color: var(--primary-color);
  font-weight: 600;
  font-size: 0.95rem;
  display: inline-block;
  margin-top: auto;
}

@media (max-width: 767px) {
  .catalog-modal {
    width: 100%;
    max-width: 100%;
    padding: 1.25rem;
    border-radius: 20px 20px 0 0;
  }
  .catalog-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
    overflow-y: auto;
    max-height: 70vh;
    padding-bottom: 1rem;
  }
  .service-card {
    padding: 1.2rem;
    flex-direction: row;
    align-items: center;
    gap: 1rem;
  }
  .service-icon {
    font-size: 2rem;
    margin-bottom: 0;
  }
  .service-card p {
    margin-bottom: 0.4rem;
    font-size: 0.85rem;
  }
  .btn-select {
    font-size: 0.85rem;
  }
}
</style>
