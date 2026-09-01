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
