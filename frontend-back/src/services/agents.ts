import api from '@/lib/api'

export interface Agent {
  id: string
  name: string
  api: string
  source: string
  bot_id: string
  is_visible: boolean
  sort_order: number
  created_at: string
  updated_at: string
}

export interface AgentCreateRequest {
  name: string
  api: string
  source: string
  bot_id?: string
  is_visible?: boolean
}

export interface AgentUpdateRequest {
  id: string
  name: string
  api: string
  source: string
  bot_id?: string
  is_visible: boolean
}

export const agentsApi = {
  async getList() {
    const response = await api.get('/admin/agents')
    return response.data
  },

  async create(data: AgentCreateRequest) {
    const response = await api.post('/admin/agents', data)
    return response.data
  },

  async update(data: AgentUpdateRequest) {
    const response = await api.put(`/admin/agents/${data.id}`, data)
    return response.data
  },

  async delete(id: string) {
    const response = await api.delete(`/admin/agents/${id}`)
    return response.data
  },

  async toggleVisible(id: string, is_visible: boolean) {
    const response = await api.patch(`/admin/agents/${id}/toggle`, { is_visible })
    return response.data
  }
}
