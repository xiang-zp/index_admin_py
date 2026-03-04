<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Drawer from '@/components/ui/Drawer.vue'
import { reviewsApi } from '@/services/reviews'
import {
  Plus,
  Edit,
  Trash2,
  Search,
  RefreshCw,
  Star,
  MessageSquare,
  Calendar,
  Quote
} from 'lucide-vue-next'

interface Review {
  id: string
  name: string
  avatar_color: string
  rating: number
  content: string
  created_at: string
}

const reviews = ref<Review[]>([])
const editingId = ref<string | null>(null)
const loading = ref(false)
const drawerOpen = ref(false)
const drawerMode = ref<'add' | 'edit'>('add')
const drawerError = ref<string | null>(null)

const searchForm = ref({
  name: ''
})

const formData = ref({
  name: '',
  avatar_color: 'indigo',
  rating: 5,
  content: ''
})

const drawerFormData = ref({
  name: '',
  avatar_color: 'indigo',
  rating: 5,
  content: ''
})

const avatarColors = [
  { value: 'indigo', label: '靛蓝', bg: 'bg-indigo-500', ring: 'ring-indigo-200' },
  { value: 'emerald', label: '翡翠', bg: 'bg-emerald-500', ring: 'ring-emerald-200' },
  { value: 'rose', label: '玫瑰', bg: 'bg-rose-500', ring: 'ring-rose-200' },
  { value: 'amber', label: '琥珀', bg: 'bg-amber-500', ring: 'ring-amber-200' },
  { value: 'violet', label: '紫罗兰', bg: 'bg-violet-500', ring: 'ring-violet-200' },
  { value: 'teal', label: '青色', bg: 'bg-teal-500', ring: 'ring-teal-200' }
]

const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0
})

const filteredReviews = computed(() => {
  if (!searchForm.value.name) return reviews.value
  const name = searchForm.value.name.toLowerCase()
  return reviews.value.filter(r => 
    r.name.toLowerCase().includes(name) ||
    r.content.toLowerCase().includes(name)
  )
})

const resetForm = () => {
  formData.value = { name: '', avatar_color: 'indigo', rating: 5, content: '' }
}

const startEdit = (review: Review) => {
  editingId.value = review.id
  formData.value = {
    name: review.name,
    avatar_color: review.avatar_color,
    rating: review.rating,
    content: review.content
  }
}

const cancelEdit = () => {
  editingId.value = null
  resetForm()
}

const saveEdit = async () => {
  if (!formData.value.name || !formData.value.content) {
    return
  }

  if (editingId.value) {
    try {
      await reviewsApi.update({
        id: editingId.value,
        name: formData.value.name,
        avatar_color: formData.value.avatar_color,
        rating: formData.value.rating,
        content: formData.value.content
      })
      await loadReviews()
    } catch (error) {
      console.error('更新用户评价失败:', error)
      alert('更新失败，请重试')
    }
  }

  editingId.value = null
  resetForm()
}

const handleDelete = async (id: string) => {
  if (!confirm('确定要删除这个用户评价吗？')) return
  
  try {
    await reviewsApi.delete(id)
    await loadReviews()
  } catch (error) {
    console.error('删除用户评价失败:', error)
    alert('删除失败，请重试')
  }
}

const handleSearch = () => {
  loading.value = true
  setTimeout(() => loading.value = false, 300)
}

const handleReset = () => {
  searchForm.value = { name: '' }
}

const handleAdd = () => {
  openDrawer('add')
}

const openDrawer = (mode: 'add' | 'edit', review?: Review) => {
  drawerMode.value = mode
  drawerError.value = null
  
  if (mode === 'add') {
    drawerFormData.value = {
      name: '',
      avatar_color: 'indigo',
      rating: 5,
      content: ''
    }
  } else if (review) {
    drawerFormData.value = {
      name: review.name,
      avatar_color: review.avatar_color,
      rating: review.rating,
      content: review.content
    }
  }
  
  drawerOpen.value = true
}

const closeDrawer = () => {
  drawerOpen.value = false
}

const handleSubmitDrawer = async () => {
  if (!drawerFormData.value.name || !drawerFormData.value.content) {
    drawerError.value = '请填写用户名和评价内容'
    return
  }
  
  try {
    if (drawerMode.value === 'add') {
      await reviewsApi.create({
        name: drawerFormData.value.name,
        avatar_color: drawerFormData.value.avatar_color,
        rating: drawerFormData.value.rating,
        content: drawerFormData.value.content
      })
    } else {
      // 编辑模式，需要知道编辑的是哪个评价
      // 目前编辑模式是行内编辑，所以这里可能不需要
    }
    
    await loadReviews()
    closeDrawer()
  } catch (error) {
    console.error(`${drawerMode.value === 'add' ? '创建' : '更新'}用户评价失败:`, error)
    drawerError.value = `${drawerMode.value === 'add' ? '创建' : '更新'}失败，请重试`
  }
}

const renderStars = (rating: number) => {
  return Array(5).fill(0).map((_, i) => i < rating)
}

const getColorClass = (color: string) => {
  return avatarColors.find(c => c.value === color) || avatarColors[0]
}

const getInitials = (name: string) => {
  return name ? name.charAt(0).toUpperCase() : '?'
}

const formatDate = (date: string) => {
  const d = new Date(date)
  return d.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

const loadReviews = async () => {
  try {
    const response = await reviewsApi.getList({ page_size: 100 })
    if (response?.code === 200 || response?.code === 0) {
      reviews.value = Array.isArray(response.data?.list) ? response.data.list : []
      pagination.value.total = response.data?.total || reviews.value.length
    }
  } catch (error) {
    console.error('加载用户评价失败:', error)
  }
}

onMounted(() => {
  loadReviews()
})
</script>

<template>
  <div class="h-screen overflow-hidden bg-gradient-to-br from-stone-50 via-slate-50 to-stone-100">
    <div class="max-w-7xl mx-auto px-8 py-6 h-full flex flex-col">
      <div class="mb-4 flex-shrink-0">
        <div class="flex items-center gap-4 mb-2">
          <div class="p-3 bg-gradient-to-br from-indigo-500 to-violet-600 rounded-2xl shadow-lg shadow-indigo-200">
            <MessageSquare class="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-900 via-gray-700 to-gray-600 bg-clip-text text-transparent">
              用户评价管理
            </h1>
            <p class="text-gray-500 mt-1 font-medium">管理前台显示的用户评价</p>
          </div>
        </div>
      </div>

      <div class="grid gap-4 mb-4 flex-shrink-0">
        <Card class="border-0 shadow-xl shadow-gray-200/50 bg-white/80 backdrop-blur-sm">
          <CardContent class="py-4 px-5">
            <div class="flex flex-wrap gap-4 items-center">
              <div class="flex-1 min-w-[240px]">
                <div class="relative">
                  <Search class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <Input 
                    v-model="searchForm.name"
                    placeholder="搜索用户名或评价内容..." 
                    class="pl-12 h-10 bg-gray-50/50 border-gray-200 focus:bg-white transition-all duration-300"
                  />
                </div>
              </div>
              <div class="flex gap-3">
                <Button variant="outline" @click="handleReset" class="h-10 px-5 hover:bg-gray-50">
                  <RefreshCw class="w-4 h-4 mr-2" />
                  重置
                </Button>
                <Button @click="handleSearch" class="h-10 px-5 bg-gradient-to-r from-indigo-500 to-violet-600 hover:from-indigo-600 hover:to-violet-700 shadow-lg shadow-indigo-200">
                  <Search class="w-4 h-4 mr-2" />
                  搜索
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        <div class="flex justify-end">
          <Button @click="handleAdd" class="h-10 px-5 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 shadow-lg shadow-emerald-200">
            <Plus class="w-4 h-4 mr-2" />
            新增评价
          </Button>
        </div>
      </div>

      <Card class="border-0 shadow-xl shadow-gray-200/50 bg-white/90 backdrop-blur-sm overflow-hidden rounded-2xl flex-1 flex flex-col min-h-0">
        <div class="overflow-auto flex-1">
          <table class="w-full">
            <thead class="sticky top-0 z-10">
              <tr class="bg-gradient-to-r from-slate-100 via-gray-100 to-slate-100 border-b-2 border-gray-200">
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide">编号</th>
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide">用户</th>
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide">评分</th>
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide w-80">评价内容</th>
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide">
                  <div class="flex items-center gap-2">
                    <Calendar class="w-4 h-4" />
                    日期
                  </div>
                </th>
                <th class="text-center py-5 px-6 font-bold text-gray-700 text-sm tracking-wide">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr 
                v-for="review in filteredReviews" 
                :key="review.id"
                class="hover:bg-gradient-to-r hover:from-indigo-50/50 hover:via-blue-50/30 hover:to-cyan-50/20 transition-all duration-300 group"
              >
                <td class="py-4 px-6">
                  <span class="font-mono text-sm text-gray-500">{{ review.id }}</span>
                </td>
                <td class="py-4 px-5">
                  <div v-if="editingId !== review.id" class="flex items-center gap-3">
                    <div :class="['avatar-bounce w-10 h-10 rounded-xl flex items-center justify-center text-white font-semibold shadow-lg', getColorClass(review.avatar_color).bg]">
                      {{ getInitials(review.name) }}
                    </div>
                    <span class="font-medium text-gray-900">{{ review.name || '未命名用户' }}</span>
                  </div>
                  <div v-else class="flex items-center gap-3">
                    <div :class="['w-10 h-10 rounded-xl flex items-center justify-center text-white font-semibold shadow-lg', getColorClass(formData.avatar_color).bg]">
                      {{ getInitials(formData.name) }}
                    </div>
                    <Input v-model="formData.name" class="w-32 h-9" placeholder="用户名" />
                  </div>
                </td>
                <td class="py-4 px-5">
                  <div v-if="editingId !== review.id" class="flex items-center gap-1">
                    <Star 
                      v-for="(_, i) in renderStars(review.rating)" 
                      :key="'filled-' + i" 
                      class="w-5 h-5 text-amber-400 fill-amber-400 drop-shadow-sm" 
                    />
                    <Star 
                      v-for="(_, i) in renderStars(5 - review.rating)" 
                      :key="'empty-' + i" 
                      class="w-5 h-5 text-gray-200" 
                    />
                    <span class="ml-2 text-sm font-semibold text-amber-500">{{ review.rating }}.0</span>
                  </div>
                  <div v-else class="flex items-center gap-1">
                    <button 
                      v-for="star in 5" 
                      :key="star" 
                      type="button" 
                      @click="formData.rating = star"
                      class="transition-transform hover:scale-110"
                    >
                      <Star 
                        class="w-6 h-6" 
                        :class="star <= formData.rating ? 'text-amber-400 fill-amber-400' : 'text-gray-200'" 
                      />
                    </button>
                  </div>
                </td>
                <td class="py-4 px-5">
                  <div v-if="editingId !== review.id" class="relative">
                    <Quote class="w-4 h-4 text-indigo-300 mb-1" />
                    <p class="text-gray-700 line-clamp-2 text-sm leading-relaxed">{{ review.content || '暂无评价内容' }}</p>
                  </div>
                  <Input 
                    v-else 
                    v-model="formData.content" 
                    class="h-20 w-full resize-none" 
                    placeholder="请输入评价内容"
                  />
                </td>
                <td class="py-4 px-5">
                  <div class="flex items-center gap-2 text-gray-500">
                    <div class="w-8 h-8 rounded-lg bg-gray-100 flex items-center justify-center">
                      <Calendar class="w-4 h-4 text-gray-400" />
                    </div>
                    <span class="text-sm font-medium">{{ formatDate(review.created_at) }}</span>
                  </div>
                </td>
                <td class="py-4 px-5">
                  <div v-if="editingId !== review.id" class="flex items-center justify-center gap-2">
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      @click="startEdit(review)"
                      class="hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
                    >
                      <Edit class="w-4 h-4 mr-1" />
                      编辑
                    </Button>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      @click="handleDelete(review.id)" 
                      class="hover:bg-red-50 hover:text-red-600 transition-colors"
                    >
                      <Trash2 class="w-4 h-4 mr-1" />
                      删除
                    </Button>
                  </div>
                  <div v-else class="flex items-center justify-center gap-2">
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      @click="saveEdit"
                      class="bg-emerald-50 text-emerald-600 hover:bg-emerald-100 transition-colors"
                    >
                      保存
                    </Button>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      @click="cancelEdit"
                      class="text-gray-500 hover:bg-gray-100 transition-colors"
                    >
                      取消
                    </Button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="filteredReviews.length === 0" class="py-16 text-center">
          <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-gray-100 flex items-center justify-center">
            <MessageSquare class="w-10 h-10 text-gray-300" />
          </div>
          <p class="text-gray-500">暂无评价数据</p>
        </div>

        <!-- Pagination -->
        <div class="flex items-center justify-between px-6 py-4 border-t border-gray-100 bg-gray-50/50 flex-shrink-0">
          <div class="flex items-center gap-2 text-sm text-gray-500">
            <span class="font-medium">每页 {{ pagination.pageSize }} 条</span>
            <span class="text-gray-300">|</span>
            <span>共 {{ filteredReviews.length }} 条记录</span>
          </div>
          <div class="flex items-center gap-2">
            <Button variant="outline" size="sm" class="hover:bg-white">上一页</Button>
            <Button variant="outline" size="sm" class="min-w-10 bg-white">1</Button>
            <Button variant="outline" size="sm" class="hover:bg-white">下一页</Button>
          </div>
        </div>
      </Card>
    </div>

    <Drawer 
      :open="drawerOpen" 
      :title="drawerMode === 'add' ? '新增用户评价' : '编辑用户评价'" 
      position="right"
      width="480px"
      @close="closeDrawer"
    >
      <div class="p-6 space-y-6">
        <div v-if="drawerError" class="p-3 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-sm text-red-600">{{ drawerError }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            用户名
            <span class="text-red-500 ml-1">*</span>
          </label>
          <Input 
            v-model="drawerFormData.name"
            placeholder="请输入用户名" 
            class="h-11"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            头像颜色
          </label>
          <div class="grid grid-cols-3 gap-2">
            <button
              v-for="color in avatarColors"
              :key="color.value"
              type="button"
              @click="drawerFormData.avatar_color = color.value"
              :class="[
                'h-10 rounded-lg flex items-center justify-center text-xs font-medium transition-all',
                drawerFormData.avatar_color === color.value 
                  ? `${color.bg} text-white ring-2 ring-offset-2 ${color.ring}`
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
            >
              {{ color.label }}
            </button>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            评分
            <span class="text-red-500 ml-1">*</span>
          </label>
          <div class="flex items-center gap-2">
            <button 
              v-for="star in 5" 
              :key="star" 
              type="button"
              @click="drawerFormData.rating = star"
              class="transition-transform hover:scale-110"
            >
              <Star 
                class="w-8 h-8" 
                :class="star <= drawerFormData.rating ? 'text-amber-400 fill-amber-400' : 'text-gray-200'" 
              />
            </button>
            <span class="ml-4 text-lg font-semibold text-amber-500">{{ drawerFormData.rating }}.0</span>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            评价内容
            <span class="text-red-500 ml-1">*</span>
          </label>
          <Input 
            v-model="drawerFormData.content"
            type="textarea"
            placeholder="请输入评价内容"
            class="min-h-32"
          />
        </div>

        <div class="pt-4 flex gap-3">
          <Button 
            variant="outline" 
            @click="closeDrawer" 
            class="flex-1 h-11"
          >
            取消
          </Button>
          <Button 
            @click="handleSubmitDrawer" 
            class="flex-1 h-11 bg-gradient-to-r from-indigo-500 to-violet-600 hover:from-indigo-600 hover:to-violet-700"
          >
            {{ drawerMode === 'add' ? '创建评价' : '保存修改' }}
          </Button>
        </div>
      </div>
    </Drawer>
  </div>
</template>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}

tbody tr {
  transition: all 0.2s ease;
}

tbody tr:hover {
  transform: translateX(4px);
}

tbody tr:hover .avatar-bounce {
  animation: bounce 0.5s ease;
}

@keyframes bounce {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}
</style>
