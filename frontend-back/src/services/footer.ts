import api from '@/lib/api'

export interface FooterLink {
  id: string
  title: string
  url: string
  sort_order: number
  created_at: string
  updated_at: string
}

export interface FooterConfig {
  logo_url: string
  slogan: string
  links: FooterLink[]
  updated_at: string
}

export interface FooterConfigUpdateRequest {
  logo_url?: string
  slogan?: string
}

export interface FooterLinkCreateRequest {
  title: string
  url: string
}

export interface FooterLinkUpdateRequest {
  id: string
  title: string
  url: string
}

export const footerApi = {
  async getConfig() {
    const response = await api.get('/admin/footer/config')
    return response.data
  },

  async updateConfig(data: FooterConfigUpdateRequest) {
    const response = await api.put('/admin/footer/config', data)
    return response.data
  },

  async getLinks() {
    const response = await api.get('/admin/footer/links')
    return response.data
  },

  async createLink(data: FooterLinkCreateRequest) {
    const response = await api.post('/admin/footer/links', data)
    return response.data
  },

  async updateLink(data: FooterLinkUpdateRequest) {
    const response = await api.put(`/admin/footer/links/${data.id}`, data)
    return response.data
  },

  async deleteLink(id: string) {
    const response = await api.delete(`/admin/footer/links/${id}`)
    return response.data
  }
}
