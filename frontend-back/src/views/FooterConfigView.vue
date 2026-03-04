<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Drawer from '@/components/ui/Drawer.vue'
import { footerApi } from '@/services/footer'
import { toast } from '@/lib/toast'
import {
  Plus,
  Edit,
  Trash2,
  Link,
  Type,
  Image,
  ExternalLink,
  Upload,
  Trash
} from 'lucide-vue-next'

interface FooterLink {
  id: string
  title: string
  url: string
  sort_order?: number
  created_at?: string
  updated_at?: string
}

interface FooterConfig {
  logo_url: string
  slogan: string
  links: FooterLink[]
  updated_at?: string
}

const config = ref<FooterConfig>({
  logo_url: '',
  slogan: '',
  links: [],
  updated_at: ''
})

const drawerOpen = ref(false)
const drawerMode = ref<'add' | 'edit'>('add')
const fileInputRef = ref<HTMLInputElement | null>(null)
const logoUploading = ref(false)
const sloganSaving = ref(false)
const lastSavedSlogan = ref('')

const formData = ref({
  id: '',
  title: '',
  url: ''
})

const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0
})

const resetForm = () => {
  formData.value = { id: '', title: '', url: '' }
}

const openAddDrawer = () => {
  resetForm()
  drawerMode.value = 'add'
  drawerOpen.value = true
}

const openEditDrawer = (link: FooterLink) => {
  formData.value = {
    id: link.id,
    title: link.title,
    url: link.url
  }
  drawerMode.value = 'edit'
  drawerOpen.value = true
}

const closeDrawer = () => {
  drawerOpen.value = false
  resetForm()
}

const handleSave = async () => {
  if (!formData.value.title || !formData.value.url) {
    alert('请填写标题和链接')
    return
  }

  try {
    if (drawerMode.value === 'add') {
      await footerApi.createLink({
        title: formData.value.title,
        url: formData.value.url
      })
    } else {
      await footerApi.updateLink({
        id: formData.value.id,
        title: formData.value.title,
        url: formData.value.url
      })
    }
    
    await loadFooterData()
    closeDrawer()
  } catch (error) {
    console.error('保存链接失败:', error)
    alert('保存失败，请重试')
  }
}

const handleDelete = async (id: string) => {
  if (!confirm('确定要删除这个链接吗？')) return
  
  try {
    await footerApi.deleteLink(id)
    await loadFooterData()
  } catch (error) {
    console.error('删除链接失败:', error)
    alert('删除失败，请重试')
  }
}

const saveLogoConfig = async (logoUrl: string) => {
  logoUploading.value = true
  try {
    const updateResponse = await footerApi.updateConfig({
      logo_url: logoUrl,
      slogan: config.value.slogan // 保持原有slogan不变
    })
    if (!(updateResponse?.code === 200 || updateResponse?.code === 0)) {
      throw new Error(updateResponse?.message || '更新失败')
    }
    // 更新成功后重新加载数据确保同步
    const configResponse = await footerApi.getConfig()
    if (!(configResponse?.code === 200 || configResponse?.code === 0)) {
      throw new Error(configResponse?.message || '获取配置失败')
    }
    config.value.logo_url = configResponse.data?.logo_url || ''
    config.value.updated_at = configResponse.data?.updated_at || ''
  } catch (error) {
    console.error('保存Logo配置失败:', error)
    alert('保存Logo配置失败，请重试')
  } finally {
    logoUploading.value = false
  }
}

const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    if (!file.type.startsWith('image/')) {
      alert('请上传图片文件')
      return
    }
    if (file.size > 5 * 1024 * 1024) {
      alert('图片大小不能超过5MB')
      return
    }
    
    logoUploading.value = true
    const reader = new FileReader()
    
    reader.onload = async (e) => {
      const logoUrl = e.target?.result as string
      config.value.logo_url = logoUrl
      await saveLogoConfig(logoUrl)
    }
    
    reader.onerror = () => {
      alert('读取文件失败')
      logoUploading.value = false
    }
    
    reader.readAsDataURL(file)
  }
}

const triggerFileUpload = () => {
  fileInputRef.value?.click()
}

const clearLogo = async () => {
  if (!confirm('确定要清除Logo图片吗？')) return
  
  config.value.logo_url = ''
  if (fileInputRef.value) {
    fileInputRef.value.value = ''
  }
  
  try {
    await saveLogoConfig('')
  } catch (error) {
    console.error('清除Logo失败:', error)
    alert('清除Logo失败，请重试')
  }
}

const isValidUrl = (url: string): boolean => {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

const loadFooterData = async () => {
  try {
    // 加载配置
    const configResponse = await footerApi.getConfig()
    if (configResponse?.code === 200 || configResponse?.code === 0) {
      config.value.logo_url = configResponse.data?.logo_url || ''
      config.value.slogan = configResponse.data?.slogan || ''
      config.value.updated_at = configResponse.data?.updated_at || ''
      lastSavedSlogan.value = config.value.slogan || ''
    }
    
    // 加载链接
    const linksResponse = await footerApi.getLinks()
    if (linksResponse?.code === 200 || linksResponse?.code === 0) {
      config.value.links = Array.isArray(linksResponse.data) ? linksResponse.data : []
      pagination.value.total = config.value.links.length
    }
  } catch (error) {
    console.error('加载底部配置失败:', error)
  }
}

onMounted(() => {
  loadFooterData()
})

const saveSloganOnBlur = async () => {
  const current = (config.value.slogan || '').trim()
  const previous = (lastSavedSlogan.value || '').trim()
  if (current === previous) return
  if (sloganSaving.value) return
  sloganSaving.value = true
  try {
    const res = await footerApi.updateConfig({ slogan: config.value.slogan })
    if (!(res?.code === 200 || res?.code === 0)) {
      throw new Error(res?.message || '保存失败')
    }
    lastSavedSlogan.value = config.value.slogan || ''
    toast.success('保存成功')
  } catch (e) {
    console.error('保存底部文案失败:', e)
    toast.error('保存失败，请重试')
  } finally {
    sloganSaving.value = false
  }
}
</script>

<template>
  <div class="h-screen overflow-hidden bg-gradient-to-br from-slate-50 via-gray-50 to-slate-100">
    <div class="max-w-7xl mx-auto px-8 py-6 h-full flex flex-col">
      <!-- Header -->
      <div class="mb-4 flex-shrink-0">
        <div class="flex items-center gap-4 mb-2">
          <div class="p-3 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-2xl shadow-lg shadow-cyan-200">
            <Type class="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-900 via-gray-700 to-gray-600 bg-clip-text text-transparent">
              底部配置
            </h1>
            <p class="text-gray-500 mt-1 font-medium">管理前台首页底部的Logo、文案和链接</p>
          </div>
        </div>
      </div>

      <!-- Logo and Slogan Config -->
      <Card class="border-0 shadow-xl shadow-gray-200/50 bg-white/80 backdrop-blur-sm mb-4 flex-shrink-0">
        <CardContent class="pt-5">
          <div class="flex items-center gap-2 mb-6">
            <div class="p-2 bg-gradient-to-br from-violet-100 to-indigo-100 rounded-lg">
              <Image class="w-5 h-5 text-violet-600" />
            </div>
            <h3 class="text-lg font-semibold text-gray-800">Logo和文案配置</h3>
          </div>
          
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div class="space-y-3">
              <label class="block text-sm font-medium text-gray-700">
                <div class="flex items-center gap-2">
                  <Image class="w-4 h-4 text-gray-500" />
                  Logo图片
                </div>
              </label>
              
              <input
                ref="fileInputRef"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleFileUpload"
              />
              
              <div v-if="!config.logo_url" class="mt-2">
                <div 
                  @click="logoUploading ? null : triggerFileUpload()"
                  :class="[
                    'border-2 rounded-lg p-8 text-center transition-colors',
                    logoUploading 
                      ? 'border-cyan-300 bg-cyan-50 cursor-wait'
                      : 'border-dashed border-gray-300 cursor-pointer hover:border-cyan-500 hover:bg-cyan-50/50'
                  ]"
                >
                  <div class="relative">
                    <div v-if="logoUploading" class="absolute inset-0 flex items-center justify-center">
                      <div class="w-6 h-6 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
                    </div>
                    <Upload 
                      :class="[
                        'w-8 h-8 mx-auto mb-2 transition-opacity',
                        logoUploading ? 'opacity-30' : 'text-gray-400'
                      ]" 
                    />
                  </div>
                  <p :class="['text-sm transition-opacity', logoUploading ? 'opacity-50' : 'text-gray-500']">
                    {{ logoUploading ? '正在上传...' : '点击上传图片' }}
                  </p>
                  <p class="text-xs text-gray-400 mt-1">支持 PNG、JPG、GIF，最大 5MB</p>
                </div>
              </div>
              
              <div v-else class="mt-2 space-y-3">
                <div class="relative inline-block">
                  <img
                    :src="config.logo_url"
                    alt="Logo预览"
                    :class="[
                      'h-20 w-20 rounded-lg object-contain border-2 bg-white p-1 transition-opacity',
                      logoUploading ? 'opacity-50 border-cyan-200' : 'border-gray-200'
                    ]"
                    @error="(e) => (e.target as HTMLImageElement).style.display = 'none'"
                  />
                  <div v-if="logoUploading" class="absolute inset-0 flex items-center justify-center">
                    <div class="w-6 h-6 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
                  </div>
                  <button
                    @click="logoUploading ? null : clearLogo()"
                    :disabled="logoUploading"
                    :class="[
                      'absolute -top-2 -right-2 p-1 text-white rounded-full shadow-lg transition-all',
                      logoUploading ? 'bg-gray-400 cursor-not-allowed' : 'bg-red-500 hover:bg-red-600'
                    ]"
                  >
                    <Trash class="w-3 h-3" />
                  </button>
                </div>
              </div>
            </div>
            
            <div class="space-y-3">
              <label class="block text-sm font-medium text-gray-700">
                <div class="flex items-center gap-2">
                  <Type class="w-4 h-4 text-gray-500" />
                  底部文案
                </div>
              </label>
              <textarea
                v-model="config.slogan"
                class="flex min-h-[120px] w-full rounded-lg border border-gray-200 bg-white px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-200 focus:border-cyan-300"
                placeholder="请输入底部文案"
                :disabled="sloganSaving"
                @blur="saveSloganOnBlur"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Action Button -->
      <div class="flex justify-end mb-4">
        <Button @click="openAddDrawer" class="h-11 px-6 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 shadow-lg shadow-cyan-200">
          <Plus class="w-4 h-4 mr-2" />
          新增链接
        </Button>
      </div>

      <!-- Links Table -->
      <Card class="border-0 shadow-xl shadow-gray-200/50 bg-white/90 backdrop-blur-sm overflow-hidden rounded-2xl flex-1 flex flex-col min-h-0">
        <div class="overflow-auto flex-1">
          <table class="w-full">
            <thead class="sticky top-0 z-10">
              <tr class="bg-gradient-to-r from-slate-100 via-gray-100 to-slate-100 border-b-2 border-gray-200">
                <th class="w-28 px-5 py-5 text-left text-sm font-bold text-gray-700 tracking-wide">ID</th>
                <th class="w-48 px-5 py-5 text-left text-sm font-bold text-gray-700 tracking-wide">标题</th>
                <th class="px-5 py-5 text-left text-sm font-bold text-gray-700 tracking-wide">
                  <div class="flex items-center gap-2">
                    <Link class="w-4 h-4" />
                    链接配置
                  </div>
                </th>
                <th class="w-32 px-5 py-5 text-center text-sm font-bold text-gray-700 tracking-wide">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="link in config.links" :key="link.id" class="hover:bg-gradient-to-r hover:from-indigo-50/50 hover:via-blue-50/30 hover:to-cyan-50/20 transition-all duration-300 group">
                <td class="px-5 py-4">
                  <span class="px-3 py-1.5 bg-gradient-to-r from-gray-100 to-gray-50 rounded-lg text-sm font-mono font-medium text-gray-700">
                    {{ link.id }}
                  </span>
                </td>
                <td class="px-5 py-4">
                  <span class="font-medium text-gray-900">{{ link.title }}</span>
                </td>
                <td class="px-5 py-4">
                  <div class="flex items-center gap-2">
                    <a
                      :href="link.url"
                      target="_blank"
                      class="flex items-center gap-2 text-sm text-cyan-600 hover:text-cyan-700 hover:underline truncate max-w-md"
                    >
                      <ExternalLink class="w-4 h-4 flex-shrink-0" />
                      <span class="truncate">{{ link.url }}</span>
                    </a>
                    <span 
                      :class="[
                        'px-2 py-0.5 rounded text-xs font-medium flex-shrink-0',
                        isValidUrl(link.url) 
                          ? 'bg-emerald-100 text-emerald-700' 
                          : 'bg-amber-100 text-amber-700'
                      ]"
                    >
                      {{ isValidUrl(link.url) ? '绝对路径' : '相对路径' }}
                    </span>
                  </div>
                </td>
                <td class="px-4 py-3">
                  <div class="flex items-center justify-center gap-2">
                    <Button variant="ghost" size="sm" @click="openEditDrawer(link)" class="hover:bg-cyan-50 hover:text-cyan-600 transition-colors">
                      <Edit class="w-4 h-4 mr-1" />
                      编辑
                    </Button>
                    <Button variant="ghost" size="sm" @click="handleDelete(link.id)" class="hover:bg-red-50 hover:text-red-600 transition-colors">
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
  <Drawer :open="drawerOpen" :title="drawerMode === 'add' ? '新增链接' : '编辑链接'" position="right" width="480px" @close="closeDrawer">
    <div class="p-6 space-y-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          <div class="flex items-center gap-2">
            <Type class="w-4 h-4 text-gray-500" />
            标题
            <span class="text-red-500 ml-1">*</span>
          </div>
        </label>
        <Input v-model="formData.title" placeholder="请输入链接标题" class="h-11" />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          <div class="flex items-center gap-2">
            <Link class="w-4 h-4 text-gray-500" />
            链接地址
            <span class="text-red-500 ml-1">*</span>
          </div>
        </label>
        <Input v-model="formData.url" placeholder="请输入链接地址（支持相对路径或绝对路径）" class="h-11" />
        <p class="text-xs text-gray-500 mt-2">
          支持两种格式：
          <br />• 绝对路径：如 https://www.example.com
          <br />• 相对路径：如 /docs/about
        </p>
      </div>

      <div v-if="formData.url" class="p-4 bg-gray-50 rounded-lg border border-gray-200">
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-600">链接类型：</span>
          <span 
            :class="[
              'px-3 py-1 rounded-lg text-sm font-medium',
              isValidUrl(formData.url) 
                ? 'bg-emerald-100 text-emerald-700' 
                : 'bg-amber-100 text-amber-700'
            ]"
          >
            {{ isValidUrl(formData.url) ? '✓ 绝对路径' : '✓ 相对路径' }}
          </span>
        </div>
      </div>

      <div class="pt-6 border-t border-gray-100">
        <Button @click="handleSave" class="w-full h-12 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 shadow-lg shadow-cyan-200">
          {{ drawerMode === 'add' ? '创建链接' : '保存修改' }}
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
