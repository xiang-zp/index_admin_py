import api from '@/lib/api'

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  token: string
  user: {
    id: string
    username: string
    role: string
  }
}

export const authApi = {
  async login(data: LoginRequest) {
    const response = await api.post('/auth/admin/login', data)
    return response.data
  },

  async logout() {
    const response = await api.post('/auth/admin/logout')
    return response.data
  },

  async getProfile() {
    const response = await api.get('/auth/admin/profile')
    return response.data
  }
}
