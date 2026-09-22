import { authState } from '../store/auth';

const API_URL = import.meta.env.VITE_API_URL || '/api';

const getHeaders = () => {
    const headers = {
        'Content-Type': 'application/json'
    };
    if (authState.token) {
        headers['Authorization'] = `Bearer ${authState.token}`;
    }
    return headers;
};

const handleResponse = async (response) => {
    if (response.status === 401) {
        authState.logout();
        window.location.href = '/login';
        throw new Error('Sesión expirada');
    }
    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.error || 'Error en la petición');
    }
    return response.json();
};

export const authService = {
    async login(email, password) {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        return handleResponse(res);
    },
    async getMe() {
        const res = await fetch(`${API_URL}/auth/me`, { headers: getHeaders() });
        return handleResponse(res);
    }
};

export const userService = {
    async getUsers() {
        const res = await fetch(`${API_URL}/users/`, { headers: getHeaders() });
        return handleResponse(res);
    },
    async createUser(userData) {
        const res = await fetch(`${API_URL}/users/`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(userData)
        });
        return handleResponse(res);
    }
};

export const ticketService = {
  async getTickets(filters = {}) {
    const params = new URLSearchParams();
    if (filters.departamento_destino) params.append('departamento_destino', filters.departamento_destino);
    if (filters.estado) params.append('estado', filters.estado);
    if (filters.departamento) params.append('departamento', filters.departamento);
    if (filters.search) params.append('search', filters.search);
    
    const res = await fetch(`${API_URL}/tickets/?${params.toString()}`, { 
        cache: 'no-store',
        headers: getHeaders()
    });
    return handleResponse(res);
  },
  
  async createTicket(data) {
    const res = await fetch(`${API_URL}/tickets/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data)
    });
    return handleResponse(res);
  },

  async updateTicket(id, data) {
    const res = await fetch(`${API_URL}/tickets/${id}`, {
      method: 'PATCH',
      headers: getHeaders(),
      body: JSON.stringify(data)
    });
    return handleResponse(res);
  }
};

export const encargadoService = {
  async getEncargados(departamento_destino = '') {
    const params = new URLSearchParams();
    if (departamento_destino) params.append('departamento_destino', departamento_destino);
    const res = await fetch(`${API_URL}/encargados/?${params.toString()}`, {
      headers: getHeaders()
    });
    return handleResponse(res);
  },

  async createEncargado(data) {
    const res = await fetch(`${API_URL}/encargados/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data)
    });
    return handleResponse(res);
  },

  async deleteEncargado(id) {
    const res = await fetch(`${API_URL}/encargados/${id}`, {
      method: 'DELETE',
      headers: getHeaders()
    });
    return handleResponse(res);
  }
};

export const categoriaService = {
  async getCategorias(departamento_destino = '') {
    const params = new URLSearchParams();
    if (departamento_destino) params.append('departamento_destino', departamento_destino);
    const res = await fetch(`${API_URL}/categorias/?${params.toString()}`, {
      headers: getHeaders()
    });
    return handleResponse(res);
  },

  async createCategoria(data) {
    const res = await fetch(`${API_URL}/categorias/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data)
    });
    return handleResponse(res);
  },

  async deleteCategoria(id) {
    const res = await fetch(`${API_URL}/categorias/${id}`, {
      method: 'DELETE',
      headers: getHeaders()
    });
    return handleResponse(res);
  }
};
