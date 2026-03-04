<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Drawer from '@/components/ui/Drawer.vue'
import { usersApi, type User } from '@/services/users'
import {
  Plus,
  Edit,
  Trash2,
  Users,
  Shield,
  Key,
  Eye,
  EyeOff,
  Calendar,
  Clock
} from 'lucide-vue-next'

const users = ref<User[]>([])
const loading = ref(false)
const visiblePasswords = ref<Set<string>>(new Set())
const drawerOpen = ref(false)
const drawerMode = ref<'add' | 'edit'>('add')

const formData = ref({
  id: '',
  username: '',
  password: '',
  role: 'admin'
})

const roleOptions = [
  { value: 'admin', label: '管理员' },
  { value: 'editor', label: '编辑' },
  { value: 'viewer', label: '只读' }
]

const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0
})

const togglePassword = (id: string) => {
  if (visiblePasswords.value.has(id)) {
    visiblePasswords.value.delete(id)
  } else {
    visiblePasswords.value.add(id)
  }
}

const isPasswordVisible = (id: string) => visiblePasswords.value.has(id)

const resetForm = () => {
  formData.value = { id: '', username: '', password: '', role: 'admin' }
}

const openAddDrawer = () => {
  resetForm()
  drawerMode.value = 'add'
  drawerOpen.value = true
}

const openEditDrawer = (user: User) => {
  formData.value = {
    id: user.id,
    username: user.username,
    password: '',
    role: user.role
  }
  drawerMode.value = 'edit'
  drawerOpen.value = true
}

const closeDrawer = () => {
  drawerOpen.value = false
  resetForm()
}

const handleSave = async () => {
  if (!formData.value.username) {
    alert('请填写用户名')
    return
  }

  if (drawerMode.value === 'add' && !formData.value.password) {
    alert('请填写密码')
    return
  }

  try {
    loading.value = true
    if (drawerMode.value === 'add') {
      const response = await usersApi.create({
        username: formData.value.username,
        password: formData.value.password,
        role: formData.value.role
      })
      if (response.code === 0 || response.code === 200) {
        await fetchUsers()
        closeDrawer()
      } else {
        alert('创建用户失败：' + response.message)
        return
      }
    } else {
      const updateData: any = {
        id: formData.value.id,
        username: formData.value.username,
        role: formData.value.role
      }
      if (formData.value.password) {
        updateData.password = formData.value.password
      }
      const response = await usersApi.update(updateData)
      if (response.code === 0 || response.code === 200) {
        await fetchUsers()
        closeDrawer()
      } else {
        alert('更新用户失败：' + response.message)
        return
      }
    }
  } catch (error: any) {
    console.error('Error saving user:', error)
    console.error('Error response:', error.response)
    console.error('Error request:', error.request)
    console.error('Error config:', error.config)
    
    let errorMessage = '操作失败'
    if (error.response?.data?.message) {
      errorMessage = error.response.data.message
    } else if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail
    } else if (error.message) {
      errorMessage = error.message
    }
    alert(errorMessage)
  } finally {
    loading.value = false
  }
}

const handleDelete = async (id: string) => {
  if (!confirm('确定要删除这个用户吗？')) {
    return
  }

  try {
    loading.value = true
    const response = await usersApi.delete(id)
    if (response.code === 0 || response.code === 200) {
      await fetchUsers()
    } else {
      alert('删除用户失败：' + response.message)
    }
  } catch (error: any) {
    console.error('Error deleting user:', error)
    alert('删除失败：' + (error.response?.data?.message || error.message))
  } finally {
    loading.value = false
  }
}

const formatDate = (date: string | null) => {
  if (!date || date === '-') return '-'
  return date
}

const fetchUsers = async () => {
  try {
    loading.value = true
    console.log('Fetching users...')
    const response = await usersApi.getList()
    console.log('Users response:', response)
    console.log('Response code:', response?.code)
    console.log('Response data:', response?.data)
    if (response?.code === 0 || response?.code === 200) {
      users.value = response.data
      console.log('Users list:', users.value)
      pagination.value.total = users.value.length
    } else {
      console.error('Failed to fetch users:', response?.message)
    }
  } catch (error) {
    console.error('Error fetching users:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<template>
  <div class="h-screen overflow-hidden bg-gradient-to-br from-slate-50 via-gray-50 to-slate-100">
    <div class="max-w-7xl mx-auto px-8 py-6 h-full flex flex-col">
      <!-- Header -->
      <div class="mb-4 flex-shrink-0">
        <div class="flex items-center gap-4 mb-2">
          <div class="p-3 bg-gradient-to-br from-violet-500 to-indigo-600 rounded-2xl shadow-lg shadow-violet-200">
            <Shield class="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-900 via-gray-700 to-gray-600 bg-clip-text text-transparent">
              账号管理
            </h1>
            <p class="text-gray-500 mt-1 font-medium">管理系统管理员账号和权限</p>
          </div>
        </div>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4 flex-shrink-0">
        <Card class="border-0 shadow-lg shadow-gray-200/50 bg-white/80 backdrop-blur-sm hover:shadow-xl transition-shadow duration-300">
          <CardContent class="pt-5">
            <div class="flex items-center gap-4">
              <div class="p-3 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-xl shadow-lg shadow-blue-200">
                <Users class="w-5 h-5 text-white" />
              </div>
              <div>
                <p class="text-xs text-gray-500 font-medium">总账号数</p>
                <p class="text-2xl font-bold text-gray-900">{{ users.length }}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card class="border-0 shadow-lg shadow-gray-200/50 bg-white/80 backdrop-blur-sm hover:shadow-xl transition-shadow duration-300">
          <CardContent class="pt-5">
            <div class="flex items-center gap-4">
              <div class="p-3 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-xl shadow-lg shadow-emerald-200">
                <Shield class="w-5 h-5 text-white" />
              </div>
              <div>
                <p class="text-xs text-gray-500 font-medium">管理员</p>
                <p class="text-2xl font-bold text-gray-900">{{ users.filter(u => u.role === 'admin').length }}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card class="border-0 shadow-lg shadow-gray-200/50 bg-white/80 backdrop-blur-sm hover:shadow-xl transition-shadow duration-300">
          <CardContent class="pt-5">
            <div class="flex items-center gap-4">
              <div class="p-3 bg-gradient-to-br from-amber-400 to-orange-500 rounded-xl shadow-lg shadow-amber-200">
                <Key class="w-5 h-5 text-white" />
              </div>
              <div>
                <p class="text-xs text-gray-500 font-medium">普通用户</p>
                <p class="text-2xl font-bold text-gray-900">{{ users.filter(u => u.role !== 'admin').length }}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Action Button -->
      <div class="flex justify-end mb-3 flex-shrink-0">
        <Button @click="openAddDrawer" class="h-10 px-5 bg-gradient-to-r from-violet-500 to-indigo-600 hover:from-violet-600 hover:to-indigo-700 shadow-lg shadow-violet-200">
          <Plus class="w-4 h-4 mr-2" />
          新增账号
        </Button>
      </div>

      <!-- Table -->
      <Card class="border-0 shadow-xl shadow-gray-200/50 bg-white/90 backdrop-blur-sm overflow-hidden rounded-2xl flex-1 flex flex-col min-h-0">
        <div class="overflow-auto flex-1">
          <table class="w-full">
            <thead class="sticky top-0 z-10">
              <tr class="bg-gradient-to-r from-slate-100 via-gray-100 to-slate-100 border-b-2 border-gray-200">
                <th class="w-28 px-5 py-5 text-left text-sm font-bold text-gray-700 tracking-wide">ID</th>
                <th class="w-32 px-5 py-5 text-left text-sm font-bold text-gray-700 tracking-wide">用户名</th>
                <th class="w-32 px-5 py-5 text-left text-sm font-bold text-gray-700 tracking-wide">密码</th>
                <th class="w-28 px-5 py-5 text-left text-sm font-bold text-gray-700 tracking-wide">角色</th>
                <th class="w-36 px-5 py-5 text-left text-sm font-bold text-gray-700 tracking-wide">
                  <div class="flex items-center gap-2">
                    <Calendar class="w-4 h-4" />
                    创建时间
                  </div>
                </th>
                <th class="w-36 px-5 py-5 text-left text-sm font-bold text-gray-700 tracking-wide">
                  <div class="flex items-center gap-2">
                    <Clock class="w-4 h-4" />
                    最后登录
                  </div>
                </th>
                <th class="w-32 px-5 py-5 text-center text-sm font-bold text-gray-700 tracking-wide">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="7" class="px-4 py-8 text-center">
                  <div class="flex flex-col items-center justify-center gap-3">
                    <div class="w-10 h-10 rounded-full border-2 border-gray-200 border-t-violet-600 animate-spin"></div>
                    <p class="text-gray-500 text-sm">加载中...</p>
                  </div>
                </td>
              </tr>
              <tr v-else-if="users.length === 0">
                <td colspan="7" class="px-4 py-12 text-center">
                  <div class="flex flex-col items-center justify-center gap-3">
                    <Users class="w-12 h-12 text-gray-300" />
                    <p class="text-gray-500 text-sm">暂无用户数据</p>
                  </div>
                </td>
              </tr>
              <tr v-else v-for="user in users" :key="user.id" class="border-b border-gray-50 hover:bg-gradient-to-r hover:from-violet-50/30 hover:to-transparent transition-all duration-300 group">
                <td class="px-4 py-3">
                  <span class="px-3 py-1.5 bg-gradient-to-r from-gray-100 to-gray-50 rounded-lg text-sm font-mono font-medium text-gray-700">
                    {{ user.id }}
                  </span>
                </td>
                <td class="px-4 py-3">
                  <span class="font-medium text-gray-900">{{ user.username }}</span>
                </td>
                <td class="px-4 py-3">
                  <div class="flex items-center gap-2">
                    <code class="px-3 py-1.5 bg-gradient-to-r from-gray-100 to-gray-50 rounded-lg text-sm font-mono">
                      {{ isPasswordVisible(user.id) ? user.password : '••••••' }}
                    </code>
                    <button @click="togglePassword(user.id)" class="p-1.5 hover:bg-violet-50 rounded-lg transition-colors">
                      <Eye v-if="!isPasswordVisible(user.id)" class="w-4 h-4 text-gray-400 group-hover:text-violet-500" />
                      <EyeOff v-else class="w-4 h-4 text-violet-500" />
                    </button>
                  </div>
                </td>
                <td class="px-4 py-3">
                  <span 
                    :class="[
                      'inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold',
                      user.role === 'admin' 
                        ? 'bg-gradient-to-r from-amber-100 to-orange-100 text-amber-700 border border-amber-200' 
                        : 'bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-700 border border-blue-200'
                    ]"
                  >
                    {{ roleOptions.find(r => r.value === user.role)?.label }}
                  </span>
                </td>
                <td class="px-4 py-3">
                  <div class="flex items-center gap-2 text-gray-500">
                    <Calendar class="w-4 h-4" />
                    <span class="text-sm">{{ formatDate(user.created_at) }}</span>
                  </div>
                </td>
                <td class="px-4 py-3">
                  <div class="flex items-center gap-2 text-gray-500">
                    <Clock class="w-4 h-4" />
                    <span class="text-sm">{{ formatDate(user.last_login_at) }}</span>
                  </div>
                </td>
                <td class="px-4 py-3">
                  <div class="flex items-center justify-center gap-2">
                    <Button variant="ghost" size="sm" @click="openEditDrawer(user)" class="hover:bg-violet-50 hover:text-violet-600 transition-colors">
                      <Edit class="w-4 h-4 mr-1" />
                      编辑
                    </Button>
                    <Button variant="ghost" size="sm" @click="handleDelete(user.id)" class="hover:bg-red-50 hover:text-red-600 transition-colors">
                      <Trash2 class="w-4 h-4 mr-1" />
                      删除
                    </Button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="flex items-center justify-between px-6 py-4 border-t border-gray-100 bg-gray-50/50 flex-shrink-0">
          <div class="flex items-center gap-2 text-sm text-gray-500">
            <span class="font-medium">每页 {{ pagination.pageSize }} 条</span>
            <span class="text-gray-300">|</span>
            <span>共 {{ pagination.total }} 条记录</span>
          </div>
          <div class="flex items-center gap-2">
            <Button variant="outline" size="sm" class="hover:bg-white">上一页</Button>
            <Button variant="outline" size="sm" class="min-w-10 bg-white">1</Button>
            <Button variant="outline" size="sm" class="hover:bg-white">下一页</Button>
          </div>
        </div>
      </Card>
    </div>
  </div>

  <!-- Drawer -->
  <Drawer :open="drawerOpen" :title="drawerMode === 'add' ? '新增账号' : '编辑账号'" position="right" width="480px" @close="closeDrawer">
    <div class="p-6 space-y-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          用户名
          <span class="text-red-500 ml-1">*</span>
        </label>
        <Input v-model="formData.username" placeholder="请输入用户名" class="h-11" />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          密码
          <span class="text-red-500 ml-1">*</span>
        </label>
        <Input v-model="formData.password" type="password" placeholder="请输入密码" class="h-11" />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          角色
          <span class="text-red-500 ml-1">*</span>
        </label>
        <select v-model="formData.role" class="w-full h-11 px-4 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-200 focus:border-violet-300 appearance-none cursor-pointer">
          <option v-for="role in roleOptions" :key="role.value" :value="role.value">{{ role.label }}</option>
        </select>
      </div>

      <div class="pt-6 border-t border-gray-100">
        <Button @click="handleSave" class="w-full h-12 bg-gradient-to-r from-violet-500 to-indigo-600 hover:from-violet-600 hover:to-indigo-700 shadow-lg shadow-violet-200">
          {{ drawerMode === 'add' ? '创建账号' : '保存修改' }}
        </Button>
      </div>
    </div>
  </Drawer>
</template>

<style scoped>
tbody tr {
  transition: all 0.2s ease;
}

tbody tr:hover {
  transform: translateX(4px);
}
</style>
