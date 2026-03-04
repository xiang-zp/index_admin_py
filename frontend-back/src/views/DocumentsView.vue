<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Textarea from '@/components/ui/Textarea.vue'
import Drawer from '@/components/ui/Drawer.vue'
import { documentsApi, type CategoryFull, type CategoryCreateRequest, type CategoryUpdateRequest } from '@/services/documents'
import type { Document, Category } from '@/services/documents'
import { toast } from '@/lib/toast'
import {
  Plus,
  Edit,
  Trash2,
  Search,
  RefreshCw,
  FileText,
  BookOpen,
  Calendar,
  Tag,
  Eye,
  EyeOff,
  Tags,
  Clock
} from 'lucide-vue-next'

const categories = ref<Category[]>([])
const documentCategories = ref<CategoryFull[]>([])
const documents = ref<Document[]>([])
const editingId = ref<string | null>(null)
const loading = ref(false)
const drawerOpen = ref(false)
const drawerMode = ref<'add' | 'edit'>('add')

const categoryDialogOpen = ref(false)
const categoryDialogMode = ref<'add' | 'edit'>('add')
const editingCategoryId = ref<number | null>(null)

const columnWidths = ref({
  id: 112,
  category: 100,
  title: 150,
  description: 200,
  row: 100,
  status: 100,
  url: 180,
  updated_at: 144,
  action: 144
})

const resizing = ref<string | null>(null)
const startX = ref(0)
const startWidth = ref(0)

const startResize = (e: MouseEvent, column: string) => {
  e.preventDefault()
  resizing.value = column
  startX.value = e.clientX
  startWidth.value = columnWidths.value[column as keyof typeof columnWidths.value]
  document.addEventListener('mousemove', handleResize)
  document.addEventListener('mouseup', stopResize)
}

const handleResize = (e: MouseEvent) => {
  if (!resizing.value) return
  const diff = e.clientX - startX.value
  const newWidth = Math.max(80, startWidth.value + diff)
  columnWidths.value[resizing.value as keyof typeof columnWidths.value] = newWidth
}

const stopResize = () => {
  resizing.value = null
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
}

const categoryFormData = ref<CategoryCreateRequest>({
  name: '',
  color: '#3b82f6'
})

const searchForm = ref({
  category: '',
  title: ''
})

const formData = ref({
  category: '',
  title: '',
  description: '',
  color: '#3b82f6',
  url: '',
  row: 'row1',
  is_visible: true
})

const colorOptions = [
  { value: '#3b82f6', label: '蓝色', class: 'bg-blue-500' },
  { value: '#10b981', label: '绿色', class: 'bg-green-500' },
  { value: '#f59e0b', label: '橙色', class: 'bg-amber-500' },
  { value: '#ef4444', label: '红色', class: 'bg-red-500' },
  { value: '#8b5cf6', label: '紫色', class: 'bg-violet-500' },
  { value: '#ec4899', label: '粉色', class: 'bg-pink-500' }
]

const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0
})

const filteredDocuments = computed(() => {
  const categoryFilter = searchForm.value.category
  const titleKeyword = searchForm.value.title.toLowerCase().trim()
  
  return documents.value.filter(doc => {
    const matchCategory = !categoryFilter || doc.category === categoryFilter
    const matchTitle = !titleKeyword || doc.title.toLowerCase().includes(titleKeyword)
    return matchCategory && matchTitle
  })
})

const resetForm = () => {
  formData.value = { 
    category: categories.value[0]?.name || '', 
    title: '', 
    description: '', 
    color: '#3b82f6',
    url: '',
    row: 'row1',
    is_visible: true 
  }
}

const loadData = async () => {
  loading.value = true
  try {
    const [docsResponse, fullCatsResponse] = await Promise.all([
      documentsApi.getList({
        category: searchForm.value.category || undefined,
        page: pagination.value.current,
        page_size: pagination.value.pageSize
      }),
      documentsApi.getCategoriesFull()
    ])

    if (docsResponse.code === 200 || docsResponse.code === 0) {
      documents.value = docsResponse.data.list
      pagination.value.total = docsResponse.data.total
    }
    
    if (fullCatsResponse.code === 200 || fullCatsResponse.code === 0) {
      documentCategories.value = fullCatsResponse.data
      categories.value = fullCatsResponse.data.map((cat: any) => ({ id: cat.id, name: cat.name }))
    }
  } catch (error) {
    console.error('Failed to load data:', error)
    toast.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const openCategoryDialog = (mode: 'add' | 'edit', category?: CategoryFull) => {
  categoryDialogMode.value = mode
  if (mode === 'edit' && category) {
    editingCategoryId.value = category.id
    categoryFormData.value = {
      name: category.name,
      color: category.color
    }
  } else {
    editingCategoryId.value = null
    categoryFormData.value = {
      name: '',
      color: '#3b82f6'
    }
  }
  categoryDialogOpen.value = true
}

const closeCategoryDialog = () => {
  categoryDialogOpen.value = false
  editingCategoryId.value = null
  categoryFormData.value = {
    name: '',
    color: '#3b82f6'
  }
}

const saveCategory = async () => {
  if (!categoryFormData.value.name) {
    toast.error('请输入标签名称')
    return
  }

  try {
    const res = await documentsApi.createCategory({
      name: categoryFormData.value.name,
      color: '#3b82f6'
    })
    if (res.code === 200 || res.code === 0) {
      toast.success('创建成功')
      categoryFormData.value.name = ''
      loadData()
    } else {
      toast.error(res.message || '创建失败')
    }
  } catch (error) {
    console.error('Failed to save category:', error)
    toast.error('保存失败')
  }
}

const deleteCategory = async (id: number) => {
  if (!confirm('确定要删除这个分类标签吗？')) return

  try {
    const res = await documentsApi.deleteCategory(id)
    if (res.code === 200 || res.code === 0) {
      toast.success('删除成功')
      loadData()
    } else {
      toast.error(res.message || '删除失败')
    }
  } catch (error) {
    console.error('Failed to delete category:', error)
    toast.error('删除失败')
  }
}

const handleSearch = () => {
  pagination.value.current = 1
  loadData()
}

const handleReset = () => {
  searchForm.value = { category: '', title: '' }
  handleSearch()
}

const handleAdd = () => {
  drawerMode.value = 'add'
  editingId.value = null
  resetForm()
  drawerOpen.value = true
}

const startEdit = (doc: Document) => {
  drawerMode.value = 'edit'
  editingId.value = doc.id
  formData.value = {
    category: doc.category,
    title: doc.title,
    description: doc.description,
    color: doc.color,
    url: doc.url || '',
    row: doc.row || 'row1',
    is_visible: doc.is_visible
  }
  drawerOpen.value = true
}

const handleSave = async () => {
  if (!formData.value.category || !formData.value.title) {
    toast.error('请填写分类和标题')
    return
  }

  try {
    if (drawerMode.value === 'add') {
      const res = await documentsApi.create({
        category: formData.value.category,
        title: formData.value.title,
        description: formData.value.description,
        color: formData.value.color,
        url: formData.value.url,
        row: formData.value.row,
        is_visible: formData.value.is_visible
      })

      if (res.code === 200 || res.code === 0) {
        toast.success('创建成功')
        drawerOpen.value = false
        resetForm()
        loadData()
      } else {
        toast.error(res.message || '创建失败')
      }
    } else {
      if (!editingId.value) return

      const res = await documentsApi.update({
        id: editingId.value,
        category: formData.value.category,
        title: formData.value.title,
        description: formData.value.description,
        color: formData.value.color,
        url: formData.value.url,
        row: formData.value.row,
        is_visible: formData.value.is_visible
      })

      if (res.code === 200 || res.code === 0) {
        toast.success('更新成功')
        drawerOpen.value = false
        editingId.value = null
        resetForm()
        loadData()
      } else {
        toast.error(res.message || '更新失败')
      }
    }
  } catch (error) {
    console.error('Failed to save document:', error)
    toast.error('保存失败')
  }
}

const closeDrawer = () => {
  drawerOpen.value = false
  editingId.value = null
  resetForm()
}

const handleDelete = async (id: string) => {
  if (!confirm('确定要删除这个文档吗？')) return

  try {
    const res = await documentsApi.delete(id)
    if (res.code === 200 || res.code === 0) {
      toast.success('删除成功')
      
      const totalAfterDelete = pagination.value.total - 1
      const maxPage = Math.ceil(totalAfterDelete / pagination.value.pageSize)
      if (pagination.value.current > maxPage && maxPage > 0) {
        pagination.value.current = maxPage
      }
      
      loadData()
    } else {
      toast.error(res.message || '删除失败')
    }
  } catch (error) {
    console.error('Failed to delete document:', error)
    toast.error('删除失败')
  }
}

const toggleVisibility = async (doc: Document) => {
  try {
    const newStatus = !doc.is_visible
    const res = await documentsApi.toggleVisible(doc.id, newStatus)
    
    if (res.code === 200 || res.code === 0) {
      doc.is_visible = newStatus
      toast.success(newStatus ? '已显示' : '已隐藏')
    } else {
      toast.error(res.message || '操作失败')
    }
  } catch (error) {
    console.error('Failed to toggle visibility:', error)
    toast.error('操作失败')
  }
}

const getVisibilityIcon = (visible: boolean) => {
  return visible ? Eye : EyeOff
}

const getVisibilityText = (visible: boolean) => {
  return visible ? '展示' : '隐藏'
}

const getVisibilityClass = (visible: boolean) => {
  return visible ? 'text-amber-600 bg-amber-50' : 'text-gray-400 bg-gray-50'
}

const getColorClass = (color: string) => {
  return colorOptions.find(c => c.value === color)?.class || 'bg-blue-500'
}

const formatDateTime = (date: string) => {
  if (!date) return '-'
  const d = new Date(date)
  return d.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="h-screen overflow-hidden bg-gradient-to-br from-stone-50 via-slate-50 to-stone-100">
    <div class="max-w-7xl mx-auto px-8 py-6 h-full flex flex-col">
      <div class="mb-6 flex-shrink-0">
        <div class="flex items-center gap-4 mb-2">
          <div class="p-3 bg-gradient-to-br from-amber-500 to-orange-600 rounded-2xl shadow-lg shadow-amber-200">
            <BookOpen class="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-900 via-gray-700 to-gray-600 bg-clip-text text-transparent">
              文档资料管理
            </h1>
            <p class="text-gray-500 mt-1 font-medium">管理前台显示的文档资料</p>
          </div>
        </div>
      </div>

      <div class="grid gap-4 mb-4 flex-shrink-0">
        <Card class="border-0 shadow-xl shadow-gray-200/50 bg-white/80 backdrop-blur-sm">
          <CardContent class="py-4 px-5">
            <div class="flex flex-wrap gap-4 items-center">
              <div class="flex gap-4 flex-1 min-w-[400px]">
                <div class="flex-1 min-w-[160px]">
                  <label class="block text-xs font-medium text-gray-500 mb-1.5">按分类筛选</label>
                  <div class="relative">
                    <Tag class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <select 
                      v-model="searchForm.category"
                      class="w-full pl-10 h-10 bg-gray-50/50 border-gray-200 focus:bg-white transition-all duration-300 rounded-lg appearance-none cursor-pointer"
                    >
                      <option value="">全部分类</option>
                      <option v-for="cat in categories" :key="cat.id" :value="cat.name">{{ cat.name }}</option>
                    </select>
                  </div>
                </div>
                <div class="flex-1 min-w-[200px]">
                  <label class="block text-xs font-medium text-gray-500 mb-1.5">按标题搜索</label>
                  <div class="relative">
                    <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <Input 
                      v-model="searchForm.title"
                      placeholder="输入文档标题" 
                      class="pl-10 h-10 bg-gray-50/50 border-gray-200 focus:bg-white transition-all duration-300"
                    />
                  </div>
                </div>
              </div>
              <div class="flex gap-3 items-end">
                <Button variant="outline" @click="handleReset" class="h-10 px-4 hover:bg-gray-50">
                  <RefreshCw class="w-4 h-4 mr-2" />
                  重置
                </Button>
                <Button @click="handleSearch" class="h-10 px-4 bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 shadow-lg shadow-amber-200">
                  <Search class="w-4 h-4 mr-2" />
                  搜索
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        <div class="flex justify-end gap-3">
          <Button 
            @click="openCategoryDialog('add')" 
            variant="outline"
            class="h-10 px-5 hover:bg-violet-50 hover:border-violet-300 hover:text-violet-600"
            title="可新增、编辑、删除标签"
          >
            <Tags class="w-4 h-4 mr-2" />
            分类标签管理
          </Button>
          <Button @click="handleAdd" class="h-10 px-5 bg-gradient-to-r from-indigo-500 to-violet-600 hover:from-indigo-600 hover:to-violet-700 shadow-lg shadow-indigo-200">
            <Plus class="w-4 h-4 mr-2" />
            新增文档
          </Button>
        </div>
      </div>

      <Card class="border-0 shadow-xl shadow-gray-200/50 bg-white/90 backdrop-blur-sm overflow-hidden rounded-2xl flex-1 flex flex-col min-h-0">
        <div class="overflow-auto flex-1">
          <table class="w-full" style="table-layout: fixed;">
            <thead class="sticky top-0 z-10">
              <tr class="bg-gradient-to-r from-slate-100 via-gray-100 to-slate-100 border-b-2 border-gray-200">
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide relative select-none group" :style="{ width: columnWidths.id + 'px', minWidth: columnWidths.id + 'px' }">
                  编号
                  <div 
                    class="absolute right-0 top-0 bottom-0 w-1.5 cursor-col-resize group-hover:w-2 transition-all duration-150 z-20 flex items-center justify-center"
                    @mousedown="(e: MouseEvent) => startResize(e, 'id')"
                  >
                    <div class="w-1 h-8 rounded-full bg-gray-300 group-hover:bg-gradient-to-b group-hover:from-blue-400 group-hover:to-indigo-500 group-hover:shadow-lg group-hover:shadow-blue-400/30 transition-all duration-150"></div>
                  </div>
                </th>
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide relative select-none group" :style="{ width: columnWidths.category + 'px', minWidth: columnWidths.category + 'px' }">
                  分类
                  <div 
                    class="absolute right-0 top-0 bottom-0 w-1.5 cursor-col-resize group-hover:w-2 transition-all duration-150 z-20 flex items-center justify-center"
                    @mousedown="(e: MouseEvent) => startResize(e, 'category')"
                  >
                    <div class="w-1 h-8 rounded-full bg-gray-300 group-hover:bg-gradient-to-b group-hover:from-blue-400 group-hover:to-indigo-500 group-hover:shadow-lg group-hover:shadow-blue-400/30 transition-all duration-150"></div>
                  </div>
                </th>
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide relative select-none group" :style="{ width: columnWidths.title + 'px', minWidth: columnWidths.title + 'px' }">
                  标题
                  <div 
                    class="absolute right-0 top-0 bottom-0 w-1.5 cursor-col-resize group-hover:w-2 transition-all duration-150 z-20 flex items-center justify-center"
                    @mousedown="(e: MouseEvent) => startResize(e, 'title')"
                  >
                    <div class="w-1 h-8 rounded-full bg-gray-300 group-hover:bg-gradient-to-b group-hover:from-blue-400 group-hover:to-indigo-500 group-hover:shadow-lg group-hover:shadow-blue-400/30 transition-all duration-150"></div>
                  </div>
                </th>
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide relative select-none group" :style="{ width: columnWidths.description + 'px', minWidth: columnWidths.description + 'px' }">
                  描述
                  <div 
                    class="absolute right-0 top-0 bottom-0 w-1.5 cursor-col-resize group-hover:w-2 transition-all duration-150 z-20 flex items-center justify-center"
                    @mousedown="(e: MouseEvent) => startResize(e, 'description')"
                  >
                    <div class="w-1 h-8 rounded-full bg-gray-300 group-hover:bg-gradient-to-b group-hover:from-blue-400 group-hover:to-indigo-500 group-hover:shadow-lg group-hover:shadow-blue-400/30 transition-all duration-150"></div>
                  </div>
                </th>
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide relative select-none group" :style="{ width: columnWidths.row + 'px', minWidth: columnWidths.row + 'px' }">
                  展示位
                  <div 
                    class="absolute right-0 top-0 bottom-0 w-1.5 cursor-col-resize group-hover:w-2 transition-all duration-150 z-20 flex items-center justify-center"
                    @mousedown="(e: MouseEvent) => startResize(e, 'row')"
                  >
                    <div class="w-1 h-8 rounded-full bg-gray-300 group-hover:bg-gradient-to-b group-hover:from-blue-400 group-hover:to-indigo-500 group-hover:shadow-lg group-hover:shadow-blue-400/30 transition-all duration-150"></div>
                  </div>
                </th>
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide relative select-none group" :style="{ width: columnWidths.status + 'px', minWidth: columnWidths.status + 'px' }">
                  状态
                  <div 
                    class="absolute right-0 top-0 bottom-0 w-1.5 cursor-col-resize group-hover:w-2 transition-all duration-150 z-20 flex items-center justify-center"
                    @mousedown="(e: MouseEvent) => startResize(e, 'status')"
                  >
                    <div class="w-1 h-8 rounded-full bg-gray-300 group-hover:bg-gradient-to-b group-hover:from-blue-400 group-hover:to-indigo-500 group-hover:shadow-lg group-hover:shadow-blue-400/30 transition-all duration-150"></div>
                  </div>
                </th>
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide relative select-none group" :style="{ width: columnWidths.url + 'px', minWidth: columnWidths.url + 'px' }">
                  跳转地址
                  <div 
                    class="absolute right-0 top-0 bottom-0 w-1.5 cursor-col-resize group-hover:w-2 transition-all duration-150 z-20 flex items-center justify-center"
                    @mousedown="(e: MouseEvent) => startResize(e, 'url')"
                  >
                    <div class="w-1 h-8 rounded-full bg-gray-300 group-hover:bg-gradient-to-b group-hover:from-blue-400 group-hover:to-indigo-500 group-hover:shadow-lg group-hover:shadow-blue-400/30 transition-all duration-150"></div>
                  </div>
                </th>
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide relative select-none group" :style="{ width: columnWidths.updated_at + 'px', minWidth: columnWidths.updated_at + 'px' }">
                  <div class="flex items-center gap-2">
                    <Clock class="w-4 h-4" />
                    更新时间
                  </div>
                  <div 
                    class="absolute right-0 top-0 bottom-0 w-1.5 cursor-col-resize group-hover:w-2 transition-all duration-150 z-20 flex items-center justify-center"
                    @mousedown="(e: MouseEvent) => startResize(e, 'updated_at')"
                  >
                    <div class="w-1 h-8 rounded-full bg-gray-300 group-hover:bg-gradient-to-b group-hover:from-blue-400 group-hover:to-indigo-500 group-hover:shadow-lg group-hover:shadow-blue-400/30 transition-all duration-150"></div>
                  </div>
                </th>
                <th class="text-center py-5 px-6 font-bold text-gray-700 text-sm tracking-wide select-none" :style="{ width: columnWidths.action + 'px', minWidth: columnWidths.action + 'px' }">
                  操作
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr 
                v-for="doc in filteredDocuments" 
                :key="doc.id"
                class="hover:bg-gradient-to-r hover:from-amber-50/30 hover:to-transparent transition-all duration-300 group"
              >
                <td class="py-4 px-5" :style="{ width: columnWidths.id + 'px' }">
                  <span class="font-mono text-sm text-gray-500 group-hover:text-amber-600 transition-colors">{{ doc.id }}</span>
                </td>
                <td class="py-4 px-5" :style="{ width: columnWidths.category + 'px' }">
                  <span class="text-gray-800 font-medium">{{ doc.category }}</span>
                </td>
                <td class="py-4 px-5" :style="{ width: columnWidths.title + 'px' }">
                  <span class="text-gray-800 font-medium block w-[10ch] break-all">{{ doc.title || '未命名文档' }}</span>
                </td>
                <td class="py-4 px-5" :style="{ width: columnWidths.description + 'px' }">
                  <div class="relative group/desc">
                    <BookOpen class="w-4 h-4 text-amber-400 mb-1" />
                    <p class="text-gray-600 line-clamp-2 text-sm leading-relaxed">{{ doc.description || '暂无描述' }}</p>
                    <div v-if="doc.description && doc.description.length > 50" class="absolute left-0 top-full mt-2 z-[100] invisible group-hover/desc:visible opacity-0 group-hover/desc:opacity-100 transition-all duration-200">
                      <div class="relative">
                        <div class="bg-gray-900 text-white text-sm px-4 py-3 rounded-lg shadow-xl w-[20em] break-all leading-relaxed">
                          {{ doc.description }}
                        </div>
                        <div class="absolute left-4 bottom-full -mb-1 w-0 h-0 border-l-[8px] border-l-transparent border-r-[8px] border-r-transparent border-b-[8px] border-b-gray-900"></div>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="py-4 px-5" :style="{ width: columnWidths.row + 'px' }">
                  <span :class="[
                    'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border',
                    doc.row === 'row2' ? 'bg-violet-100 text-violet-700 border-violet-200' : 'bg-blue-100 text-blue-700 border-blue-200'
                  ]">
                    {{ doc.row === 'row2' ? '第二行' : '第一行' }}
                  </span>
                </td>
                <td class="py-4 px-5" :style="{ width: columnWidths.status + 'px' }">
                  <button 
                    @click="toggleVisibility(doc)"
                    class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200 hover:scale-105"
                    :class="getVisibilityClass(doc.is_visible)"
                  >
                    <component :is="getVisibilityIcon(doc.is_visible)" class="w-3.5 h-3.5" />
                    {{ getVisibilityText(doc.is_visible) }}
                  </button>
                </td>
                <td class="py-4 px-5" :style="{ width: columnWidths.url + 'px' }">
                  <span v-if="doc.url" class="text-blue-600 hover:underline truncate block" :title="doc.url">
                    {{ doc.url }}
                  </span>
                  <span v-else class="text-gray-400 text-sm">-</span>
                </td>
                <td class="py-4 px-5" :style="{ width: columnWidths.updated_at + 'px' }">
                  <div class="flex items-center gap-2 text-gray-500">
                    <div class="w-8 h-8 rounded-lg bg-gray-100 flex items-center justify-center">
                      <Clock class="w-4 h-4 text-gray-400" />
                    </div>
                    <span class="text-sm font-medium">{{ formatDateTime(doc.updated_at) }}</span>
                  </div>
                </td>
                <td class="py-4 px-5" :style="{ width: columnWidths.action + 'px' }">
                  <div class="flex items-center justify-center gap-2">
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      @click="startEdit(doc)"
                      class="hover:bg-amber-50 hover:text-amber-600 transition-colors"
                    >
                      <Edit class="w-4 h-4 mr-1" />
                      编辑
                    </Button>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      @click="handleDelete(doc.id)" 
                      class="hover:bg-red-50 hover:text-red-600 transition-colors"
                    >
                      <Trash2 class="w-4 h-4 mr-1" />
                      删除
                    </Button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <div v-if="!loading && filteredDocuments.length === 0" class="py-16 text-center">
            <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-gray-100 flex items-center justify-center">
              <FileText class="w-10 h-10 text-gray-300" />
            </div>
            <p class="text-gray-500">暂无文档数据</p>
          </div>
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
            <Button variant="outline" size="sm" class="min-w-10 bg-white">{{ pagination.current }}</Button>
            <Button variant="outline" size="sm" class="hover:bg-white">下一页</Button>
          </div>
        </div>
      </Card>
    </div>
    <Drawer 
      :open="drawerOpen" 
      :title="drawerMode === 'add' ? '新增文档' : '编辑文档'"
      @close="closeDrawer"
    >
      <div class="p-6 space-y-6">
        <div class="space-y-2">
          <label class="text-sm font-medium text-gray-700">文档分类 <span class="text-red-500">*</span></label>
          <div class="relative">
            <Tag class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <select 
              v-model="formData.category"
              class="w-full pl-10 h-10 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-200 focus:border-amber-300 transition-all appearance-none cursor-pointer"
            >
              <option value="" disabled>请选择分类</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.name">{{ cat.name }}</option>
            </select>
          </div>
        </div>

        <div class="space-y-2">
          <label class="text-sm font-medium text-gray-700">文档标题 <span class="text-red-500">*</span></label>
          <Input 
            v-model="formData.title"
            placeholder="请输入文档标题" 
          />
        </div>

        <div class="space-y-2">
          <label class="text-sm font-medium text-gray-700">标识颜色</label>
          <div class="flex flex-wrap gap-3">
            <button
              v-for="option in colorOptions"
              :key="option.value"
              type="button"
              @click="formData.color = option.value"
              class="w-8 h-8 rounded-full transition-transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400"
              :class="[
                option.class,
                formData.color === option.value ? 'ring-2 ring-offset-2 ring-gray-400 scale-110' : ''
              ]"
              :title="option.label"
            />
          </div>
        </div>

        <div class="space-y-2">
          <label class="text-sm font-medium text-gray-700">文档描述</label>
          <Textarea 
            v-model="formData.description"
            placeholder="请输入文档内容的简要描述..." 
            class="h-32 resize-none"
          />
        </div>

        <div class="space-y-2">
          <label class="text-sm font-medium text-gray-700">跳转地址</label>
          <Input 
            v-model="formData.url"
            placeholder="请输入文档跳转地址，如：https://www.baidu.com/" 
          />
        </div>

        <div class="space-y-2">
          <label class="text-sm font-medium text-gray-700">展示位置</label>
          <div class="flex gap-3">
            <button
              type="button"
              @click="formData.row = 'row1'"
              :class="[
                'flex-1 py-3 px-4 rounded-lg border-2 transition-all duration-200 flex items-center justify-center gap-2',
                formData.row === 'row1' 
                  ? 'border-blue-500 bg-blue-50 text-blue-700' 
                  : 'border-gray-200 bg-white text-gray-500 hover:border-gray-300'
              ]"
            >
              第一行
            </button>
            <button
              type="button"
              @click="formData.row = 'row2'"
              :class="[
                'flex-1 py-3 px-4 rounded-lg border-2 transition-all duration-200 flex items-center justify-center gap-2',
                formData.row === 'row2' 
                  ? 'border-violet-500 bg-violet-50 text-violet-700' 
                  : 'border-gray-200 bg-white text-gray-500 hover:border-gray-300'
              ]"
            >
              第二行
            </button>
          </div>
        </div>

        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div class="flex items-center gap-3">
            <div :class="[
              'w-10 h-10 rounded-lg flex items-center justify-center transition-colors',
              formData.is_visible ? 'bg-amber-100' : 'bg-gray-200'
            ]">
              <component :is="formData.is_visible ? Eye : EyeOff" :class="[
                'w-5 h-5',
                formData.is_visible ? 'text-amber-600' : 'text-gray-500'
              ]" />
            </div>
            <div>
              <p class="text-sm font-medium text-gray-900">前台展示</p>
              <p class="text-xs text-gray-500">{{ formData.is_visible ? '当前文档对用户可见' : '当前文档已隐藏' }}</p>
            </div>
          </div>
          <button 
            type="button"
            @click="formData.is_visible = !formData.is_visible"
            :class="[
              'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-amber-500 focus:ring-offset-2',
              formData.is_visible ? 'bg-amber-500' : 'bg-gray-200'
            ]"
          >
            <span 
              :class="[
                'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                formData.is_visible ? 'translate-x-5' : 'translate-x-0'
              ]" 
            />
          </button>
        </div>
      </div>

      <div class="p-6 border-t bg-gray-50">
        <div class="flex gap-3">
          <Button variant="outline" class="flex-1" @click="closeDrawer">取消</Button>
          <Button class="flex-1 bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white shadow-lg shadow-amber-200" @click="handleSave">
            {{ drawerMode === 'add' ? '确认创建' : '保存修改' }}
          </Button>
        </div>
      </div>
    </Drawer>

    <Drawer :open="categoryDialogOpen" position="right" width="420px" title="标签管理" @close="closeCategoryDialog">
      <div class="flex flex-col h-full">
        <div class="flex-1 overflow-y-auto p-5 space-y-5">
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">新增标签 <span class="text-red-500">*</span></label>
            <div class="flex gap-2">
              <Input 
                v-model="categoryFormData.name"
                placeholder="请输入标签名称"
                class="flex-1"
              />
              <Button 
                class="bg-gradient-to-r from-violet-500 to-purple-600 hover:from-violet-600 hover:to-purple-700 text-white"
                @click="saveCategory"
              >
                新增
              </Button>
            </div>
          </div>

          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">已有标签列表</label>
            <div class="border border-gray-200 rounded-lg overflow-hidden">
              <table class="w-full">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="text-left py-2 px-3 text-xs font-medium text-gray-500">标签名称</th>
                    <th class="text-right py-2 px-3 text-xs font-medium text-gray-500">操作</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr v-for="cat in documentCategories" :key="cat.id" class="hover:bg-gray-50">
                    <td class="py-2 px-3 text-sm font-medium text-gray-700">{{ cat.name }}</td>
                    <td class="py-2 px-3 text-right">
                      <div class="flex items-center justify-end gap-1">
                        <button 
                          @click="deleteCategory(cat.id)"
                          class="p-1 hover:bg-red-50 rounded text-red-500"
                          title="删除"
                        >
                          <Trash2 class="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div v-if="documentCategories.length === 0" class="py-8 text-center text-gray-400 text-sm">
                暂无标签，请新增
              </div>
            </div>
          </div>
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

select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 0.75rem;
  padding-right: 2.5rem;
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
</style>
