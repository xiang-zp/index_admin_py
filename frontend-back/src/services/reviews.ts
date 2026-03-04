import api from '@/lib/api'

export interface Review {
  id: string
  name: string
  avatar_color: string
  rating: number
  content: string
  created_at: string
  updated_at: string
}

export interface ReviewCreateRequest {
  name: string
  avatar_color?: string
  rating: number
  content: string
}

export interface ReviewUpdateRequest {
  id: string
  name: string
  avatar_color?: string
  rating: number
  content: string
}

export const reviewsApi = {
  async getList(params?: { page?: number; page_size?: number }) {
    const response = await api.get('/admin/reviews', { params })
    return response.data
  },

  async create(data: ReviewCreateRequest) {
    const response = await api.post('/admin/reviews', data)
    return response.data
  },

  async update(data: ReviewUpdateRequest) {
    const response = await api.put(`/admin/reviews/${data.id}`, data)
    return response.data
  },

  async delete(id: string) {
    const response = await api.delete(`/admin/reviews/${id}`)
    return response.data
  }
}
