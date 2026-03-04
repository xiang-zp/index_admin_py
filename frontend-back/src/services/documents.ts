import api from '@/lib/api'

export interface Document {
  id: string
  category: string
  title: string
  description: string
  color: string
  url?: string
  row: string
  is_visible: boolean
  sort_order: number
  created_at: string
  updated_at: string
}

export interface DocumentCreateRequest {
  category: string
  title: string
  description: string
  color: string
  url?: string
  row?: string
  is_visible?: boolean
}

export interface DocumentUpdateRequest {
  id: string
  category: string
  title: string
  description: string
  color: string
  url?: string
  row?: string
  is_visible: boolean
}

export interface Category {
  id: string
  name: string
}

export interface CategoryFull {
  id: number
  name: string
  color: string
  is_active: boolean
  sort_order: number
  created_at: string
  updated_at: string
}

export interface CategoryCreateRequest {
  name: string
  color: string
}

export interface CategoryUpdateRequest {
  name?: string
  color?: string
  is_active?: boolean
}

export const documentsApi = {
  async getList(params?: { category?: string; page?: number; page_size?: number }) {
    const response = await api.get('/admin/documents', { params })
    return response.data
  },

  async getCategories() {
    const response = await api.get('/admin/documents/categories')
    return response.data
  },

  async getCategoriesFull() {
    const response = await api.get('/admin/document-categories')
    return response.data
  },

  async createCategory(data: CategoryCreateRequest) {
    const response = await api.post('/admin/document-categories', data)
    return response.data
  },

  async updateCategory(id: number, data: CategoryUpdateRequest) {
    const response = await api.put(`/admin/document-categories/${id}`, data)
    return response.data
  },

  async deleteCategory(id: number) {
    const response = await api.delete(`/admin/document-categories/${id}`)
    return response.data
  },

  async create(data: DocumentCreateRequest) {
    const response = await api.post('/admin/documents', data)
    return response.data
  },

  async update(data: DocumentUpdateRequest) {
    const response = await api.put(`/admin/documents/${data.id}`, data)
    return response.data
  },

  async delete(id: string) {
    const response = await api.delete(`/admin/documents/${id}`)
    return response.data
  },

  async toggleVisible(id: string, is_visible: boolean) {
    const response = await api.patch(`/admin/documents/${id}/toggle`, { is_visible })
    return response.data
  }
}
