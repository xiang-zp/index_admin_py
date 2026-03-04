<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { toast } from '@/lib/toast'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import { Eye, EyeOff } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const showPassword = ref(false)

const handleLogin = async () => {
  if (!username.value || !password.value) {
    toast.error('请输入用户名或密码！')
    return
  }
  
  loading.value = true
  
  const result = await authStore.login(username.value, password.value)
  
  loading.value = false
  
  if (result.success) {
    toast.success(`欢迎 ${username.value} 登录后台管理系统！`, 5000)
    router.push({ name: 'dashboard' })
  } else {
    toast.error('用户名或密码错误，请重新输入！')
  }
}


</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-[#ECFEFF] relative overflow-hidden">
    <!-- Background Decor -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
      <div class="absolute -top-20 -left-20 w-96 h-96 bg-[#22D3EE] rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
      <div class="absolute top-0 -right-20 w-96 h-96 bg-[#0891B2] rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
      <div class="absolute -bottom-32 left-20 w-96 h-96 bg-[#22C55E] rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
      
      <!-- Floating Geometric Shapes -->
      <div class="absolute top-20 left-[10%] opacity-30 animate-float-slow">
        <svg class="w-16 h-16 text-cyan-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <polygon points="12,2 22,8.5 22,15.5 12,22 2,15.5 2,8.5" />
        </svg>
      </div>
      <div class="absolute top-[30%] right-[15%] opacity-25 animate-float-medium">
        <svg class="w-12 h-12 text-teal-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="10" />
        </svg>
      </div>
      <div class="absolute bottom-[25%] left-[20%] opacity-20 animate-float-fast">
        <svg class="w-10 h-10 text-cyan-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="3" y="3" width="18" height="18" rx="2" />
        </svg>
      </div>
      <div class="absolute top-[15%] right-[25%] opacity-15 animate-float-slow">
        <svg class="w-20 h-20 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
          <polygon points="12,2 22,8.5 22,15.5 12,22 2,15.5 2,8.5" />
        </svg>
      </div>
      <div class="absolute bottom-[40%] right-[10%] opacity-20 animate-float-medium">
        <svg class="w-14 h-14 text-teal-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
        </svg>
      </div>
    </div>

    <Card class="w-full max-w-md shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-white/50 bg-white/70 backdrop-blur-xl rounded-3xl relative z-10">
      <CardContent class="pt-10 pb-8 px-10">
        <div class="text-center mb-10">
          <div class="w-16 h-16 mx-auto mb-6 bg-gradient-to-br from-[#0891B2] to-[#22D3EE] rounded-2xl flex items-center justify-center shadow-lg shadow-cyan-500/30 transform hover:scale-105 transition-transform duration-300">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h1 class="text-2xl font-bold text-[#164E63] tracking-tight">首页-后台管理</h1>
          <p class="text-gray-500 mt-3 text-sm font-medium">欢迎回来，请登录您的管理员账号</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-[#164E63] ml-1">用户名</label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none transition-colors duration-300 group-focus-within:text-[#0891B2]">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <Input
                v-model="username"
                type="text"
                placeholder="请输入用户名"
                class="h-12 pl-12 bg-white/50 border-gray-200 focus:bg-white focus:border-[#22D3EE] focus:ring-4 focus:ring-[#22D3EE]/10 rounded-xl transition-all duration-300 placeholder:text-gray-400"
                :disabled="loading"
              />
            </div>
          </div>
          
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-[#164E63] ml-1">密码</label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none transition-colors duration-300 group-focus-within:text-[#0891B2]">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <Input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="请输入密码"
                class="h-12 pl-12 pr-12 bg-white/50 border-gray-200 focus:bg-white focus:border-[#22D3EE] focus:ring-4 focus:ring-[#22D3EE]/10 rounded-xl transition-all duration-300 placeholder:text-gray-400"
                :disabled="loading"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-[#0891B2] transition-colors cursor-pointer"
              >
                <Eye v-if="showPassword" class="w-5 h-5" />
                <EyeOff v-else class="w-5 h-5" />
              </button>
            </div>
          </div>
          
          <div class="space-y-4 pt-2">
            <Button
              type="submit"
              class="w-full h-12 bg-gradient-to-r from-[#0891B2] to-[#22D3EE] hover:from-[#0E7490] hover:to-[#0891B2] text-white font-semibold rounded-xl shadow-lg shadow-cyan-500/25 hover:shadow-cyan-500/40 hover:-translate-y-0.5 transition-all duration-300"
              :disabled="loading"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? '登录中...' : '立即登录' }}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  </div>
</template>

<style scoped>
@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}
.animate-blob {
  animation: blob 7s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
.animation-delay-4000 {
  animation-delay: 4s;
}

@keyframes float-slow {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}
@keyframes float-medium {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-15px) rotate(-5deg); }
}
@keyframes float-fast {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(3deg); }
}
.animate-float-slow {
  animation: float-slow 8s ease-in-out infinite;
}
.animate-float-medium {
  animation: float-medium 6s ease-in-out infinite;
}
.animate-float-fast {
  animation: float-fast 5s ease-in-out infinite;
}
</style>
