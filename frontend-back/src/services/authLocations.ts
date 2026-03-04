import api from '@/lib/api'

export interface AuthLocation {
  id: string
  value: string
  label: string
  description: string | null
  created_at: string | null
  updated_at: string | null
}

export interface AuthLocationCreateRequest {
  value: string
  label: string
  description?: string
}

export const authLocationsApi = {
  async getList() {
    const response = await api.get('/admin/auth-locations')
    return response.data
  },

  async create(data: AuthLocationCreateRequest) {
    const response = await api.post('/admin/auth-locations', data)
    return response.data
  },

  async delete(id: string) {
    const response = await api.delete(`/admin/auth-locations/${id}`)
    return response.data
  }
}
