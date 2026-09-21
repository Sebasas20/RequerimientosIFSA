import { reactive } from 'vue'

const token = localStorage.getItem('token')
const userStr = localStorage.getItem('user')

export const authState = reactive({
  token: token || null,
  user: userStr ? JSON.parse(userStr) : null,
  
  get isAuthenticated() {
    return !!this.token
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
  },
  
  logout() {
    this.token = null
    this.user = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }
})
