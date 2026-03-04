<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import Button from '@/components/ui/Button.vue'
import { dashboardApi } from '@/services/dashboard'
import { useAuthStore } from '@/stores/auth'
import type { DashboardStats, Activity } from '@/services/dashboard'
import {
  Bot,
  Wrench,
  FileText,
  Star,
  Users,
  Activity as ActivityIcon,
  Trash2,
  BarChart3,
  PieChart as PieChartIcon,
  TrendingUp
} from 'lucide-vue-next'

// ECharts imports
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart as EChartsPieChart, BarChart, LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import * as echarts from 'echarts/core'

use([
  CanvasRenderer,
  EChartsPieChart,
  BarChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

const stats = ref<DashboardStats>({
  agents: 0,
  tools: 0,
  documents: 0,
  reviews: 0,
  users: 0
})
const loading = ref(false)
const deleteAllLoading = ref(false)

const authStore = useAuthStore()
const currentUsername = computed(() => authStore.user?.username || '管理员')

const chartType = ref<'pie' | 'bar' | 'line'>('pie')
const showChartDropdown = ref(false)

const chartOptions = [
  { value: 'pie', label: '饼图', icon: 'PieChartIcon' },
  { value: 'bar', label: '柱状图', icon: 'BarChart3' },
  { value: 'line', label: '折线图', icon: 'TrendingUp' }
]

const setChartType = (type: 'pie' | 'bar' | 'line') => {
  chartType.value = type
  showChartDropdown.value = false
}

const total = computed(() => {
  return stats.value.agents + stats.value.tools + stats.value.documents + stats.value.users
})

// ECharts Option
const chartOption = computed(() => {
  if (chartType.value === 'bar') {
    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderColor: '#e2e8f0',
        borderWidth: 1,
        textStyle: {
          color: '#1e293b'
        },
        padding: [8, 12],
        formatter: (params: any) => {
          const data = params[0]
          return `${data.name}: ${data.value}`
        },
        extraCssText: 'box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); border-radius: 8px;'
      },
      grid: {
        left: '12%',
        right: '4%',
        bottom: '3%',
        top: '15%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: ['智能体', '开源项目', '文档资料', '管理员'],
        axisLine: {
          lineStyle: {
            color: '#e2e8f0'
          }
        },
        axisTick: {
          show: false
        },
        axisLabel: {
          color: '#64748b',
          fontSize: 12,
          fontWeight: 600,
          margin: 12
        }
      },
      yAxis: {
        type: 'value',
        axisLine: {
          show: false
        },
        axisLabel: {
          color: '#64748b',
          fontSize: 12
        },
        splitLine: {
          lineStyle: {
            color: '#f1f5f9'
          }
        }
      },
      series: [
        {
          name: '数量',
          type: 'bar',
          barWidth: '40%',
          data: [
            {
              value: stats.value.agents,
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#a855f7' },
                  { offset: 1, color: '#ec4899' }
                ]),
                borderRadius: [8, 8, 0, 0]
              }
            },
            {
              value: stats.value.tools,
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#3b82f6' },
                  { offset: 1, color: '#06b6d4' }
                ]),
                borderRadius: [8, 8, 0, 0]
              }
            },
            {
              value: stats.value.documents,
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#22c55e' },
                  { offset: 1, color: '#10b981' }
                ]),
                borderRadius: [8, 8, 0, 0]
              }
            },
            {
              value: stats.value.users,
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#ef4444' },
                  { offset: 1, color: '#f43f5e' }
                ]),
                borderRadius: [8, 8, 0, 0]
              }
            }
          ],
          label: {
            show: true,
            position: 'top',
            formatter: (params: any) => {
              const total = stats.value.agents + stats.value.tools + stats.value.documents + stats.value.users
              if (total === 0) return '0%'
              const percent = Math.round((params.value / total) * 100)
              return percent + '%'
            },
            color: '#64748b',
            fontSize: 12,
            fontWeight: 600
          },
          animationDelay: function (idx: number) {
            return idx * 100
          }
        }
      ],
      animationEasing: 'elasticOut',
      animationDelayUpdate: function (idx: number) {
        return idx * 5
      }
    }
  }
  
  if (chartType.value === 'line') {
    const dataValues = [
      stats.value.agents,
      stats.value.tools,
      stats.value.documents,
      stats.value.users
    ]
    return {
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderColor: '#e2e8f0',
        borderWidth: 1,
        textStyle: {
          color: '#1e293b'
        },
        padding: [8, 12],
        formatter: (params: any) => {
          const data = params[0]
          return `${data.name}: ${data.value}`
        },
        extraCssText: 'box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); border-radius: 8px;'
      },
      grid: {
        left: '8%',
        right: '4%',
        bottom: '3%',
        top: '10%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['智能体', '开源项目', '文档资料', '管理员'],
        axisLine: {
          lineStyle: {
            color: '#e2e8f0'
          }
        },
        axisTick: {
          show: false
        },
        axisLabel: {
          color: '#64748b',
          fontSize: 12,
          fontWeight: 600,
          margin: 12
        }
      },
      yAxis: {
        type: 'value',
        axisLine: {
          show: false
        },
        axisLabel: {
          color: '#64748b',
          fontSize: 12
        },
        splitLine: {
          lineStyle: {
            color: '#f1f5f9'
          }
        }
      },
      series: [
        {
          name: '数量',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 8,
          lineStyle: {
            width: 3,
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#0891B2' },
              { offset: 1, color: '#22D3EE' }
            ])
          },
          itemStyle: {
            color: '#0891B2',
            borderColor: '#fff',
            borderWidth: 2,
            shadowColor: 'rgba(8, 145, 178, 0.3)',
            shadowBlur: 8
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(8, 145, 178, 0.3)' },
              { offset: 1, color: 'rgba(8, 145, 178, 0.05)' }
            ])
          },
          data: dataValues,
          label: {
            show: true,
            position: 'top',
            formatter: (params: any) => {
              const total = stats.value.agents + stats.value.tools + stats.value.documents + stats.value.users
              if (total === 0) return '0%'
              const percent = Math.round((params.value / total) * 100)
              return percent + '%'
            },
            color: '#64748b',
            fontSize: 12,
            fontWeight: 600
          },
          animationDelay: function (idx: number) {
            return idx * 100
          }
        }
      ],
      animationEasing: 'cubicOut'
    }
  }
  
  const data = [
    { 
      value: stats.value.agents, 
      name: '智能体',
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 1, 1, [
          { offset: 0, color: '#a855f7' },
          { offset: 1, color: '#ec4899' }
        ])
      }
    },
    { 
      value: stats.value.tools, 
      name: '开源项目',
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 1, 1, [
          { offset: 0, color: '#3b82f6' },
          { offset: 1, color: '#06b6d4' }
        ])
      }
    },
    { 
      value: stats.value.documents, 
      name: '文档资料',
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 1, 1, [
          { offset: 0, color: '#22c55e' },
          { offset: 1, color: '#10b981' }
        ])
      }
    },
    { 
      value: stats.value.users, 
      name: '管理员',
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 1, 1, [
          { offset: 0, color: '#ef4444' },
          { offset: 1, color: '#f43f5e' }
        ])
      }
    }
  ]

  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: {
        color: '#1e293b'
      },
      padding: [8, 12],
      extraCssText: 'box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); border-radius: 8px;'
    },
    series: [
      {
        name: '数据分布',
        type: 'pie',
        radius: '75%', // 纯实心饼图
        center: ['50%', '50%'],
        // 移除 roseType 以回归标准饼图，但通过样式增强质感
        padAngle: 5, // 扇区间隔，增加现代感
        itemStyle: {
          borderRadius: 10, // 大圆角
          borderColor: '#fff',
          borderWidth: 0,
          shadowBlur: 15,
          shadowOffsetX: 0,
          shadowOffsetY: 5,
          shadowColor: 'rgba(0, 0, 0, 0.2)'
        },
        label: {
          show: true,
          position: 'outside',
          formatter: '{b}\n{d}%',
          color: '#334155', // slate-700
          fontSize: 14,
          fontWeight: 600,
          lineHeight: 20
        },
        labelLine: {
          show: true,
          length: 15,
          length2: 10,
          smooth: true,
          lineStyle: {
            width: 2,
            type: 'solid'
          }
        },
        emphasis: {
          scale: true,
          scaleSize: 10,
          itemStyle: {
            shadowBlur: 25,
            shadowColor: 'rgba(0, 0, 0, 0.4)'
          },
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: data,
        animationType: 'scale',
        animationEasing: 'elasticOut',
        animationDelay: function (_idx: number) {
          return Math.random() * 200;
        }
      }
    ]
  }
})

// Keep existing helper functions for list view
const chartDataList = computed(() => [
  { label: '智能体', value: stats.value.agents, color: ['#a855f7', '#ec4899'], percent: 0 },
  { label: '开源项目', value: stats.value.tools, color: ['#3b82f6', '#06b6d4'], percent: 0 },
  { label: '文档资料', value: stats.value.documents, color: ['#22c55e', '#10b981'], percent: 0 },
  { label: '管理员', value: stats.value.users, color: ['#ef4444', '#f43f5e'], percent: 0 }
].map(item => ({
  ...item,
  percent: total.value > 0 ? Math.round((item.value / total.value) * 100) : 0
})))

const activeIndex = ref<number | null>(null)

const getColorStyle = (colors: string[]) => {
  return `linear-gradient(135deg, ${colors[0]}, ${colors[1]})`
}

const recentActivities = ref<Activity[]>([])

const currentPage = ref(1)
const pageSize = 5
const totalActivities = computed(() => recentActivities.value.length)
const paginatedActivities = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return recentActivities.value.slice(start, end)
})
const totalPages = computed(() => Math.ceil(totalActivities.value / pageSize))

const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const getActivityIcon = (type: string) => {
  const icons: Record<string, any> = {
    agent: Bot,
    tool: Wrench,
    document: FileText,
    review: Star,
    user: Users,
    auth: Star
  }
  return icons[type] || Star
}

const getActivityColor = (type: string) => {
  const colors: Record<string, string> = {
    agent: 'bg-purple-100 text-purple-600',
    tool: 'bg-blue-100 text-blue-600',
    document: 'bg-green-100 text-green-600',
    review: 'bg-yellow-100 text-yellow-600',
    user: 'bg-red-100 text-red-600',
    auth: 'bg-indigo-100 text-indigo-600'
  }
  return colors[type] || 'bg-gray-100 text-gray-600'
}

const loadDashboardData = async () => {
  loading.value = true
  try {
    const [statsResponse, activitiesResponse] = await Promise.all([
      dashboardApi.getStats(),
      dashboardApi.getActivities()
    ])
    
    if (statsResponse.code === 200 || statsResponse.code === 0) {
      stats.value = statsResponse.data
    }
    
    if (activitiesResponse.code === 200 || activitiesResponse.code === 0) {
      recentActivities.value = activitiesResponse.data
      currentPage.value = 1
    }
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  } finally {
    loading.value = false
  }
}

const handleDeleteActivity = async (activity: Activity) => {
  if (!activity.db_id) {
    console.error('活动记录缺少数据库ID')
    return
  }
  
  // 确认删除
  if (!confirm(`确定要删除这条活动记录吗？\n"${activity.message}"`)) {
    return
  }
  
  try {
    const response = await dashboardApi.deleteActivity(activity.db_id)
    if (response.code === 200 || response.code === 0) {
      // 重新加载活动数据以确保数据一致性
      await loadDashboardData()
    } else {
      console.error('删除活动记录失败:', response.message)
      alert(`删除失败: ${response.message}`)
    }
  } catch (error) {
    console.error('删除活动记录错误:', error)
    alert('删除活动记录时发生错误')
  }
}

const handleDeleteAllActivities = async () => {
 //  确认删除 - 危险操作需要更明确的警告
  if (!confirm(`⚠️ 警告：确定要删除所有活动记录吗？\n\n此操作将永久删除所有活动记录，无法恢复！\n\n共 ${recentActivities.value.length} 条记录将被删除。`)) {
    return
  }
  
  deleteAllLoading.value = true
  try {
    const response = await dashboardApi.deleteAllActivities()
    if (response.code === 200 || response.code === 0) {
      const deletedCount = response.data?.deleted_count || 0
      alert(`✅ 成功删除所有活动记录 (${deletedCount} 条)`)
      // 重新加载活动数据
      await loadDashboardData()
    } else {
      console.error('删除所有活动记录失败:', response.message)
      alert(`删除失败: ${response.message}`)
    }
  } catch (error) {
    console.error('删除所有活动记录错误:', error)
    alert('删除所有活动记录时发生错误')
  } finally {
    deleteAllLoading.value = false
  }
}

onMounted(() => {
  loadDashboardData()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const handleClickOutside = (e: MouseEvent) => {
  const target = e.target as HTMLElement
  if (!target.closest('.chart-dropdown')) {
    showChartDropdown.value = false
  }
}
</script>

<template>
  <div class="min-h-screen">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-10">
        <div class="flex items-center gap-4 mb-2">
          <div class="p-3 bg-gradient-to-br from-[#0891B2] to-[#22D3EE] rounded-2xl shadow-lg shadow-cyan-500/20">
            <ActivityIcon class="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 class="text-3xl font-bold text-[#164E63] tracking-tight">
              仪表盘
            </h1>
            <p class="text-gray-500 mt-1 font-medium">
              欢迎使用首页后台管理系统 - <span class="text-[#0891B2] font-semibold">{{ currentUsername }}</span>
            </p>
          </div>
        </div>
      </div>

      <!-- Stats with Pie Chart -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Pie Chart -->
        <Card class="border-0 shadow-[0_4px_20px_rgba(0,0,0,0.02)] bg-white/60 backdrop-blur-xl rounded-2xl border-white/60">
          <CardContent class="pt-8 px-8">
            <div class="flex items-center justify-between mb-2">
              <div>
                <CardTitle class="text-[#164E63]">数据概览</CardTitle>
                <CardDescription>系统资源分布统计</CardDescription>
              </div>
              <div class="relative chart-dropdown">
                <button
                  @click="showChartDropdown = !showChartDropdown"
                  class="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-[#0891B2] to-[#22D3EE] hover:from-[#0E7490] hover:to-[#0891B2] text-white rounded-lg shadow-md shadow-cyan-500/20 hover:shadow-cyan-500/40 transition-all duration-300 hover:-translate-y-0.5"
                  title="切换图表样式"
                >
                  <PieChartIcon class="w-4 h-4" />
                  <span class="text-sm font-semibold">图表切换</span>
                  <svg class="w-4 h-4 transition-transform duration-200" :class="showChartDropdown ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <Transition name="dropdown">
                  <div
                    v-if="showChartDropdown"
                    class="absolute right-0 mt-2 w-36 bg-white rounded-xl shadow-xl border border-gray-100 py-1 z-50 overflow-hidden"
                  >
                    <button
                      v-for="option in chartOptions"
                      :key="option.value"
                      @click="setChartType(option.value as 'pie' | 'bar' | 'line')"
                      class="w-full flex items-center gap-3 px-4 py-2.5 text-left hover:bg-cyan-50 transition-colors"
                      :class="chartType === option.value ? 'text-[#0891B2] bg-cyan-50/50' : 'text-gray-600'"
                    >
                      <TrendingUp v-if="option.value === 'line'" class="w-4 h-4" />
                      <BarChart3 v-else-if="option.value === 'bar'" class="w-4 h-4" />
                      <PieChartIcon v-else class="w-4 h-4" />
                      <span class="text-sm font-medium">{{ option.label }}</span>
                      <svg v-if="chartType === option.value" class="w-4 h-4 ml-auto text-[#0891B2]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </button>
                  </div>
                </Transition>
              </div>
            </div>
            
            <div class="flex items-center justify-center mt-12 mb-8" style="overflow: visible;">
              <div class="relative w-full h-80">
                <!-- ECharts Chart -->
                <v-chart :key="chartType" class="w-full h-full" :option="chartOption" autoresize />
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Chart Legend -->
        <Card class="border-0 shadow-[0_4px_20px_rgba(0,0,0,0.02)] bg-white/60 backdrop-blur-xl rounded-2xl border-white/60 flex flex-col">
          <CardContent class="pt-8 px-8 flex-1 flex flex-col">
            <div class="flex items-center justify-between mb-6">
              <div>
                <CardTitle class="text-[#164E63]">数据分布</CardTitle>
                <CardDescription>各类数据占比详情</CardDescription>
              </div>
              <Button variant="ghost" size="icon" class="text-gray-400 hover:text-[#0891B2]">
                <Bot class="w-5 h-5" />
              </Button>
            </div>
            
            <div class="mt-4 space-y-5 flex-1 overflow-y-auto custom-scrollbar pr-2">
              <div
                v-for="(item, index) in chartDataList"
                :key="index"
                class="group cursor-pointer p-3 rounded-xl hover:bg-white/50 transition-all duration-300 border border-transparent hover:border-gray-100"
                @mouseenter="activeIndex = index"
                @mouseleave="activeIndex = null"
              >
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-3">
                    <div class="w-3 h-3 rounded-full shadow-sm" :style="{ background: getColorStyle(item.color) }"></div>
                    <span class="text-sm font-semibold text-gray-700 group-hover:text-[#0891B2] transition-colors">{{ item.label }}</span>
                  </div>
                  <div class="flex items-baseline gap-1">
                    <span class="text-lg font-bold text-gray-900">{{ item.value }}</span>
                    <span class="text-xs text-gray-400">条</span>
                  </div>
                </div>
                <div class="relative h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    class="absolute inset-y-0 left-0 rounded-full transition-all duration-500 shadow-[0_2px_4px_rgba(0,0,0,0.1)]"
                    :style="{ width: `${item.percent}%`, background: getColorStyle(item.color) }"
                  ></div>
                </div>
                <div class="flex justify-between mt-1.5">
                  <span class="text-xs font-medium text-gray-400">占比 {{ item.percent }}%</span>
                  <span v-if="activeIndex === index" class="text-xs font-bold text-[#0891B2] animate-fade-in">
                    {{ total > 0 ? Math.round((item.value / total) * 100) : 0 }}%
                  </span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Recent Activities -->
      <Card class="border-0 shadow-[0_4px_20px_rgba(0,0,0,0.02)] bg-white/60 backdrop-blur-xl rounded-2xl border-white/60">
        <CardContent class="pt-8 px-8 pb-8">
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-3">
              <div class="p-2 bg-violet-50 rounded-lg text-violet-600">
                <ActivityIcon class="w-5 h-5" />
              </div>
              <div>
                <CardTitle class="text-[#164E63]">最近活动</CardTitle>
                <CardDescription>系统最近操作记录</CardDescription>
              </div>
            </div>
            <button
              @click="handleDeleteAllActivities"
              :disabled="deleteAllLoading || totalActivities === 0"
              class="flex items-center gap-2 px-4 py-2 bg-red-50 text-red-600 hover:bg-red-100 border border-red-200 rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Trash2 class="w-4 h-4" />
              <span class="text-sm font-medium">
                {{ deleteAllLoading ? '删除中...' : '删除全部记录' }}
              </span>
            </button>
          </div>
          
          <div class="mt-4 space-y-1">
            <div
              v-for="activity in paginatedActivities"
              :key="activity.id"
              class="flex items-center gap-4 p-4 rounded-xl hover:bg-white/80 transition-all duration-300 group border border-transparent hover:border-gray-100 hover:shadow-sm"
            >
              <div :class="['p-2.5 rounded-xl transition-transform duration-300 group-hover:scale-105 shadow-sm', getActivityColor(activity.type)]">
                <component :is="getActivityIcon(activity.type)" class="w-5 h-5" />
              </div>
              <div class="flex-1">
                <p class="text-sm font-semibold text-gray-700 group-hover:text-[#0891B2] transition-colors">
                  <span class="text-[#0891B2]">{{ activity.username || '系统' }}</span> {{ activity.message }}
                </p>
                <div class="flex items-center gap-2 mt-1">
                  <span class="w-1.5 h-1.5 rounded-full bg-gray-300 group-hover:bg-[#22D3EE] transition-colors"></span>
                  <p class="text-xs text-gray-400">{{ activity.time }}</p>
                </div>
              </div>
              <div class="transition-all duration-300">
                <div 
                  class="p-2 rounded-full bg-gray-50 text-gray-400 hover:bg-red-500 hover:text-white transition-colors cursor-pointer"
                  @click="handleDeleteActivity(activity)"
                >
                  <Trash2 class="w-4 h-4" />
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="totalPages > 1" class="flex items-center justify-between mt-6 pt-4 border-t border-gray-100">
            <span class="text-sm text-gray-500">共 {{ totalActivities }} 条</span>
            <div class="flex items-center gap-2">
              <button
                @click="goToPage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="px-3 py-1.5 text-sm rounded-lg border border-gray-200 text-gray-600 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                上一页
              </button>
              <span class="px-3 py-1.5 text-sm text-gray-700">
                {{ currentPage }} / {{ totalPages }}
              </span>
              <button
                @click="goToPage(currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="px-3 py-1.5 text-sm rounded-lg border border-gray-200 text-gray-600 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                下一页
              </button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(2px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}
.custom-scrollbar:hover::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
}

/* Dropdown animation */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
