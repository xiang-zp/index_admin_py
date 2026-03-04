import { defineStore } from 'pinia'
import api from '@/lib/api'

interface User {
  id: string
  username: string
  role: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: null,
    isAuthenticated: false
  }),

  getters: {
    getUser: (state) => state.user,
    isAdmin: (state) => state.user?.role === 'admin'
  },

  actions: {
    async login(username: string, password: string) {
      try {
        console.debug('Login request:', { username, password })
        
        const response = await api.post('/auth/admin/login', {
          username,
          password
        })
        
        console.debug('Login response:', response.data)
        console.debug('Response code:', response.data.code)
        console.debug('Checking code === 0 or 200:', response.data.code === 0 || response.data.code === 200)
        
        if (response.data.code === 0 || response.data.code === 200) {
          const { token, user } = response.data.data
          this.token = token
          this.user = user
          this.isAuthenticated = true
          localStorage.setItem('admin_token', token)
          localStorage.setItem('admin_user', JSON.stringify(user))
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`
          console.debug('Login success, token:', token)
          console.debug('Returning success: true')
          return { success: true }
        }
        console.debug('Returning failure, message:', response.data.message)
        return { success: false, message: response.data.message }
      } catch (error: any) {
        console.error('Login error:', error)
        if (error.response?.status === 401) {
          return { success: false, message: '用户名或密码错误' }
        }
        if (error.response?.status === 404) {
          return { success: false, message: '后端API未实现，当前为模拟登录模式' }
        }
        return { 
          success: false, 
          message: error.response?.data?.message || '登录失败' 
        }
      }
    },

    async mockLogin(username: string, _password: string) {
      this.token = 'mock-token-' + Date.now()
      this.user = {
        id: '1',
        username: username,
        role: 'admin'
      }
      this.isAuthenticated = true
      localStorage.setItem('admin_token', this.token)
      localStorage.setItem('admin_user', JSON.stringify(this.user))
      localStorage.setItem('mock_mode', 'true')
      api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
      return { success: true }
    },

    logout() {
      this.token = null
      this.user = null
      this.isAuthenticated = false
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_user')
      localStorage.removeItem('mock_mode')
      delete api.defaults.headers.common['Authorization']
    },

    initAuth() {
      const token = localStorage.getItem('admin_token')
      const userStr = localStorage.getItem('admin_user')
      
      console.debug('initAuth - token:', token)
      console.debug('initAuth - userStr:', userStr)
      
      if (token && userStr) {
        this.token = token
        this.user = JSON.parse(userStr)
        this.isAuthenticated = true
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`
        console.debug('initAuth - restored session')
      }
    }
  }
})
