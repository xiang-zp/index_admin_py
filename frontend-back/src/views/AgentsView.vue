<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Drawer from '@/components/ui/Drawer.vue'
import type { Agent, AgentCreateRequest, AgentUpdateRequest } from '@/services/agents'
import { agentsApi } from '@/services/agents'
import {
  Plus,
  Edit,
  Trash2,
  X,
  Check,
  Bot,
  Settings
} from 'lucide-vue-next'

const agents = ref<Agent[]>([])
const loading = ref(false)
const drawerOpen = ref(false)
const drawerMode = ref<'add' | 'edit'>('add')
const showJsonModal = ref(false)
const currentJsonAgent = ref<Agent | null>(null)

const jsonContent = ref('')

const formData = ref({
  id: '',
  name: '',
  api: '',
  source: '内置',
  bot_id: ''
})

const sourceOptions = [
  { value: '内置', label: '内置' },
  { value: '第三方', label: '第三方' }
]

const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0
})

const resetForm = () => {
  formData.value = { id: '', name: '', api: '', source: '内置', bot_id: '' }
}

const openAddDrawer = () => {
  resetForm()
  drawerMode.value = 'add'
  drawerOpen.value = true
}

const openEditDrawer = (agent: Agent) => {
  formData.value = {
    id: agent.id,
    name: agent.name,
    api: agent.api,
    source: agent.source,
    bot_id: agent.bot_id || ''
  }
  drawerMode.value = 'edit'
  drawerOpen.value = true
}

const closeDrawer = () => {
  drawerOpen.value = false
  resetForm()
}

const handleSave = async () => {
  if (!formData.value.name || !formData.value.api) {
    alert('请输入名称和调用接口')
    return
  }

  try {
    if (drawerMode.value === 'add') {
      const createData: AgentCreateRequest = {
        name: formData.value.name,
        api: formData.value.api,
        source: formData.value.source,
        bot_id: formData.value.bot_id,
        is_visible: true
      }
      const response = await agentsApi.create(createData)
      if (response.code === 200 || response.code === 0) {
        await fetchAgents()
        closeDrawer()
      } else {
        alert(`创建失败: ${response.message}`)
      }
    } else {
      // 查找原始智能体以获取当前状态
      const originalAgent = agents.value.find(a => a.id === formData.value.id)
      const updateData: AgentUpdateRequest = {
        id: formData.value.id,
        name: formData.value.name,
        api: formData.value.api,
        source: formData.value.source,
        bot_id: formData.value.bot_id,
        is_visible: originalAgent ? originalAgent.is_visible : true
      }
      const response = await agentsApi.update(updateData)
      if (response.code === 200 || response.code === 0) {
        await fetchAgents()
        closeDrawer()
      } else {
        alert(`更新失败: ${response.message}`)
      }
    }
  } catch (error) {
    console.error('保存智能体异常:', error)
    alert('操作失败，请重试')
  }
}

const handleDelete = async (id: string) => {
  if (!confirm('确定要删除这个智能体吗？')) return
  
  try {
    const response = await agentsApi.delete(id)
    if (response.code === 200 || response.code === 0) {
      await fetchAgents()
    } else {
      alert(`删除失败: ${response.message}`)
    }
  } catch (error) {
    console.error('删除智能体异常:', error)
    alert('删除失败，请重试')
  }
}

const handleJsonEditor = (agent: Agent) => {
  currentJsonAgent.value = agent
  jsonContent.value = JSON.stringify({
    api: agent.api,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    timeout: 30000
  }, null, 2)
  showJsonModal.value = true
}

const closeJsonModal = () => {
  showJsonModal.value = false
  currentJsonAgent.value = null
}

const fetchAgents = async () => {
  try {
    loading.value = true
    const response = await agentsApi.getList()
    if (response.code === 200 || response.code === 0) {
      agents.value = response.data
      pagination.value.total = response.data.length
    } else {
      console.error('获取智能体列表失败:', response.message)
    }
  } catch (error) {
    console.error('获取智能体列表异常:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchAgents()
})
</script>

<template>
  <div class="h-screen overflow-hidden bg-gradient-to-br from-slate-50 via-gray-50 to-slate-100">
    <div class="max-w-7xl mx-auto px-8 py-6 h-full flex flex-col">
      <!-- Header -->
      <div class="mb-4 flex-shrink-0">
        <div class="flex items-center gap-4 mb-2">
          <div class="p-3 bg-gradient-to-br from-[#0891B2] to-[#22D3EE] rounded-2xl shadow-lg shadow-cyan-500/20">
            <Bot class="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-[#164E63] tracking-tight">
              智能体管理
            </h1>
            <p class="text-gray-500 mt-1 font-medium">配置和管理系统中的AI智能体</p>
          </div>
        </div>
      </div>

      <!-- Action Button -->
      <div class="flex justify-end mb-3 flex-shrink-0">
        <Button @click="openAddDrawer" class="h-10 px-5 bg-[#0891B2] hover:bg-[#0E7490] text-white shadow-lg shadow-cyan-500/20 rounded-xl transition-all duration-300 hover:-translate-y-0.5">
          <Plus class="w-4 h-4 mr-2" />
          新增智能体
        </Button>
      </div>

      <!-- Table -->
      <Card class="border-0 shadow-xl shadow-gray-200/50 bg-white/90 backdrop-blur-sm overflow-hidden rounded-2xl flex-1 flex flex-col min-h-0">
        <div class="overflow-auto flex-1">
          <table class="w-full">
            <thead class="sticky top-0 z-10">
              <tr class="bg-gradient-to-r from-slate-100 via-gray-100 to-slate-100 border-b-2 border-gray-200">
                <th class="w-24 px-6 py-5 text-left text-sm font-bold text-gray-700 tracking-wide">ID</th>
                <th class="w-48 px-6 py-5 text-left text-sm font-bold text-gray-700 tracking-wide">名称</th>
                <th class="px-6 py-5 text-left text-sm font-bold text-gray-700 tracking-wide">API 接口</th>
                <th class="w-28 px-6 py-5 text-left text-sm font-bold text-gray-700 tracking-wide">来源</th>
                <th class="w-32 px-6 py-5 text-center text-sm font-bold text-gray-700 tracking-wide">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-if="agents.length === 0" class="hover:bg-transparent">
                <td colspan="5" class="py-16 text-center">
                  <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center shadow-inner">
                    <Bot class="w-10 h-10 text-gray-400" />
                  </div>
                  <p class="text-gray-500 font-medium">暂无智能体数据</p>
                  <p class="text-gray-400 text-sm mt-1">点击上方"新增智能体"按钮添加数据</p>
                </td>
              </tr>
              <tr v-for="agent in agents" :key="agent.id" class="group hover:bg-gradient-to-r hover:from-indigo-50/50 hover:via-blue-50/30 hover:to-cyan-50/20 transition-all duration-300">
                <td class="px-6 py-4">
                  <span class="font-mono text-sm text-gray-500">{{ agent.id }}</span>
                </td>
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full bg-cyan-50 flex items-center justify-center text-cyan-600 font-bold text-xs">
                      {{ agent.name.charAt(0) }}
                    </div>
                    <span class="font-semibold text-gray-700">{{ agent.name }}</span>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <Button
                    variant="link"
                    size="sm"
                    class="text-[#0891B2] hover:text-[#0E7490] p-0 h-auto font-mono text-sm flex items-center gap-1 group/link"
                    @click="handleJsonEditor(agent)"
                  >
                    <span class="truncate max-w-[200px]">{{ agent.api }}</span>
                    <Settings class="w-3 h-3 opacity-0 group-hover/link:opacity-100 transition-opacity" />
                  </Button>
                </td>
                <td class="px-6 py-4">
                  <span 
                    :class="[
                      'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border',
                      agent.source === '内置' 
                        ? 'bg-emerald-100 text-emerald-700 border-emerald-200' 
                        : 'bg-amber-100 text-amber-700 border-amber-200'
                    ]"
                  >
                    {{ agent.source }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <div class="flex items-center justify-center gap-2">
                    <Button variant="ghost" size="sm" @click="openEditDrawer(agent)" class="bg-white border border-gray-200 shadow-sm hover:bg-gradient-to-r hover:from-indigo-50 hover:to-blue-50 hover:border-indigo-200 hover:shadow-md transition-all duration-200">
                      <Edit class="w-4 h-4 mr-1.5 text-indigo-500" />
                      <span class="text-gray-600">编辑</span>
                    </Button>
                    <Button variant="ghost" size="sm" @click="handleDelete(agent.id)" class="bg-white border border-gray-200 shadow-sm hover:bg-gradient-to-r hover:from-red-50 hover:to-orange-50 hover:border-red-200 hover:shadow-md transition-all duration-200">
                      <Trash2 class="w-4 h-4 mr-1.5 text-red-500" />
                      <span class="text-gray-600">删除</span>
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

    <!-- Drawer -->
    <Drawer :open="drawerOpen" :title="drawerMode === 'add' ? '新增智能体' : '编辑智能体'" position="right" width="480px" @close="closeDrawer">
      <div class="p-8 space-y-8">
        <div class="space-y-6">
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-[#164E63]">
              名称 <span class="text-red-500">*</span>
            </label>
            <Input v-model="formData.name" placeholder="给智能体起个名字" class="h-11 rounded-xl bg-gray-50 border-gray-200 focus:bg-white focus:border-[#22D3EE] focus:ring-4 focus:ring-[#22D3EE]/10 transition-all" />
          </div>

          <div class="space-y-2">
            <label class="block text-sm font-semibold text-[#164E63]">
              调用接口 <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <Input v-model="formData.api" placeholder="https://api.example.com/v1/chat" class="h-11 pl-10 rounded-xl bg-gray-50 border-gray-200 focus:bg-white focus:border-[#22D3EE] focus:ring-4 focus:ring-[#22D3EE]/10 transition-all font-mono text-sm" />
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                <Settings class="w-4 h-4" />
              </div>
            </div>
            <p class="text-xs text-gray-400 mt-1">智能体服务的完整 API 调用地址</p>
          </div>

          <div class="space-y-2">
            <label class="block text-sm font-semibold text-[#164E63]">
              来源 <span class="text-red-500">*</span>
            </label>
            <div class="grid grid-cols-2 gap-3">
              <div 
                v-for="source in sourceOptions" 
                :key="source.value"
                @click="formData.source = source.value"
                :class="[
                  'cursor-pointer px-4 py-3 rounded-xl border transition-all duration-200 flex items-center justify-center gap-2',
                  formData.source === source.value
                    ? 'bg-[#0891B2]/5 border-[#0891B2] text-[#0891B2] font-semibold'
                    : 'bg-white border-gray-200 text-gray-600 hover:border-gray-300'
                ]"
              >
                <div class="w-2 h-2 rounded-full" :class="source.value === '内置' ? 'bg-emerald-400' : 'bg-amber-400'"></div>
                {{ source.label }}
              </div>
            </div>
          </div>
        </div>

        <div class="pt-6 border-t border-gray-100">
          <Button @click="handleSave" class="w-full h-12 bg-[#0891B2] hover:bg-[#0E7490] text-white rounded-xl shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/30 transition-all duration-300 font-medium">
            {{ drawerMode === 'add' ? '创建智能体' : '保存修改' }}
          </Button>
        </div>
      </div>
    </Drawer>

    <!-- JSON Editor Modal -->
    <div v-if="showJsonModal" class="fixed inset-0 z-50 flex items-center justify-center bg-[#164E63]/20 backdrop-blur-sm" @click="closeJsonModal">
      <Card class="w-full max-w-2xl mx-4 border-0 shadow-2xl bg-white/95 backdrop-blur-xl animate-scale-in rounded-3xl" @click.stop>
        <CardContent class="p-0">
          <div class="flex items-center justify-between p-6 border-b border-gray-100">
            <div class="flex items-center gap-4">
              <div class="p-2.5 bg-cyan-50 rounded-xl">
                <Settings class="w-6 h-6 text-[#0891B2]" />
              </div>
              <div>
                <h3 class="text-lg font-bold text-[#164E63]">接口配置详情</h3>
                <p class="text-sm text-gray-500 font-medium">{{ currentJsonAgent?.name }}</p>
              </div>
            </div>
            <Button variant="ghost" size="icon" @click="closeJsonModal" class="hover:bg-gray-100 rounded-xl">
              <X class="w-5 h-5 text-gray-400" />
            </Button>
          </div>
          
          <div class="p-6 space-y-6">
            <div class="space-y-2">
              <label class="block text-sm font-semibold text-[#164E63]">API 端点</label>
              <div class="flex items-center gap-2 p-3 bg-gray-50 rounded-xl border border-gray-100 font-mono text-sm text-gray-600">
                <span class="px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-700 text-xs font-bold">POST</span>
                {{ currentJsonAgent?.api }}
              </div>
            </div>

            <div class="space-y-2">
              <label class="block text-sm font-semibold text-[#164E63]">JSON 配置</label>
              <div class="relative group">
                <textarea
                  v-model="jsonContent"
                  class="w-full h-80 p-5 rounded-xl border border-gray-200 font-mono text-sm leading-relaxed bg-[#1e293b] text-cyan-300 focus:outline-none focus:ring-4 focus:ring-[#22D3EE]/20 resize-none selection:bg-cyan-500/30 custom-scrollbar"
                  placeholder="{ ... }"
                />
                <div class="absolute top-4 right-4 px-2 py-1 bg-white/10 rounded text-xs text-white/50 font-mono">JSON</div>
              </div>
            </div>

            <div class="flex justify-end gap-3 pt-2">
              <Button variant="outline" @click="closeJsonModal" class="h-11 px-6 rounded-xl border-gray-200 hover:bg-gray-50 text-gray-600">取消</Button>
              <Button @click="closeJsonModal" class="h-11 px-6 bg-[#0891B2] hover:bg-[#0E7490] text-white rounded-xl shadow-lg shadow-cyan-500/20">
                <Check class="w-4 h-4 mr-2" />
                保存配置
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<style scoped>
@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.animate-scale-in {
  animation: scale-in 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Custom Scrollbar for Textarea */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}
.custom-scrollbar:hover::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
}

tbody tr {
  transition: all 0.2s ease;
}

tbody tr:hover {
  transform: translateX(4px);
}
</style>
