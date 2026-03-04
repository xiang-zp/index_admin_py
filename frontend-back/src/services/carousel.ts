import api from '@/lib/api'

export interface CarouselItem {
  id: string
  title: string
  description: string
  is_visible: boolean
  sort_order: number
  created_at: string
  updated_at: string
}

export interface CarouselCreateRequest {
  title: string
  description: string
  is_visible?: boolean
}

export interface CarouselUpdateRequest {
  id: string
  title: string
  description: string
  is_visible: boolean
}

export interface ReorderRequest {
  ids: string[]
}

export const carouselApi = {
  async getList() {
    const response = await api.get('/admin/carousels')
    return response.data
  },

  async create(data: CarouselCreateRequest) {
    const response = await api.post('/admin/carousels', data)
    return response.data
  },

  async update(data: CarouselUpdateRequest) {
    const response = await api.put(`/admin/carousels/${data.id}`, data)
    return response.data
  },

  async delete(id: string) {
    const response = await api.delete(`/admin/carousels/${id}`)
    return response.data
  },

  async toggleVisible(id: string, is_visible: boolean) {
    const response = await api.patch(`/admin/carousels/${id}/toggle`, { is_visible })
    return response.data
  },

  async reorder(data: ReorderRequest) {
    const response = await api.put('/admin/carousels/reorder', data)
    return response.data
  }
}
