<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Card from '@/components/ui/Card.vue'
import Drawer from '@/components/ui/Drawer.vue'
import { carouselApi, type CarouselItem, type CarouselCreateRequest, type CarouselUpdateRequest } from '@/services/carousel'
import { toast } from '@/lib/toast'
import {
  Plus,
  Edit,
  Trash2,
  Save,
  Eye,
  EyeOff,
  GripVertical,
  Layers
} from 'lucide-vue-next'

const carouselItems = ref<CarouselItem[]>([])
const drawerOpen = ref(false)
const drawerMode = ref<'add' | 'edit'>('add')
const draggedIndex = ref<number | null>(null)

const formData = ref({
  id: '',
  title: '',
  description: '',
  is_visible: true,
  sort_order: 0
})

const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0
})

const resetForm = () => {
  formData.value = { id: '', title: '', description: '', is_visible: true, sort_order: 0 }
}

const openAddDrawer = () => {
  resetForm()
  formData.value.sort_order = carouselItems.value.length + 1
  drawerMode.value = 'add'
  drawerOpen.value = true
}

const openEditDrawer = (item: CarouselItem) => {
  formData.value = {
    id: item.id,
    title: item.title, // 保留但不使用
    description: item.description,
    is_visible: item.is_visible,
    sort_order: item.sort_order
  }
  drawerMode.value = 'edit'
  drawerOpen.value = true
}

const closeDrawer = () => {
  drawerOpen.value = false
  resetForm()
}

const handleSave = async () => {
  if (!formData.value.description) {
    toast.error('请填写文案内容')
    return
  }

  if (formData.value.description.length > 35) {
    toast.error('字数输入超限，最多可输入35个字符')
    return
  }

  loading.value = true

  try {
    if (drawerMode.value === 'add') {
      const response = await carouselApi.create({
        title: '轮播文案',
        description: formData.value.description,
        is_visible: formData.value.is_visible !== undefined ? formData.value.is_visible : true
      })
      if (response.code === 200 || response.code === 0) {
        await fetchCarousels() // 刷新列表
        toast.success('创建成功')
      } else {
        toast.error(`创建失败: ${response.message}`)
        return
      }
    } else {
      const response = await carouselApi.update({
        id: formData.value.id,
        title: '轮播文案',
        description: formData.value.description,
        is_visible: formData.value.is_visible
      })
      if (response.code === 200 || response.code === 0) {
        await fetchCarousels() // 刷新列表
        toast.success('更新成功')
      } else {
        toast.error(`更新失败: ${response.message}`)
        return
      }
    }
    closeDrawer()
  } catch (error) {
    console.error('保存失败:', error)
    toast.error('保存失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const handleDelete = async (id: string) => {
  if (!confirm('确定要删除这个轮播项吗？')) {
    return
  }

  try {
    const response = await carouselApi.delete(id)
    if (response.code === 200 || response.code === 0) {
      await fetchCarousels() // 刷新列表
      toast.success('删除成功')
    } else {
      toast.error(`删除失败: ${response.message}`)
    }
  } catch (error) {
    console.error('删除失败:', error)
    toast.error('删除失败，请稍后重试')
  }
}

const toggleVisibility = async (item: CarouselItem) => {
  try {
    const newVisibleState = !item.is_visible
    const response = await carouselApi.toggleVisible(item.id, newVisibleState)
    if (response.code === 200 || response.code === 0) {
      // 更新本地状态
      item.is_visible = newVisibleState
    } else {
      toast.error(`切换状态失败: ${response.message}`)
    }
  } catch (error) {
    console.error('切换状态失败:', error)
    toast.error('切换状态失败，请稍后重试')
  }
}

const onDragStart = (index: number) => {
  draggedIndex.value = index
}

const onDragOver = (event: DragEvent, index: number) => {
  event.preventDefault()
  if (draggedIndex.value === null || draggedIndex.value === index) return
  
  const draggedItem = carouselItems.value[draggedIndex.value]
  carouselItems.value.splice(draggedIndex.value, 1)
  carouselItems.value.splice(index, 0, draggedItem)
  draggedIndex.value = index
  
  // 更新所有项目的排序值以反映新顺序
  carouselItems.value.forEach((item, idx) => {
    item.sort_order = idx
  })
}

const saveOrder = async () => {
  try {
    const ids = carouselItems.value.map(item => item.id)
    console.log('保存排序，ID列表:', ids, '当前轮播项:', carouselItems.value)
    const response = await carouselApi.reorder({ ids })
    console.log('排序API响应:', response)
    if (response.code === 200 || response.code === 0) {
      console.log('排序保存成功')
    } else {
      console.error('排序保存失败:', response.message)
      // 如果排序失败，重新获取数据以恢复正确顺序
      await fetchCarousels()
    }
  } catch (error) {
    console.error('排序保存异常:', error)
    // 如果排序失败，重新获取数据以恢复正确顺序
    await fetchCarousels()
  }
}

const onDragEnd = async () => {
  draggedIndex.value = null
  // 保存排序
  await saveOrder()
}

const loading = ref(false)

const fetchCarousels = async () => {
  try {
    loading.value = true
    const response = await carouselApi.getList()
    console.log('API响应:', response)
    if (response.code === 200 || response.code === 0) {
      carouselItems.value = response.data
      pagination.value.total = carouselItems.value.length
    } else {
      console.error('获取轮播列表失败:', response.message)
    }
  } catch (error) {
    console.error('获取轮播列表异常:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCarousels()
})
</script>

<template>
  <div class="h-screen overflow-hidden bg-gradient-to-br from-slate-50 via-gray-50 to-slate-100 relative">
    <div class="absolute inset-0 opacity-30" style="background-image: url('data:image/svg+xml,%3Csvg width=&quot;60&quot; height=&quot;60&quot; viewBox=&quot;0 0 60 60&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;%3E%3Cg fill=&quot;none&quot; fill-rule=&quot;evenodd&quot;%3E%3Cg fill=&quot;%239C92AC&quot; fill-opacity=&quot;0.15&quot;%3E%3Cpath d=&quot;M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z&quot;/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
    <div class="max-w-7xl mx-auto px-8 py-6 h-full flex flex-col relative">
      <!-- Header -->
      <div class="mb-4 flex-shrink-0">
        <div class="flex items-center gap-4 mb-2">
          <div class="p-3 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl shadow-lg shadow-indigo-200">
            <Layers class="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-900 via-gray-700 to-gray-600 bg-clip-text text-transparent">
              轮播文案管理
            </h1>
            <p class="text-gray-500 mt-1 font-medium">管理首页轮播图展示的文案内容</p>
          </div>
        </div>
      </div>

      <!-- Action Button -->
      <div class="flex justify-end mb-3 flex-shrink-0">
        <Button @click="openAddDrawer" class="h-10 px-5 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 shadow-lg shadow-indigo-200">
          <Plus class="w-4 h-4 mr-2" />
          新增轮播
        </Button>
      </div>

      <!-- Table -->
      <Card class="border-0 shadow-xl shadow-gray-200/50 bg-white/90 backdrop-blur-sm overflow-hidden rounded-2xl flex-1 flex flex-col min-h-0">
        <div class="overflow-auto flex-1">
          <table class="w-full">
            <thead class="sticky top-0 z-10">
              <tr class="bg-gradient-to-r from-slate-100 via-gray-100 to-slate-100 border-b-2 border-gray-200">
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide w-20">序号</th>
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide">文案内容</th>
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide w-28">状态</th>
                <th class="text-center py-5 px-6 font-bold text-gray-700 text-sm tracking-wide w-36">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr 
                v-for="(item, index) in carouselItems" 
                :key="item.id"
                draggable="true"
                @dragstart="onDragStart(index)"
                @dragover="(e) => onDragOver(e, index)"
                @dragend="onDragEnd"
                class="hover:bg-gradient-to-r hover:from-indigo-50/50 hover:via-blue-50/30 hover:to-cyan-50/20 transition-all duration-300 group cursor-move"
                :class="draggedIndex === index ? 'opacity-40 bg-indigo-50' : ''"
              >
                <td class="py-4 px-6">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
                      <GripVertical class="w-4 h-4 text-gray-400" />
                    </div>
                    <span class="text-sm font-semibold text-gray-600 bg-gray-100 px-3 py-1 rounded-full">{{ item.sort_order }}</span>
                  </div>
                </td>
                <td class="py-4 px-6">
                  <div class="max-w-xl">
                    <p class="text-gray-800 font-medium leading-relaxed">{{ item.description }}</p>
                  </div>
                </td>
                <td class="py-4 px-6">
                  <button 
                    @click="toggleVisibility(item)"
                    class="inline-flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200 w-20"
                    :class="item.is_visible 
                      ? 'bg-emerald-100 text-emerald-700 border border-emerald-200' 
                      : 'bg-gray-100 text-gray-500 border border-gray-200'"
                  >
                    <Eye v-if="item.is_visible" class="w-3.5 h-3.5 flex-shrink-0" />
                    <EyeOff v-else class="w-3.5 h-3.5 flex-shrink-0" />
                    <span class="whitespace-nowrap">{{ item.is_visible ? '展示中' : '已隐藏' }}</span>
                  </button>
                </td>
                <td class="py-4 px-6">
                  <div class="flex items-center justify-center gap-3">
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      @click="openEditDrawer(item)"
                      class="bg-white border border-gray-200 shadow-sm hover:bg-gradient-to-r hover:from-indigo-50 hover:to-blue-50 hover:border-indigo-200 hover:shadow-md transition-all duration-200"
                    >
                      <Edit class="w-4 h-4 mr-1.5 text-indigo-500" />
                      <span class="text-gray-600">编辑</span>
                    </Button>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      @click="handleDelete(item.id)" 
                      class="bg-white border border-gray-200 shadow-sm hover:bg-gradient-to-r hover:from-red-50 hover:to-orange-50 hover:border-red-200 hover:shadow-md transition-all duration-200"
                    >
                      <Trash2 class="w-4 h-4 mr-1.5 text-red-500" />
                      <span class="text-gray-600">删除</span>
                    </Button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          
          <div v-if="carouselItems.length === 0" class="py-16 text-center">
            <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center shadow-inner">
              <Layers class="w-10 h-10 text-gray-400" />
            </div>
            <p class="text-gray-500 font-medium">暂无轮播数据</p>
            <p class="text-gray-400 text-sm mt-1">点击上方"新增轮播"按钮添加数据</p>
          </div>
        </div>

        <!-- Pagination (always show) -->
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
  <Drawer :open="drawerOpen" :title="drawerMode === 'add' ? '新增轮播' : '编辑轮播'" position="right" width="520px" @close="closeDrawer">
    <div class="p-6 space-y-5">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          <div class="flex items-center gap-2">
            文案内容
            <span class="text-red-500 ml-1">*</span>
          </div>
        </label>
        <textarea
          v-model="formData.description"
          class="flex min-h-[120px] w-full rounded-lg border border-gray-200 bg-white px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-200 focus:border-indigo-300"
          placeholder="请输入轮播文案内容"
          maxlength="35"
        />
        <div class="text-right mt-1 text-xs" :class="formData.description.length > 30 ? 'text-red-500' : 'text-gray-400'">
          {{ formData.description.length }}/35
        </div>
      </div>



      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          <div class="flex items-center gap-2">
            <Eye class="w-4 h-4 text-gray-500" />
            状态
          </div>
        </label>
        <div class="flex gap-3">
          <button
            type="button"
            @click="formData.is_visible = true"
            class="flex-1 py-3 px-4 rounded-lg border-2 transition-all duration-200 flex items-center justify-center gap-2"
            :class="formData.is_visible 
              ? 'border-indigo-500 bg-indigo-50 text-indigo-700' 
              : 'border-gray-200 bg-white text-gray-500 hover:border-gray-300'"
          >
            <Eye class="w-4 h-4" />
            展示
          </button>
          <button
            type="button"
            @click="formData.is_visible = false"
            class="flex-1 py-3 px-4 rounded-lg border-2 transition-all duration-200 flex items-center justify-center gap-2"
            :class="!formData.is_visible 
              ? 'border-gray-400 bg-gray-100 text-gray-700' 
              : 'border-gray-200 bg-white text-gray-500 hover:border-gray-300'"
          >
            <EyeOff class="w-4 h-4" />
            隐藏
          </button>
        </div>
      </div>

      <div class="pt-6 border-t border-gray-100">
        <Button 
          @click="handleSave" 
          :disabled="loading"
          class="w-full h-12 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 shadow-lg shadow-indigo-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Save v-if="!loading" class="w-4 h-4 mr-2" />
          <svg v-else class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ loading ? '保存中...' : (drawerMode === 'add' ? '创建轮播' : '保存修改') }}
        </Button>
      </div>
    </div>
  </Drawer>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

tbody tr {
  transition: all 0.2s ease;
}

tbody tr:hover {
  transform: translateX(4px);
}
</style>
