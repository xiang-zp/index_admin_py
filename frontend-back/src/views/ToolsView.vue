<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Drawer from '@/components/ui/Drawer.vue'
import { toolsApi } from '@/services/tools'
import { vTruncate } from '@/directives/truncate'
import { toast } from '@/lib/toast'
import {
  Box,
  Plus,
  Edit,
  Trash2,
  Search,
  RefreshCw,
  Layers,
  Image as ImageIcon,
  Eye,
  EyeOff,
  Settings,
  Upload,
  X,
  Save,
  Check,
  ChevronDown
} from 'lucide-vue-next'

import type { Tool } from '@/services/tools'

const API_BASE = 'http://localhost:8000'

const tools = ref<Tool[]>([])
const loading = ref(true)
const saving = ref(false)
const detailLoading = ref(false)
const imageProcessing = ref(false)
const imagePreviewLoading = ref(false)
const modalImageLoading = ref(false)
const drawerOpen = ref(false)
const drawerMode = ref<'add' | 'edit'>('add')
const tempImageFile = ref<File | null>(null)
const tempImagePreview = ref<string>('')
const previewImageOpen = ref(false)
const previewImageUrl = ref('')

const columnWidths = ref({
  id: 112,
  title: 150,
  description: 200,
  image: 128,
  row: 112,
  status: 112,
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

const searchForm = ref({
  title: '',
  description: ''
})

const formData = ref({
  id: '',
  title: '',
  description: '',
  image: '',
  row: 'row1',
  is_visible: true
})

const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0
})

const busy = computed(() => saving.value || detailLoading.value || imageProcessing.value)
const busyText = computed(() => {
  if (saving.value) return '保存中...'
  if (detailLoading.value) return '加载中...'
  if (imageProcessing.value) return '图片处理中...'
  return ''
})

const currentPreviewSrc = computed(() => tempImagePreview.value || formData.value.image)

watch(
  currentPreviewSrc,
  (src) => {
    imagePreviewLoading.value = !!src
  },
  { immediate: true }
)

watch(previewImageOpen, (open) => {
  if (!open) modalImageLoading.value = false
})

watch(previewImageUrl, (src) => {
  if (previewImageOpen.value && src) modalImageLoading.value = true
})

const filteredTools = computed(() => {
  const titleKeyword = searchForm.value.title.toLowerCase().trim()
  const descKeyword = searchForm.value.description.toLowerCase().trim()
  
  return tools.value.filter(t => {
    const matchTitle = !titleKeyword || t.title.toLowerCase().includes(titleKeyword)
    const matchDesc = !descKeyword || t.description.toLowerCase().includes(descKeyword)
    return matchTitle && matchDesc
  })
})

const getImageUrl = (imagePath: string | undefined) => {
  if (!imagePath) return ''
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://') || imagePath.startsWith('data:')) {
    return imagePath
  }
  return `${API_BASE}${imagePath}`
}

const formatDate = (dateStr: string | undefined) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}`
}

const resetForm = () => {
  formData.value = { id: '', title: '', description: '', image: '', row: 'row1', is_visible: true }
  tempImageFile.value = null
  tempImagePreview.value = ''
}

const openAddDrawer = () => {
  resetForm()
  drawerMode.value = 'add'
  drawerOpen.value = true
}

const openEditDrawer = async (tool: Tool) => {
  const maxRetries = 5
  const retryDelay = 3000

  formData.value = {
    id: tool.id,
    title: tool.title,
    description: tool.description,
    image: tool.image,
    row: tool.row || 'row1',
    is_visible: tool.is_visible
  }
  tempImageFile.value = null
  tempImagePreview.value = getImageUrl(tool.image) || ''
  drawerMode.value = 'edit'
  drawerOpen.value = true

  if (!tool.id) return

  const loadDetail = async (retryCount = 0) => {
    try {
      detailLoading.value = true
      const response = await toolsApi.get(tool.id)
      if ((response.code === 200 || response.code === 0) && response.data) {
        formData.value = {
          id: response.data.id,
          title: response.data.title,
          description: response.data.description,
          image: response.data.image,
          row: response.data.row || 'row1',
          is_visible: response.data.is_visible
        }
        tempImagePreview.value = getImageUrl(response.data.image) || ''
      } else {
        if (retryCount < maxRetries) {
          console.log(`获取项目详情失败，${retryDelay / 1000}秒后重试 (${retryCount + 1}/${maxRetries})...`)
          setTimeout(() => loadDetail(retryCount + 1), retryDelay)
        } else {
          alert('获取项目详情失败: ' + (response.message || '未知错误'))
        }
      }
    } catch (e) {
      console.error('获取项目详情失败:', e)
      if (retryCount < maxRetries) {
        console.log(`获取项目详情异常，${retryDelay / 1000}秒后重试 (${retryCount + 1}/${maxRetries})...`)
        setTimeout(() => loadDetail(retryCount + 1), retryDelay)
      } else {
        alert('获取项目详情异常，请检查网络连接')
      }
    } finally {
      if (retryCount === 0) {
        detailLoading.value = false
      }
    }
  }

  loadDetail()
}

const closeDrawer = () => {
  drawerOpen.value = false
  resetForm()
}

const handleSave = async (retryCount = 0) => {
  const maxRetries = 5
  const retryDelay = 3000

  if (!formData.value.title || !formData.value.description) {
    alert('请填写标题和描述')
    return
  }

  if (retryCount === 0) {
    saving.value = true
  }

  try {
    const requestData: any = {
      title: formData.value.title,
      description: formData.value.description,
      is_visible: formData.value.is_visible
    }

    if (formData.value.image) {
      requestData.image = formData.value.image
    }

    let response
    if (drawerMode.value === 'add') {
      response = await toolsApi.create(requestData)
    } else {
      if (!formData.value.id) {
        alert('更新错误：缺少ID')
        saving.value = false
        return
      }
      requestData.id = formData.value.id
      response = await toolsApi.update(requestData)
    }

    if (response.code === 200) {
      await loadTools()
      closeDrawer()
      saving.value = false
    } else {
      if (retryCount < maxRetries) {
        console.log(`保存失败，${retryDelay / 1000}秒后重试 (${retryCount + 1}/${maxRetries})...`)
        setTimeout(() => handleSave(retryCount + 1), retryDelay)
      } else {
        saving.value = false
        alert('保存失败: ' + (response.message || '未知错误'))
      }
    }
  } catch (error: any) {
    console.error('保存异常:', error)
    if (error.code === 'ECONNABORTED') {
      saving.value = false
      alert('保存超时，图片可能过大，请尝试压缩图片后重试')
    } else if (retryCount < maxRetries) {
      console.log(`保存异常，${retryDelay / 1000}秒后重试 (${retryCount + 1}/${maxRetries})...`)
      setTimeout(() => handleSave(retryCount + 1), retryDelay)
    } else {
      saving.value = false
      alert('保存异常，请检查网络连接')
    }
  }
}

const handleDelete = async (id: string, retryCount = 0) => {
  const maxRetries = 5
  const retryDelay = 3000

  if (!confirm('确定要删除这个项目吗？')) return
  
  try {
    loading.value = true
    const response = await toolsApi.delete(id)
    if (response.code === 200) {
      await loadTools()
    } else {
      if (retryCount < maxRetries) {
        console.log(`删除失败，${retryDelay / 1000}秒后重试 (${retryCount + 1}/${maxRetries})...`)
        setTimeout(() => handleDelete(id, retryCount + 1), retryDelay)
      } else {
        alert('删除失败: ' + (response.message || '未知错误'))
      }
    }
  } catch (error) {
    console.error('删除异常:', error)
    if (retryCount < maxRetries) {
      console.log(`删除异常，${retryDelay / 1000}秒后重试 (${retryCount + 1}/${maxRetries})...`)
      setTimeout(() => handleDelete(id, retryCount + 1), retryDelay)
    } else {
      alert('删除异常，请检查网络连接')
    }
  } finally {
    if (retryCount === 0) {
      loading.value = false
    }
  }
}

const handleReset = () => {
  searchForm.value = { title: '', description: '' }
}

const handleSearch = () => {
  loading.value = true
  setTimeout(() => loading.value = false, 300)
}

const toggleVisibility = async (tool: Tool, retryCount = 0) => {
  const maxRetries = 5
  const retryDelay = 3000

  if (!tool.id) return
  
  try {
    loading.value = true
    const response = await toolsApi.toggleVisible(tool.id)
    if (response.code === 200) {
      await loadTools()
    } else {
      if (retryCount < maxRetries) {
        console.log(`切换状态失败，${retryDelay / 1000}秒后重试 (${retryCount + 1}/${maxRetries})...`)
        setTimeout(() => toggleVisibility(tool, retryCount + 1), retryDelay)
      } else {
        alert('切换状态失败: ' + (response.message || '未知错误'))
      }
    }
  } catch (error) {
    console.error('切换状态异常:', error)
    if (retryCount < maxRetries) {
      console.log(`切换状态异常，${retryDelay / 1000}秒后重试 (${retryCount + 1}/${maxRetries})...`)
      setTimeout(() => toggleVisibility(tool, retryCount + 1), retryDelay)
    } else {
      alert('切换状态异常，请检查网络连接')
    }
  } finally {
    if (retryCount === 0) {
      loading.value = false
    }
  }
}

const getVisibilityClass = (visible: boolean) => {
  return visible ? 'text-emerald-600 bg-emerald-50' : 'text-gray-400 bg-gray-50'
}

const getImagePlaceholder = (title: string) => {
  const colors = [
    'from-indigo-500 to-purple-600',
    'from-emerald-500 to-teal-600',
    'from-rose-500 to-pink-600',
    'from-amber-500 to-orange-600',
    'from-violet-500 to-indigo-600',
    'from-cyan-500 to-blue-600'
  ]
  const index = title.charCodeAt(0) % colors.length
  return colors[index]
}

const readFileAsDataURL = (file: File) => {
  return new Promise<string>((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => resolve((e.target?.result as string) || '')
    reader.onerror = () => reject(new Error('读取文件失败'))
    reader.readAsDataURL(file)
  })
}

const loadImageFromDataURL = (dataUrl: string) => {
  return new Promise<HTMLImageElement>((resolve, reject) => {
    const img = new Image()
    img.onload = () => resolve(img)
    img.onerror = () => reject(new Error('加载图片失败'))
    img.src = dataUrl
  })
}

const canvasToBlob = (canvas: HTMLCanvasElement, type: string, quality: number) => {
  return new Promise<Blob>((resolve, reject) => {
    canvas.toBlob(
      (blob) => {
        if (!blob) {
          reject(new Error('图片压缩失败'))
          return
        }
        resolve(blob)
      },
      type,
      quality
    )
  })
}

const compressImageFile = async (
  file: File,
  options: {
    maxSide?: number
    maxBytes?: number
    type?: string
  } = {}
) => {
  const maxSide = options.maxSide ?? 1280
  const maxBytes = options.maxBytes ?? 220 * 1024
  const outputType = options.type ?? 'image/webp'

  const originalDataUrl = await readFileAsDataURL(file)
  const img = await loadImageFromDataURL(originalDataUrl)

  let targetWidth = img.naturalWidth
  let targetHeight = img.naturalHeight
  const longestSide = Math.max(targetWidth, targetHeight)
  if (longestSide > maxSide) {
    const scale = maxSide / longestSide
    targetWidth = Math.max(1, Math.round(targetWidth * scale))
    targetHeight = Math.max(1, Math.round(targetHeight * scale))
  }

  const canvas = document.createElement('canvas')
  canvas.width = targetWidth
  canvas.height = targetHeight
  const ctx = canvas.getContext('2d')
  if (!ctx) throw new Error('无法创建画布')
  ctx.drawImage(img, 0, 0, targetWidth, targetHeight)

  let quality = 0.85
  let blob = await canvasToBlob(canvas, outputType, quality)

  while (blob.size > maxBytes && quality > 0.45) {
    quality = Math.max(0.45, quality - 0.08)
    blob = await canvasToBlob(canvas, outputType, quality)
  }

  const compressedFile = new File([blob], file.name.replace(/\.[^/.]+$/, '') + '.webp', { type: outputType })
  const compressedDataUrl = await readFileAsDataURL(compressedFile)

  return {
    file: compressedFile,
    dataUrl: compressedDataUrl,
    originalBytes: file.size,
    compressedBytes: blob.size
  }
}

const handleImageUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (file) {
    if (!file.type.startsWith('image/')) {
      alert('请上传图片文件')
      return
    }
    if (file.size > 20 * 1024 * 1024) {
      alert('图片大小不能超过20MB')
      return
    }

    const shouldBypassCompression = file.type === 'image/gif' || file.type === 'image/svg+xml'
    const isCompressible = /^(image\/jpeg|image\/png|image\/webp|image\/bmp|image\/heic|image\/heif)$/.test(file.type)

    try {
      imageProcessing.value = true
      if (shouldBypassCompression || !isCompressible) {
        const dataUrl = await readFileAsDataURL(file)
        tempImageFile.value = file
        tempImagePreview.value = dataUrl
        formData.value.image = dataUrl
        return
      }

      const { file: compressedFile, dataUrl } = await compressImageFile(file)
      tempImageFile.value = compressedFile
      tempImagePreview.value = dataUrl
      formData.value.image = dataUrl
    } catch (e: any) {
      console.error('图片处理失败:', e)
      alert('图片处理失败，请更换图片或使用图片链接')
    } finally {
      imageProcessing.value = false
      input.value = ''
    }
  }
}

const clearImage = () => {
  tempImageFile.value = null
  tempImagePreview.value = ''
  formData.value.image = ''
}

const openImagePreview = (imageUrl: string) => {
  if (!imageUrl) return
  modalImageLoading.value = true
  previewImageUrl.value = imageUrl
  previewImageOpen.value = true
}

const closeImagePreview = () => {
  previewImageOpen.value = false
  previewImageUrl.value = ''
}

const loadTools = async (retryCount = 0) => {
  const maxRetries = 5
  const retryDelay = 3000

  try {
    loading.value = true
    const response = await toolsApi.getList()
    if (response.code === 200 || response.code === 0) {
      tools.value = Array.isArray(response.data) ? response.data : []
      pagination.value.total = tools.value.length
    } else {
      if (retryCount < maxRetries) {
        console.log(`加载失败，${retryDelay / 1000}秒后重试 (${retryCount + 1}/${maxRetries})...`)
        setTimeout(() => loadTools(retryCount + 1), retryDelay)
      } else {
        alert('加载失败: ' + (response.message || '未知错误'))
      }
    }
  } catch (error) {
    console.error('加载异常:', error)
    if (retryCount < maxRetries) {
      console.log(`加载异常，${retryDelay / 1000}秒后重试 (${retryCount + 1}/${maxRetries})...`)
      setTimeout(() => loadTools(retryCount + 1), retryDelay)
    } else {
      alert('加载异常，请检查网络连接')
    }
  } finally {
    if (retryCount === 0) {
      loading.value = false
    }
  }
}

onMounted(() => {
  loadTools()
})
</script>

<template>
  <div class="h-screen overflow-hidden bg-gradient-to-br from-stone-50 via-slate-50 to-stone-100">
    <div class="max-w-7xl mx-auto px-8 py-6 h-full flex flex-col">
      <!-- Header -->
      <div class="mb-4 flex-shrink-0">
        <div class="flex items-center gap-4 mb-2">
          <div class="p-3 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl shadow-lg shadow-emerald-200">
            <Box class="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-900 via-gray-700 to-gray-600 bg-clip-text text-transparent">
              开源项目管理
            </h1>
            <p class="text-gray-500 mt-1 font-medium">管理前台显示的开源项目分享</p>
          </div>
        </div>
      </div>

      <!-- Search -->
      <Card class="border-0 shadow-xl shadow-gray-200/50 bg-white/80 backdrop-blur-sm mb-4 flex-shrink-0">
        <CardContent class="py-4 px-5">
          <div class="flex flex-wrap gap-4 items-end">
            <div class="flex gap-4 flex-1 min-w-[400px]">
              <div class="flex-1 min-w-[180px]">
                <label class="block text-xs font-medium text-gray-500 mb-1.5">按标题搜索</label>
                <div class="relative">
                  <Layers class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <Input 
                    v-model="searchForm.title"
                    placeholder="输入项目标题" 
                    class="pl-10 h-10 bg-gray-50/50 border-gray-200 focus:bg-white transition-all duration-300"
                  />
                </div>
              </div>
              <div class="flex-1 min-w-[180px]">
                <label class="block text-xs font-medium text-gray-500 mb-1.5">按描述搜索</label>
                <div class="relative">
                  <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <Input 
                    v-model="searchForm.description"
                    placeholder="输入描述关键词" 
                    class="pl-10 h-10 bg-gray-50/50 border-gray-200 focus:bg-white transition-all duration-300"
                  />
                </div>
              </div>
            </div>
            <div class="flex gap-3">
              <Button variant="outline" @click="handleReset" class="h-10 px-4 hover:bg-gray-50">
                <RefreshCw class="w-4 h-4 mr-2" />
                重置
              </Button>
              <Button @click="handleSearch" class="h-10 px-4 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 shadow-lg shadow-emerald-200">
                <Search class="w-4 h-4 mr-2" />
                搜索
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Action Button -->
      <div class="flex justify-end mb-3 flex-shrink-0">
        <Button @click="openAddDrawer" class="h-10 px-5 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 shadow-lg shadow-emerald-200">
          <Plus class="w-4 h-4 mr-2" />
          新增项目
        </Button>
      </div>

      <!-- Table -->
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
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide relative select-none group" :style="{ width: columnWidths.image + 'px', minWidth: columnWidths.image + 'px' }">
                  图片
                  <div 
                    class="absolute right-0 top-0 bottom-0 w-1.5 cursor-col-resize group-hover:w-2 transition-all duration-150 z-20 flex items-center justify-center"
                    @mousedown="(e: MouseEvent) => startResize(e, 'image')"
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
                <th class="text-left py-5 px-6 font-bold text-gray-700 text-sm tracking-wide relative select-none group" :style="{ width: columnWidths.updated_at + 'px', minWidth: columnWidths.updated_at + 'px' }">
                  更新时间
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
            <tbody class="divide-y divide-gray-100">
              <tr v-if="loading">
                <td colspan="6" class="py-24 text-center">
                  <div class="flex flex-col items-center justify-center gap-3">
                    <div class="w-10 h-10 rounded-full border-4 border-emerald-100 border-t-emerald-500 animate-spin"></div>
                    <p class="text-gray-500 font-medium animate-pulse">正在加载数据...</p>
                  </div>
                </td>
              </tr>
              <template v-else>
                <tr 
                  v-for="tool in filteredTools" 
                  :key="tool.id"
                  class="hover:bg-gradient-to-r hover:from-indigo-50/50 hover:via-blue-50/30 hover:to-cyan-50/20 transition-all duration-300 group"
                >
                  <td class="py-4 px-6" :style="{ width: columnWidths.id + 'px' }">
                    <span class="font-mono text-sm text-gray-500">{{ tool.id }}</span>
                  </td>
                  <td class="py-4 px-6" :style="{ width: columnWidths.title + 'px' }">
                    <span class="text-gray-800 font-medium block w-[10ch] break-all">{{ tool.title || '未命名项目' }}</span>
                  </td>
                  <td class="py-4 px-6" :style="{ width: columnWidths.description + 'px' }">
                    <div class="relative group/desc">
                      <p 
                        v-truncate="(isTruncated: boolean) => { tool._isTruncated = isTruncated }"
                        class="text-gray-600 line-clamp-2 text-sm leading-relaxed"
                      >
                        {{ tool.description || '暂无描述' }}
                      </p>
                      <div v-if="tool.description && tool._isTruncated" class="absolute left-0 top-full mt-2 z-[100] invisible group-hover/desc:visible opacity-0 group-hover/desc:opacity-100 transition-all duration-200">
                        <div class="relative">
                          <div class="bg-gray-900 text-white text-sm px-4 py-3 rounded-lg shadow-xl w-[20em] break-all leading-relaxed">
                            {{ tool.description }}
                          </div>
                          <div class="absolute left-4 bottom-full -mb-1 w-0 h-0 border-l-[8px] border-l-transparent border-r-[8px] border-r-transparent border-b-[8px] border-b-gray-900"></div>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="py-4 px-6" :style="{ width: columnWidths.image + 'px' }">
                    <div v-if="tool.image" class="relative group/image">
                      <img :src="getImageUrl(tool.image)" alt="项目图片" class="w-12 h-12 rounded-lg object-cover shadow-md cursor-pointer hover:scale-105 transition-transform duration-200" @click="openImagePreview(getImageUrl(tool.image))" />
                    </div>
                    <div v-else :class="['w-12 h-12 rounded-lg flex items-center justify-center shadow-md bg-gradient-to-br', getImagePlaceholder(tool.title)]">
                      <ImageIcon class="w-5 h-5 text-white/80" />
                    </div>
                  </td>
                  <td class="py-4 px-6" :style="{ width: columnWidths.row + 'px' }">
                    <span :class="[
                      'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border',
                      tool.row === 'row2' ? 'bg-violet-100 text-violet-700 border-violet-200' : 'bg-blue-100 text-blue-700 border-blue-200'
                    ]">
                      {{ tool.row === 'row2' ? '第二行' : '第一行' }}
                    </span>
                  </td>
                  <td class="py-4 px-6" :style="{ width: columnWidths.status + 'px' }">
                    <button 
                      @click="toggleVisibility(tool)"
                      class="inline-flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200 w-20"
                      :class="getVisibilityClass(tool.is_visible)"
                    >
                      <Eye v-if="tool.is_visible" class="w-3.5 h-3.5 flex-shrink-0" />
                      <EyeOff v-else class="w-3.5 h-3.5 flex-shrink-0" />
                      <span class="whitespace-nowrap">{{ tool.is_visible ? '展示中' : '已隐藏' }}</span>
                    </button>
                  </td>
                  <td class="py-4 px-6" :style="{ width: columnWidths.updated_at + 'px' }">
                    <span class="text-sm text-gray-500">{{ formatDate(tool.updated_at) }}</span>
                  </td>
                  <td class="py-4 px-6" :style="{ width: columnWidths.action + 'px' }">
                    <div class="flex items-center justify-center gap-3">
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        @click="openEditDrawer(tool)"
                        class="bg-white border border-gray-200 shadow-sm hover:bg-gradient-to-r hover:from-indigo-50 hover:to-blue-50 hover:border-indigo-200 hover:shadow-md transition-all duration-200"
                      >
                        <Edit class="w-4 h-4 mr-1.5 text-indigo-500" />
                        <span class="text-gray-600">编辑</span>
                      </Button>
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        @click="handleDelete(tool.id)" 
                        class="bg-white border border-gray-200 shadow-sm hover:bg-gradient-to-r hover:from-red-50 hover:to-orange-50 hover:border-red-200 hover:shadow-md transition-all duration-200"
                      >
                        <Trash2 class="w-4 h-4 mr-1.5 text-red-500" />
                        <span class="text-gray-600">删除</span>
                      </Button>
                    </div>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>

        <div v-if="!loading && filteredTools.length === 0" class="py-16 text-center">
          <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-gray-100 flex items-center justify-center">
            <Box class="w-10 h-10 text-gray-300" />
          </div>
          <p class="text-gray-500">暂无项目数据</p>
        </div>

        <!-- Pagination -->
        <div class="flex items-center justify-between px-6 py-4 border-t border-gray-100 bg-gray-50/50 flex-shrink-0">
          <div class="flex items-center gap-2 text-sm text-gray-500">
            <span class="font-medium">每页 {{ pagination.pageSize }} 条</span>
            <span class="text-gray-300">|</span>
            <span>共 {{ filteredTools.length }} 条记录</span>
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
  <Drawer :open="drawerOpen" :title="drawerMode === 'add' ? '新增项目' : '编辑项目'" position="right" width="520px" @close="closeDrawer">
    <div class="p-6 space-y-5">
      <div v-if="busy" class="flex items-center gap-2 px-3 py-2 rounded-lg bg-emerald-50 border border-emerald-100 text-emerald-700">
        <div class="w-4 h-4 rounded-full border-2 border-emerald-200 border-t-emerald-600 animate-spin"></div>
        <p class="text-sm font-medium">{{ busyText }}</p>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          <div class="flex items-center gap-2">
            <Box class="w-4 h-4 text-gray-500" />
            标题
            <span class="text-red-500 ml-1">*</span>
          </div>
        </label>
        <Input v-model="formData.title" placeholder="请输入项目标题（最多10字）" class="h-11" maxlength="10" />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          <div class="flex items-center gap-2">
            <Layers class="w-4 h-4 text-gray-500" />
            描述
            <span class="text-red-500 ml-1">*</span>
          </div>
        </label>
        <textarea
          v-model="formData.description"
          class="flex min-h-[100px] w-full rounded-lg border border-gray-200 bg-white px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-200 focus:border-emerald-300"
          placeholder="请输入项目描述"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          <div class="flex items-center gap-2">
            <ImageIcon class="w-4 h-4 text-gray-500" />
            图片
          </div>
        </label>
        
        <div v-if="!tempImagePreview && !formData.image" class="mt-2">
          <div 
            @click="($refs.fileInput as HTMLInputElement)?.click()"
            class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-emerald-500 hover:bg-emerald-50/50 transition-colors"
          >
            <Upload class="w-8 h-8 mx-auto text-gray-400 mb-2" />
            <p class="text-sm text-gray-500">点击上传图片</p>
            <p class="text-xs text-gray-400 mt-1">支持 PNG、JPG、GIF，最大 20MB（会自动压缩）</p>
          </div>
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="handleImageUpload"
          />
          
          <div class="mt-3">
            <p class="text-xs text-gray-400 mb-2">或输入图片地址</p>
            <Input 
              v-model="formData.image" 
              placeholder="https://example.com/image.jpg"
              class="h-10"
            />
          </div>
        </div>
        
        <div v-else class="mt-2 space-y-3">
          <div class="relative inline-block">
            <img
              :src="tempImagePreview || getImageUrl(formData.image)"
              alt="图片预览"
              class="h-24 rounded-lg object-cover border-2 border-gray-200 bg-white p-1"
              @load="imagePreviewLoading = false"
              @error="imagePreviewLoading = false"
            />
            <div v-if="imagePreviewLoading" class="mt-2 flex items-center gap-2 text-xs text-gray-500">
              <div class="w-3.5 h-3.5 rounded-full border-2 border-gray-200 border-t-emerald-600 animate-spin"></div>
              <span>图片加载中...</span>
            </div>
            <button
              @click="clearImage"
              class="absolute -top-2 -right-2 p-1.5 bg-red-500 text-white rounded-full hover:bg-red-600 shadow-lg"
            >
              <X class="w-3.5 h-3.5" />
            </button>
          </div>
          
          <div class="flex items-center gap-2">
            <div class="h-px flex-1 bg-gray-200"></div>
            <span class="text-xs text-gray-400">或输入新图片地址</span>
            <div class="h-px flex-1 bg-gray-200"></div>
          </div>
          
          <Input 
            v-model="formData.image" 
            placeholder="https://example.com/image.jpg"
            class="h-10"
          />
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          <div class="flex items-center gap-2">
            <Layers class="w-4 h-4 text-gray-500" />
            展示位置
          </div>
        </label>
        <div class="flex gap-3">
          <button
            type="button"
            @click="formData.row = 'row1'"
            class="flex-1 py-3 px-4 rounded-lg border-2 transition-all duration-200 flex items-center justify-center gap-2"
            :class="formData.row === 'row1' 
              ? 'border-blue-500 bg-blue-50 text-blue-700' 
              : 'border-gray-200 bg-white text-gray-500 hover:border-gray-300'"
          >
            <Check v-if="formData.row === 'row1'" class="w-4 h-4" />
            第一行
          </button>
          <button
            type="button"
            @click="formData.row = 'row2'"
            class="flex-1 py-3 px-4 rounded-lg border-2 transition-all duration-200 flex items-center justify-center gap-2"
            :class="formData.row === 'row2' 
              ? 'border-violet-500 bg-violet-50 text-violet-700' 
              : 'border-gray-200 bg-white text-gray-500 hover:border-gray-300'"
          >
            <Check v-if="formData.row === 'row2'" class="w-4 h-4" />
            第二行
          </button>
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          <div class="flex items-center gap-2">
            <Eye class="w-4 h-4 text-gray-500" />
            是否展示
          </div>
        </label>
        <div class="flex gap-3">
          <button
            type="button"
            @click="formData.is_visible = true"
            class="flex-1 py-3 px-4 rounded-lg border-2 transition-all duration-200 flex items-center justify-center gap-2"
            :class="formData.is_visible 
              ? 'border-emerald-500 bg-emerald-50 text-emerald-700' 
              : 'border-gray-200 bg-white text-gray-500 hover:border-gray-300'"
          >
            <Check v-if="formData.is_visible" class="w-4 h-4" />
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
        <Button @click="handleSave" :disabled="busy" class="w-full h-12 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 shadow-lg shadow-emerald-200">
          <div v-if="saving" class="w-4 h-4 mr-2 rounded-full border-2 border-white/60 border-t-white animate-spin"></div>
          <Save v-else class="w-4 h-4 mr-2" />
          {{ saving ? '保存中...' : (drawerMode === 'add' ? '创建项目' : '保存修改') }}
        </Button>
      </div>
    </div>
  </Drawer>

  <!-- Image Preview Modal -->
  <div v-if="previewImageOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm" @click="closeImagePreview">
    <Card class="w-full max-w-4xl mx-4 border-0 shadow-2xl bg-white/95 backdrop-blur-sm animate-scale-in" @click.stop>
      <CardContent class="pt-6">
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-gradient-to-br from-emerald-100 to-teal-100 rounded-lg">
              <ImageIcon class="w-5 h-5 text-emerald-600" />
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">图片预览</h3>
              <p class="text-sm text-gray-500">点击图片外区域关闭</p>
            </div>
          </div>
          <Button variant="ghost" size="icon" @click="closeImagePreview" class="hover:bg-gray-100 rounded-lg">
            <X class="w-5 h-5 text-gray-400" />
          </Button>
        </div>
        
        <div class="space-y-4">
          <div class="flex justify-center">
            <img
              :src="previewImageUrl"
              alt="图片预览"
              class="max-w-full max-h-[70vh] rounded-xl object-contain border-2 border-gray-200 bg-white p-1 shadow-lg"
              :class="modalImageLoading ? 'opacity-60' : 'opacity-100'"
              @load="modalImageLoading = false"
              @error="modalImageLoading = false"
            />
          </div>
          <div v-if="modalImageLoading" class="flex items-center justify-center gap-2 text-sm text-gray-600">
            <div class="w-4 h-4 rounded-full border-2 border-gray-200 border-t-emerald-600 animate-spin"></div>
            <span>图片加载中...</span>
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t border-gray-100">
            <Button variant="outline" @click="closeImagePreview" class="h-11 px-6 hover:bg-gray-50">关闭</Button>
          </div>
        </div>
      </CardContent>
    </Card>
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

@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-scale-in {
  animation: scale-in 0.2s ease-out;
}

tbody tr {
  transition: all 0.2s ease;
}

tbody tr:hover {
  transform: translateX(4px);
}
</style>
