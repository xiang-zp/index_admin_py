import api from '@/lib/api'

export type AuthStatus = 'authorized' | 'expired' | 'revoked'
export type AuthLocation = string

export interface AuthCode {
  id: string
  description: string
  invite_code: string
  status: AuthStatus
  auth_location: AuthLocation
  authorized_user: string
  authorized_at: string | null
  expire_time: string
  created_at: string
  updated_at: string
}

export interface AuthCodeCreateRequest {
  description?: string
  invite_code: string
  auth_location: AuthLocation
  start_date: string
  end_date: string
}

export interface AuthCodeUpdateRequest {
  id: string
  description?: string
  auth_location?: AuthLocation
  status?: AuthStatus
  expire_time?: string
}

export const authCodesApi = {
  async getList() {
    const response = await api.get('/admin/auth-codes')
    return response.data
  },

  async create(data: AuthCodeCreateRequest) {
    const response = await api.post('/admin/auth-codes', data)
    return response.data
  },

  async update(data: AuthCodeUpdateRequest) {
    const { id, ...updateData } = data
    const response = await api.put(`/admin/auth-codes/${id}`, updateData)
    return response.data
  },

  async delete(id: string) {
    const response = await api.delete(`/admin/auth-codes/${id}`)
    return response.data
  },

  async revoke(id: string) {
    const response = await api.post(`/admin/auth-codes/${id}/revoke`)
    return response.data
  }
}
