import { reactive } from 'vue'

function decodeJwtPayload(token) {
  if (!token) return null
  try {
    const parts = token.split('.')
    if (parts.length < 2) return null
    const base64 = parts[1].replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )
    return JSON.parse(jsonPayload)
  } catch (e) {
    return null
  }
}

export function getTokenExpMs(token) {
  const payload = decodeJwtPayload(token)
  if (!payload || !payload.exp) return null
  return payload.exp * 1000
}

export function isTokenExpired(token) {
  const expMs = getTokenExpMs(token)
  if (!expMs) return true
  return Date.now() >= expMs
}

const initialToken = localStorage.getItem('token')
const initialUser = localStorage.getItem('user')

let validToken = initialToken
let validUser = initialUser ? JSON.parse(initialUser) : null

if (initialToken && isTokenExpired(initialToken)) {
  validToken = null
  validUser = null
  localStorage.removeItem('token')
  localStorage.removeItem('user')
}

let logoutTimer = null
let heartbeatInterval = null

export const authState = reactive({
  token: validToken || null,
  user: validUser,
  
  get isAuthenticated() {
    if (!this.token) return false
    if (isTokenExpired(this.token)) {
      this.logout()
      return false
    }
    return true
  },
  
  get isAdmin() {
    return this.user && this.user.role === 'Administrador'
  },
  
  get canManageTickets() {
    return this.user && ['Administrador', 'Admin Data', 'Admin HelpDesk'].includes(this.user.role)
  },

  get isAdminData() {
    return this.user && this.user.role === 'Admin Data'
  },

  get isAdminHelpDesk() {
    return this.user && this.user.role === 'Admin HelpDesk'
  },

  get isAreaAdmin() {
    return this.user && ['Admin Data', 'Admin HelpDesk'].includes(this.user.role)
  },
  
  login(tokenData, userData) {
    this.token = tokenData
    this.user = userData
    localStorage.setItem('token', tokenData)
    localStorage.setItem('user', JSON.stringify(userData))
    this.startExpirationMonitoring()
  },
  
  logout() {
    this.token = null
    this.user = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    this.stopExpirationMonitoring()

    if (typeof window !== 'undefined' && window.location.pathname !== '/login') {
      window.location.href = '/login'
    }
  },

  startExpirationMonitoring() {
    this.stopExpirationMonitoring()
    
    if (!this.token) return
    
    const expMs = getTokenExpMs(this.token)
    if (!expMs) return

    const msRemaining = expMs - Date.now()
    if (msRemaining <= 0) {
      this.logout()
      return
    }

    // 1. Timer programado exactamente para el instante de vencimiento del token
    logoutTimer = setTimeout(() => {
      this.logout()
    }, msRemaining)

    // 2. Monitoreo pasivo continuo cada 5 segundos (cubre estados de reposo e inactividad)
    heartbeatInterval = setInterval(() => {
      if (this.token && isTokenExpired(this.token)) {
        this.logout()
      }
    }, 5000)
  },

  stopExpirationMonitoring() {
    if (logoutTimer) {
      clearTimeout(logoutTimer)
      logoutTimer = null
    }
    if (heartbeatInterval) {
      clearInterval(heartbeatInterval)
      heartbeatInterval = null
    }
  }
})

// Iniciar monitoreo proactivo al cargar el estado
if (authState.token) {
  authState.startExpirationMonitoring()
}

// Reactividad inmediata al cambiar de pestaña o volver a enfocar la ventana
if (typeof window !== 'undefined') {
  const checkExpOnFocusOrVisibility = () => {
    if (authState.token && isTokenExpired(authState.token)) {
      authState.logout()
    }
  }
  window.addEventListener('focus', checkExpOnFocusOrVisibility)
  document.addEventListener('visibilitychange', checkExpOnFocusOrVisibility)
}
