import api from '@/lib/api'

export interface DashboardStats {
  agents: number
  tools: number
  documents: number
  reviews: number
  users: number
}

export interface Activity {
  id: number
  db_id?: string
  type: string
  message: string
  time: string
  user_id?: string
  username?: string
  target_id?: string
  target_type?: string
}

export const dashboardApi = {
  async getStats() {
    const response = await api.get('/admin/dashboard/stats')
    return response.data
  },

  async getActivities(limit: number = 10) {
    const response = await api.get('/admin/dashboard/activities', {
      params: { limit }
    })
    return response.data
  },

  async deleteActivity(activityId: string) {
    const response = await api.delete(`/admin/dashboard/activities/${activityId}`)
    return response.data
  },

  async deleteAllActivities() {
    const response = await api.delete('/admin/dashboard/activities/all')
    return response.data
  }
}