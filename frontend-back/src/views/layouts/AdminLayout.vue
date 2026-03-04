<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterView, RouterLink, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  LayoutDashboard,
  Bot,
  Wrench,
  FileText,
  Star,
  Key,
  Users,
  Footprints,
  LogOut,
  Image,
  AlertTriangle
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const showLogoutConfirm = ref(false)

const menuItems = [
  { path: '/', name: 'dashboard', label: '仪表盘', icon: LayoutDashboard },
  { path: '/carousel', name: 'carousel', label: '轮播文案', icon: Image },
  { path: '/agents', name: 'agents', label: '智能体管理', icon: Bot },
  { path: '/tools', name: 'tools', label: '开源项目', icon: Wrench },
  { path: '/documents', name: 'documents', label: '文档资料', icon: FileText },
  { path: '/footer', name: 'footer', label: '底部配置', icon: Footprints },
  { path: '/reviews', name: 'reviews', label: '用户评价', icon: Star },
  { path: '/auth-codes', name: 'auth-codes', label: '授权码管理', icon: Key },
  { path: '/users', name: 'users', label: '账号管理', icon: Users },
]

const handleLogoutClick = () => {
  showLogoutConfirm.value = true
}

const confirmLogout = () => {
  showLogoutConfirm.value = false
  authStore.logout()
  router.push({ name: 'login' })
}

const cancelLogout = () => {
  showLogoutConfirm.value = false
}

onMounted(() => {
  authStore.initAuth()
})
</script>

<template>
  <div class="min-h-screen bg-[#ECFEFF] flex font-sans">
    <!-- Fixed Sidebar -->
    <aside class="fixed inset-y-0 left-0 z-40 w-64 bg-white/70 backdrop-blur-xl border-r border-white/20 shadow-[4px_0_24px_rgba(0,0,0,0.02)]">
      <div class="flex flex-col h-full">
        <!-- Logo -->
        <div class="flex items-center px-8 h-20 border-b border-gray-100/50">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-[#0891B2] to-[#22D3EE] flex items-center justify-center shadow-lg shadow-cyan-500/20 mr-3">
            <LayoutDashboard class="w-5 h-5 text-white" />
          </div>
          <h1 class="text-lg font-bold text-[#164E63] tracking-tight">首页-后台管理</h1>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 px-4 py-6 space-y-1 overflow-y-auto custom-scrollbar">
          <RouterLink
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            :class="[
              'flex items-center gap-3 px-4 py-3.5 rounded-xl transition-all duration-300 group relative overflow-hidden',
              route.name === item.name
                ? 'bg-gradient-to-r from-[#0891B2]/10 to-[#22D3EE]/10 text-[#0891B2] font-semibold'
                : 'text-gray-500 hover:text-[#0891B2] hover:bg-white/50'
            ]"
          >
            <component 
              :is="item.icon" 
              :class="[
                'w-5 h-5 transition-transform duration-300',
                route.name === item.name ? 'scale-110' : 'group-hover:scale-110'
              ]" 
            />
            <span class="relative z-10">{{ item.label }}</span>
            <div v-if="route.name === item.name" class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-[#0891B2] rounded-r-full"></div>
          </RouterLink>
        </nav>

        <!-- Logout -->
        <div class="p-4 border-t border-gray-100/50 bg-white/30 backdrop-blur-md">
          <button
            @click="handleLogoutClick"
            class="flex items-center gap-3 w-full px-4 py-3.5 rounded-xl text-gray-500 hover:text-red-500 hover:bg-red-50/50 transition-all duration-300 group"
          >
            <LogOut class="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
            <span class="font-medium">退出登录</span>
          </button>
        </div>
      </div>
    </aside>

    <!-- Logout Confirm Modal -->
    <div v-if="showLogoutConfirm" class="fixed inset-0 z-50 flex items-center justify-center bg-[#164E63]/20 backdrop-blur-sm transition-all duration-300">
      <div class="bg-white/90 backdrop-blur-xl rounded-3xl shadow-2xl p-8 w-full max-w-sm mx-4 border border-white/50 transform transition-all duration-300 scale-100">
        <div class="flex items-center justify-center w-16 h-16 mx-auto bg-red-50 rounded-2xl mb-6 shadow-inner">
          <AlertTriangle class="w-8 h-8 text-red-500" />
        </div>
        <h3 class="text-xl font-bold text-[#164E63] text-center mb-2">确认退出</h3>
        <p class="text-gray-500 text-center mb-8 leading-relaxed">您确定要退出当前账号吗？<br>未保存的数据可能会丢失。</p>
        <div class="flex gap-4">
          <button
            @click="cancelLogout"
            class="flex-1 px-4 py-3 border border-gray-200 rounded-xl text-gray-600 font-medium hover:bg-gray-50 hover:border-gray-300 transition-all duration-200"
          >
            取消
          </button>
          <button
            @click="confirmLogout"
            class="flex-1 px-4 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl font-medium hover:shadow-lg hover:shadow-red-500/30 hover:-translate-y-0.5 transition-all duration-200"
          >
            确认退出
          </button>
        </div>
      </div>
    </div>

    <!-- Main content with fixed sidebar -->
    <main class="flex-1 ml-64 min-h-screen transition-all duration-300">
      <div class="p-10 max-w-7xl mx-auto">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(8, 145, 178, 0.1);
  border-radius: 10px;
}
.custom-scrollbar:hover::-webkit-scrollbar-thumb {
  background: rgba(8, 145, 178, 0.2);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
