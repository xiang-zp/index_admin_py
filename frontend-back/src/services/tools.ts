import api from '@/lib/api'

export interface Tool {
  id: string
  title: string
  description: string
  image: string
  row?: string
  is_visible: boolean
  sort_order: number
  created_at: string
  updated_at: string
  _isTruncated?: boolean
}

export interface ToolCreateRequest {
  title: string
  description: string
  image?: string
  row?: string
  is_visible?: boolean
}

export interface ToolUpdateRequest {
  id: string
  title: string
  description: string
  image?: string
  is_visible: boolean
}

export const toolsApi = {
  async getList() {
    const response = await api.get('/admin/tools')
    return response.data
  },

  async get(id: string) {
    const response = await api.get(`/admin/tools/${id}`)
    return response.data
  },

  async create(data: ToolCreateRequest) {
    const response = await api.post('/admin/tools', data)
    return response.data
  },

  async update(data: ToolUpdateRequest) {
    const response = await api.put(`/admin/tools/${data.id}`, data)
    return response.data
  },

  async delete(id: string) {
    const response = await api.delete(`/admin/tools/${id}`)
    return response.data
  },

  async toggleVisible(id: string) {
    const response = await api.patch(`/admin/tools/${id}/toggle_visibility`)
    return response.data
  }
}
