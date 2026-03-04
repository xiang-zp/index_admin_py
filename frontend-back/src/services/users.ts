import api from '@/lib/api';

export interface User {
  id: string;
  username: string;
  password: string;
  role: string;
  last_login_at: string;
  created_at: string;
  updated_at: string;
}

export interface UserCreate {
  username: string;
  password: string;
  role: string;
}

export interface UserUpdate {
  id: string;
  username: string;
  password?: string;
  role: string;
}

export const usersApi = {
  async getList() {
    const response = await api.get('/admin/users');
    return response.data;
  },
  async create(data: UserCreate) {
    const response = await api.post('/admin/users', data);
    return response.data;
  },
  async update(data: UserUpdate) {
    const response = await api.put('/admin/users', data);
    return response.data;
  },
  async delete(id: string) {
    const response = await api.delete('/admin/users', { data: { id } });
    return response.data;
  }
};
