<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, watch, computed } from 'vue';
import { useRouter } from 'vue-router';
import Button from '@/components/ui/Button.vue';
import Input from '@/components/ui/Input.vue';
import Textarea from '@/components/ui/Textarea.vue';
import Card from '@/components/ui/Card.vue';
import CardHeader from '@/components/ui/CardHeader.vue';
import CardTitle from '@/components/ui/CardTitle.vue';
import CardDescription from '@/components/ui/CardDescription.vue';
import CardContent from '@/components/ui/CardContent.vue';
import CardFooter from '@/components/ui/CardFooter.vue';
import Badge from '@/components/ui/Badge.vue';
import Tooltip from '@/components/ui/Tooltip.vue';
import Spinner from '@/components/ui/Spinner.vue';
import { useAuth } from '@/composables/useAuth';
import { useAgents } from '@/composables/useAgents';
import { useTools } from '@/composables/useTools';
import { useProjects } from '@/composables/useProjects';
import { useDocuments } from '@/composables/useDocuments';
import { useReviews } from '@/composables/useReviews';
import { useCarousels } from '@/composables/useCarousels';
import { useFooter } from '@/composables/useFooter';
import { Send, Bot, ChevronLeft, ChevronRight, Sun, Moon, Calendar, ArrowRight, Star, Check } from 'lucide-vue-next';

const router = useRouter();

const inviteCode = ref('');
const isDialogOpen = ref(false);
const isCancelAuthDialogOpen = ref(false);
const { isAuthorized, verifyInviteCode, revokeAuthorization, errorMessage, checkPermission } = useAuth();

const { agents, selectedAgent, setSelectedAgent, loadData } = useAgents();
const { tools, loading: toolsLoading } = useTools();
const { projects, categories: projectCategories } = useProjects();
const { documents, categories: documentCategories, loading: documentsLoading } = useDocuments();
const { reviews, submitReview, refreshReviews, loading: reviewsLoading } = useReviews();
const { messages: marqueeMessages, isError: marqueeIsError } = useCarousels();
const { config: footerConfig, links: footerLinks, loading: footerLoading } = useFooter();

const isDataLoading = computed(() => {
  return documentsLoading.value || reviewsLoading.value || toolsLoading.value;
});

const selectedAgentName = computed(() => {
  const agent = agents.value.find(a => a.id === selectedAgent.value);
  return agent?.name || selectedAgent.value || '请选择智能体';
});

const getCategoryColorClass = (color: string, isDark: boolean) => {
  const colorMap: Record<string, { dark: string; light: string }> = {
    '#3b82f6': { dark: 'bg-blue-900/50 text-blue-200 hover:bg-blue-800/50', light: 'bg-blue-100 text-blue-700 hover:bg-blue-200' },
    '#10b981': { dark: 'bg-green-900/50 text-green-200 hover:bg-green-800/50', light: 'bg-green-100 text-green-700 hover:bg-green-200' },
    '#f59e0b': { dark: 'bg-amber-900/50 text-amber-200 hover:bg-amber-800/50', light: 'bg-amber-100 text-amber-700 hover:bg-amber-200' },
    '#ef4444': { dark: 'bg-red-900/50 text-red-200 hover:bg-red-800/50', light: 'bg-red-100 text-red-700 hover:bg-red-200' },
    '#8b5cf6': { dark: 'bg-violet-900/50 text-violet-200 hover:bg-violet-800/50', light: 'bg-violet-100 text-violet-700 hover:bg-violet-200' },
  };
  return colorMap[color]?.[isDark ? 'dark' : 'light'] || (isDark ? 'bg-gray-700 text-gray-200 hover:bg-gray-600' : 'bg-gray-100 text-gray-700 hover:bg-gray-200');
};

const categoryColorMap = computed(() => {
  const map: Record<string, string> = {};
  documentCategories.value.forEach(cat => {
    map[cat.name] = cat.color;
  });
  return map;
});

const getBadgeClass = (categoryName: string, isDark: boolean) => {
  const color = categoryColorMap.value[categoryName] || '#3b82f6';
  return getCategoryColorClass(color, isDark);
};

const goToDocument = (url: string) => {
  const permission = checkPermission('documents');
  if (!permission.hasPermission) {
    showToastMessage(permission.message || '无权限访问', 'error');
    return;
  }
  if (url) {
    window.open(url, '_blank');
  }
};

const goToTool = (url: string) => {
  const permission = checkPermission('tools');
  if (!permission.hasPermission) {
    showToastMessage(permission.message || '无权限访问', 'error');
    return;
  }
  if (url) {
    window.open(url, '_blank');
  }
};

const API_BASE = 'http://localhost:8000';

const getImageUrl = (imagePath: string | undefined | null) => {
  if (!imagePath) return '';
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://') || imagePath.startsWith('data:')) {
    return imagePath;
  }
  return `${API_BASE}${imagePath}`;
};

const handleImageError = (_event: Event, toolId: string) => {
  imageLoadError.value = { ...imageLoadError.value, [toolId]: true };
};

const checkImageError = (toolId: string) => {
  return imageLoadError.value[toolId] === true;
};

const handleToolHover = (event: MouseEvent, toolId: string, description: string) => {
  const rect = (event.target as HTMLElement).getBoundingClientRect();
  hoveredToolId.value = toolId;
  hoveredToolDescription.value = description;
  hoveredToolPosition.value = {
    x: rect.right - 40,
    y: rect.top + rect.height / 2
  };
};

const handleToolLeave = () => {
  hoveredToolId.value = null;
  hoveredToolDescription.value = '';
};

const handleDocHover = (event: MouseEvent, docId: string, description: string) => {
  const rect = (event.target as HTMLElement).getBoundingClientRect();
  hoveredDocId.value = docId;
  hoveredDocDescription.value = description;
  hoveredDocPosition.value = {
    x: rect.left + rect.width / 2,
    y: rect.top - 8
  };
};

const handleDocLeave = () => {
  hoveredDocId.value = null;
  hoveredDocDescription.value = '';
};

const footerLinkGroups = computed(() => {
  const groups = [];
  for (let i = 0; i < footerLinks.value.length; i += 7) {
    groups.push(footerLinks.value.slice(i, i + 7));
  }
  return groups;
});

const footerSloganLines = computed(() => {
  let text = footerConfig.value.slogan || '';
  text = text.replace(/\\n/g, '\n');
  const maxCharsPerLine = 35;
  const lines: string[] = [];
  
  const rawLines = text.split('\n').filter(line => line.trim() !== '');
  
  for (const rawLine of rawLines) {
    if (rawLine.length <= maxCharsPerLine) {
      lines.push(rawLine);
    } else {
      for (let i = 0; i < rawLine.length; i += maxCharsPerLine) {
        lines.push(rawLine.slice(i, i + maxCharsPerLine));
      }
    }
  }
  
  return lines;
});

const isTextTruncated = (text: string, maxLines = 2) => {
  const maxCharsPerLine = 20;
  const maxChars = maxLines * maxCharsPerLine;
  return text.length > maxChars;
};

const isDark = ref(false);
const imageLoadError = ref<Record<string, boolean>>({});
const hoveredToolId = ref<string | null>(null);
const hoveredToolPosition = ref({ x: 0, y: 0 });
const hoveredToolDescription = ref('');
const hoveredDocId = ref<string | null>(null);
const hoveredDocPosition = ref({ x: 0, y: 0 });
const hoveredDocDescription = ref('');
const isThemeInitialized = ref(false);
const isLoading = ref(true);

onMounted(async () => {
  const saved = localStorage.getItem('isDark');
  const isDarkTheme = saved !== null ? saved === 'true' : false;
  isDark.value = isDarkTheme;
  isThemeInitialized.value = true;
  
  const checkLoading = setInterval(() => {
    if (!documentsLoading.value && !reviewsLoading.value && !toolsLoading.value) {
      clearInterval(checkLoading);
      isLoading.value = false;
    }
  }, 100);
  
  setTimeout(() => {
    clearInterval(checkLoading);
    isLoading.value = false;
  }, 10000);
});

const toggleTheme = () => {
  const newDarkState = !isDark.value;
  isDark.value = newDarkState;
  localStorage.setItem('isDark', newDarkState.toString());
  
  if (newDarkState) {
    document.documentElement.classList.add('dark');
    if (document.body) {
      document.body.style.backgroundColor = '#0f172a';
    }
  } else {
    document.documentElement.classList.remove('dark');
    if (document.body) {
      document.body.style.backgroundColor = '#ffffff';
    }
  }
};

const searchQuery = ref('');

const displayMarqueeMessages = computed(() => {
  if (!marqueeMessages.value || marqueeMessages.value.length === 0) return [];
  return [...marqueeMessages.value, ...marqueeMessages.value];
});

const marqueeDuration = computed(() => {
  const count = marqueeMessages.value.length;
  return count > 0 ? count * 5 : 5;
});

onMounted(() => {});

onUnmounted(() => {});

watch(marqueeMessages, () => {});

const reviewContent = ref('');
const reviewScrollIndex = ref(0);
const disableTransition = ref(false);
const textareaRef = ref<HTMLTextAreaElement | null>(null);
const messagesContainerRef = ref<HTMLDivElement | null>(null);

const showToast = ref(false);
const toastMessage = ref('');
const toastType = ref<'success' | 'error'>('success');

const isReviewConfirmDialogOpen = ref(false);
const isAgentDialogOpen = ref(false);
const tempSelectedAgent = ref('');
const agentSearchQuery = ref('');
const isScrolled = ref(false);

const showToastMessage = (message: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = message;
  toastType.value = type;
  showToast.value = true;
  
  setTimeout(() => {
    showToast.value = false;
  }, 3000);
};

const handleScroll = () => {
  isScrolled.value = window.scrollY > 10;
  console.log('scrollY:', window.scrollY, 'isScrolled:', isScrolled.value);
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});

watch(isAgentDialogOpen, (newVal) => {
  if (newVal) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});

const filteredAgents = computed(() => {
  if (!agents.value || !Array.isArray(agents.value)) {
    return [];
  }
  if (!agentSearchQuery.value.trim()) {
    return agents.value;
  }
  const query = agentSearchQuery.value.toLowerCase().trim();
  return agents.value.filter(agent => 
    agent.name.toLowerCase().includes(query) || 
    agent.description.toLowerCase().includes(query)
  );
});

const expandedReviews = computed(() => {
  const reviewsArray = reviews.value || [];
  return [...reviewsArray, ...reviewsArray, ...reviewsArray];
});

const messages = ref<Array<{
  id: number;
  content: string;
  isUser: boolean;
  timestamp: Date;
}>>([]);

const isTerminated = ref(false);
const toolRow1Scroll = ref(0);
const toolRow2Scroll = ref(0);
const selectedCategory = ref<string>('all');
const isChatMode = ref(false);

watch(messages, () => {
  nextTick(() => {
    if (messagesContainerRef.value) {
      messagesContainerRef.value.scrollTop = messagesContainerRef.value.scrollHeight;
    }
  });
});

const adjustTextareaHeight = () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto';
    textareaRef.value.style.height = `${textareaRef.value.scrollHeight}px`;
  }
};

watch(searchQuery, () => {
  adjustTextareaHeight();
});

const handleAgentConfirm = () => {
  const permission = checkPermission('agents');
  if (!permission.hasPermission) {
    showToastMessage(permission.message || '无权限使用智能体', 'error');
    isAgentDialogOpen.value = false;
    return;
  }
  setSelectedAgent(tempSelectedAgent.value);
  isAgentDialogOpen.value = false;
  agentSearchQuery.value = '';
};

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    const userMessage = {
      id: Date.now(),
      content: searchQuery.value,
      isUser: true,
      timestamp: new Date()
    };
    messages.value = [...messages.value, userMessage];
    
    setTimeout(() => {
      const systemMessage = {
        id: Date.now() + 1,
        content: `我收到了您的消息："${searchQuery.value}"。这是一个模拟的系统回复。实际应用中，这里会显示AI的回复内容。`,
        isUser: false,
        timestamp: new Date()
      };
      messages.value = [...messages.value, systemMessage];
    }, 500);
    
    searchQuery.value = '';
    isTerminated.value = false;
    isChatMode.value = true;
  }
};

const handleBackToInitial = () => {
  isChatMode.value = false;
  searchQuery.value = '';
  messages.value = [];
  isTerminated.value = false;
};

const handleTerminateTask = () => {
  isTerminated.value = !isTerminated.value;
};

const handleToolScroll = (row: number, direction: 'left' | 'right') => {
  const scrollAmount = 300;
  const maxScroll = 600;
  
  if (row === 1) {
    const newScroll = direction === 'left' ? toolRow1Scroll.value - scrollAmount : toolRow1Scroll.value + scrollAmount;
    toolRow1Scroll.value = Math.max(0, Math.min(newScroll, maxScroll));
  } else {
    const newScroll = direction === 'left' ? toolRow2Scroll.value - scrollAmount : toolRow2Scroll.value + scrollAmount;
    toolRow2Scroll.value = Math.max(0, Math.min(newScroll, maxScroll));
  }
};

const handleInviteCode = async () => {
  if (!inviteCode.value.trim()) {
    errorMessage.value = '请输入授权码，再点击确认！';
    return;
  }
  const result = await verifyInviteCode(inviteCode.value.trim());
  if (result.success) {
    isDialogOpen.value = false;
    inviteCode.value = '';
  }
};

const handleCancelAuth = async () => {
  await revokeAuthorization();
  isCancelAuthDialogOpen.value = false;
};

const handleReviewSubmit = () => {
  if (reviewContent.value.trim()) {
    isReviewConfirmDialogOpen.value = true;
  }
};

const handleReviewConfirm = async () => {
  console.log('Submitting review:', reviewContent.value);
  const result = await submitReview({
    name: '当前用户',
    rating: 5,
    content: reviewContent.value
  });
  console.log('Submit result:', result);
  
  if (result.success) {
    console.log('Submission successful, clearing input and refreshing reviews');
    reviewContent.value = '';
    showToastMessage('评价成功！', 'success');
    await refreshReviews();
  } else {
    console.log('Submission failed:', result.message);
    showToastMessage(`提交失败: ${result.message}`, 'error');
  }
  
  isReviewConfirmDialogOpen.value = false;
};

const filteredRecommendations = computed(() => {
  return selectedCategory.value === 'all'
    ? documents.value
    : documents.value.filter(item => item.category === selectedCategory.value);
});

const documentsRow1 = computed(() => {
  return filteredRecommendations.value.filter(item => !item.row || item.row === 'row1');
});

const documentsRow2 = computed(() => {
  return filteredRecommendations.value.filter(item => item.row === 'row2');
});
</script>

<template>
  <div>
    <div v-if="!isThemeInitialized" class="fixed inset-0 z-[100] flex items-center justify-center bg-white dark:bg-slate-900">
      <div class="flex flex-col items-center gap-4">
        <div class="relative w-12 h-12">
          <div class="absolute inset-0 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <div class="absolute inset-2 border-4 border-blue-400 border-b-transparent rounded-full animate-spin" style="animation-direction: reverse"></div>
        </div>
        <p class="text-sm font-medium text-gray-600 dark:text-gray-300">
          加载中...
        </p>
      </div>
    </div>

    <div v-if="(isLoading || isDataLoading) && isThemeInitialized" :class="`fixed inset-0 z-[100] flex items-center justify-center ${isDark ? 'bg-slate-900/60' : 'bg-white/60'} backdrop-blur-sm transition-opacity duration-300`">
      <div class="flex flex-col items-center gap-4">
        <div class="relative w-12 h-12">
          <div :class="`absolute inset-0 border-4 ${isDark ? 'border-purple-500' : 'border-blue-500'} border-t-transparent rounded-full animate-spin`"></div>
          <div :class="`absolute inset-2 border-4 ${isDark ? 'border-purple-400' : 'border-blue-400'} border-b-transparent rounded-full animate-spin`" style="animation-direction: reverse"></div>
        </div>
        <p :class="`text-sm font-medium ${isDark ? 'text-gray-300' : 'text-gray-600'}`">
          加载中...
        </p>
      </div>
    </div>

    <header v-if="isThemeInitialized" :class="`fixed top-0 left-0 right-0 z-[1000] transition-all duration-300 ${isScrolled ? 'py-2 shadow-xl' : 'py-4 shadow-lg'} ${isDark ? 'bg-slate-900 border-slate-700' : 'bg-white border-gray-200'} backdrop-blur-xl border-b px-8`">
      <div class="mx-auto flex items-center justify-between max-w-[1800px] xl:max-w-[2000px] 2xl:max-w-[2200px]">
          <div class="flex items-center space-x-3">
            <div 
              v-if="footerLoading"
              :class="`h-12 w-12 rounded-lg flex items-center justify-center ${isDark ? 'bg-slate-700' : 'bg-gray-100'}`"
            >
              <Spinner :class="`w-5 h-5 ${isDark ? 'text-gray-400' : 'text-gray-400'}`" />
            </div>
            <div 
              v-else-if="footerConfig.logo_url"
              class="h-12 w-12 rounded-lg overflow-hidden"
            >
              <img 
                :src="footerConfig.logo_url" 
                alt="Logo" 
                class="h-full w-full object-contain"
              />
            </div>
            <div 
              v-else
              :class="`h-12 w-12 rounded-lg border flex items-center justify-center ${isDark ? 'bg-slate-800 border-slate-600' : 'bg-white border-gray-200'}`"
            >
              <svg :class="`w-6 h-6 ${isDark ? 'text-slate-600' : 'text-gray-300'}`" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="h-6 w-[500px] overflow-hidden">
              <div
                class="marquee-container"
                :style="{ '--duration': marqueeDuration + 's' }"
              >
                <div v-for="(msg, index) in displayMarqueeMessages" :key="index" :class="`h-6 flex items-center text-sm ${marqueeIsError ? 'text-red-500' : (isDark ? 'text-gray-300' : 'text-gray-600')}`">
                  <span class="truncate">{{ msg }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <Button
              @click="toggleTheme"
              variant="outline"
              :class="`${isDark ? 'bg-slate-800 hover:bg-slate-700 border-slate-600 text-gray-200' : 'bg-white hover:bg-gray-50 border-gray-200 text-gray-700'}`"
            >
              <Sun v-if="isDark" class="w-4 h-4 mr-2" />
              <Moon v-else class="w-4 h-4 mr-2" />
              {{ isDark ? '明' : '暗' }}
            </Button>

            <Button
              @click="isAuthorized ? isCancelAuthDialogOpen = true : isDialogOpen = true"
              :class="isAuthorized ? 'bg-gradient-to-r from-indigo-900 via-purple-900 to-indigo-900 hover:from-indigo-800 hover:via-purple-800 hover:to-indigo-800 text-white' : 'bg-black hover:bg-gray-800 text-white'"
            >
              {{ isAuthorized ? '已授权' : '未授权' }}
            </Button>
          </div>
        </div>
      </header>

      <div v-if="isThemeInitialized" :class="`${isChatMode ? 'h-screen overflow-hidden' : 'min-h-screen'} bg-gradient-to-br from-cyan-50/30 via-blue-50/20 to-violet-50/30 dark:from-gray-900/95 dark:via-slate-900/90 dark:to-slate-800/95 backdrop-blur-[2px] relative overflow-x-hidden`">
        <div class="absolute top-20 left-10 w-64 h-64 bg-cyan-400/15 rounded-full blur-3xl animate-float"></div>
        <div class="absolute top-40 right-20 w-96 h-96 bg-blue-400/10 rounded-full blur-3xl animate-float-delay"></div>
        <div class="absolute bottom-40 left-1/4 w-80 h-80 bg-violet-400/15 rounded-full blur-3xl animate-float-slow"></div>
        <div class="absolute bottom-20 right-1/3 w-72 h-72 bg-indigo-400/10 rounded-full blur-3xl animate-float-delay-slow"></div>

        <div :class="`relative ${isChatMode ? 'flex flex-col pt-[80px] h-screen overflow-hidden' : 'pt-40 pb-20'}`">
        <div v-if="!isChatMode" class="mx-auto max-w-4xl px-8">
          <div class="text-center space-y-8">
            <h1 :class="`text-4xl font-bold tracking-tight ${isDark ? 'text-white' : 'text-gray-900'}`">
              智能问答
            </h1>

            <p :class="`text-lg max-w-2xl mx-auto leading-relaxed ${isDark ? 'text-gray-300' : 'text-gray-600'}`">
              AI 驱动的智能搜索，为您提供精准、高效的信息检索服务
            </p>

            <div class="max-w-4xl mx-auto flex items-start justify-between">
              <div class="relative">
                <button
                  @click="isAgentDialogOpen = true; tempSelectedAgent = selectedAgent; loadData()"
                  :class="`flex items-center gap-2 px-4 py-2.5 ${isDark ? 'bg-slate-800 hover:bg-slate-700 border-slate-600 text-gray-200' : 'bg-white hover:bg-gray-50 border-gray-200 text-gray-700'} border rounded-xl shadow-sm transition-all duration-200 group`"
                >
                  <Bot :class="`w-5 h-5 ${isDark ? 'text-purple-400' : 'text-purple-600'}`" />
                  <span :class="`text-sm font-medium ${isDark ? 'text-gray-200' : 'text-gray-700'}`">{{ selectedAgentName }}</span>
                  <svg :class="`w-4 h-4 ${isDark ? 'text-gray-400 group-hover:text-gray-300' : 'text-gray-400 group-hover:text-gray-600'} transition-colors`" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
              </div>
            </div>

            <div class="max-w-4xl mx-auto -mt-[27px]">
              <div :class="`relative rounded-2xl shadow-lg border ${isDark ? 'bg-slate-800 border-slate-600' : 'bg-white border-gray-200'}`">
                <div class="relative p-4 pr-14">
                  <textarea
                    ref="textareaRef"
                    :placeholder="isTerminated ? '任务已终止，点击重新开始' : '请输入您的问题...'"
                    v-model="searchQuery"
                    @keydown="(e: KeyboardEvent) => { if (e.key === 'Enter' && !e.shiftKey && !isTerminated) { e.preventDefault(); handleSearch(); } }"
                    rows="1"
                    :disabled="isTerminated"
                    :class="`w-full resize-none outline-none text-left text-base leading-relaxed min-h-[56px] max-h-[200px] bg-transparent ${
                      isTerminated
                        ? 'text-gray-400 placeholder:text-gray-400 cursor-not-allowed'
                        : `${isDark ? 'text-white placeholder:text-gray-400' : 'text-gray-900 placeholder:text-gray-400'}`
                    }`"
                    style="overflow-y: auto; height: auto"
                  />

                  <button
                    @click="handleSearch"
                    :disabled="isTerminated || !searchQuery.trim()"
                    :class="`absolute bottom-4 right-4 p-2 rounded-lg transition-all duration-200 flex items-center justify-center ${
                      isTerminated || !searchQuery.trim()
                        ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                        : 'bg-purple-600 hover:bg-purple-700 text-white'
                    }`"
                  >
                    <Send class="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="relative h-full flex flex-col overflow-hidden">
          <div class="flex-shrink-0 px-8 py-4">
            <div class="max-w-4xl mx-auto flex items-center justify-end">
              <button
                @click="handleBackToInitial"
                :class="`flex items-center gap-2 px-4 py-2.5 rounded-xl shadow-sm transition-all duration-200 ${isDark ? 'bg-blue-600 hover:bg-blue-700 text-white' : 'bg-gray-900 hover:bg-gray-800 text-white'}`"
              >
                <svg :class="`w-4 h-4`" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                <span class="text-sm font-medium">返回</span>
              </button>
            </div>
          </div>

          <div class="flex-1 px-8 overflow-y-auto" ref="messagesContainerRef">
            <div class="max-w-4xl mx-auto py-6 space-y-6">
              <div v-if="messages.length === 0" class="flex items-center justify-center h-full min-h-[300px]">
                <div class="text-center space-y-4">
                  <div class="w-16 h-16 mx-auto bg-gradient-to-br from-purple-100 to-blue-100 rounded-2xl flex items-center justify-center">
                    <Bot class="w-8 h-8 text-purple-400" />
                  </div>
                  <div>
                    <p :class="`${isDark ? 'text-white' : 'text-gray-900'} font-medium mb-1`">开始对话</p>
                    <p :class="`text-sm ${isDark ? 'text-gray-300' : 'text-gray-500'}`">输入问题，开始与AI智能助手对话</p>
                  </div>
                </div>
              </div>

              <div
                v-for="msg in messages"
                :key="msg.id"
                :class="`flex ${msg.isUser ? 'justify-end' : 'justify-start'} animate-fade-in`"
              >
                <div
                  :class="`max-w-[85%] rounded-2xl px-5 py-4 shadow-md transition-all duration-200 ${
                    msg.isUser
                      ? isDark ? 'bg-slate-700 text-white rounded-br-md shadow-slate-600/30' : 'bg-gray-100 text-gray-800 rounded-br-md shadow-gray-200'
                      : isDark ? 'bg-slate-800 border border-slate-600 text-white rounded-bl-md shadow-slate-700/50' : 'bg-gradient-to-br from-white to-gray-50 border border-gray-200 text-gray-800 rounded-bl-md shadow-gray-100/50'
                  }`"
                >
                  <p class="text-[15px] leading-relaxed whitespace-pre-wrap break-words">{{ msg.content }}</p>
                  <div :class="`flex items-center gap-2 mt-3 pt-2 border-t ${isDark ? 'border-white/5' : 'border-black/5'}`">
                    <p :class="`text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'}`">
                      {{ msg.timestamp.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }) }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div :class="`flex-shrink-0 ${isDark ? 'bg-gradient-to-t from-slate-900 via-slate-900/95 to-transparent' : 'bg-gradient-to-t from-slate-50 via-slate-50/95 to-transparent'} pt-8 pb-8 px-8`">
            <div class="max-w-4xl mx-auto">
              <div class="mb-3 flex justify-center">
                <button
                  @click="handleTerminateTask"
                  :class="`flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 text-sm ${
                    isTerminated
                      ? 'bg-blue-50 hover:bg-blue-100 border border-blue-200 text-blue-700'
                      : 'bg-red-50 hover:bg-red-100 border border-red-200 text-red-700'
                  }`"
                >
                  <template v-if="isTerminated">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    <span>重新开始</span>
                  </template>
                  <template v-else>
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                      <rect x="6" y="6" width="12" height="12" rx="2" />
                    </svg>
                    <span>终止任务</span>
                  </template>
                </button>
              </div>

              <div :class="`relative rounded-2xl shadow-lg border transition-colors ${isDark ? 'bg-slate-800 border-slate-600' : 'bg-white border-gray-200'}`">
                <div class="relative p-4 pr-14">
                  <textarea
                    ref="textareaRef"
                    placeholder="请输入您的问题..."
                    v-model="searchQuery"
                    @keydown="(e: KeyboardEvent) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSearch(); } }"
                    rows="1"
                    :class="`w-full resize-none outline-none text-left text-base leading-relaxed min-h-[56px] max-h-[200px] bg-transparent ${isDark ? 'text-white placeholder:text-gray-400' : 'text-gray-900 placeholder:text-gray-400'}`"
                    style="overflow-y: auto; height: auto"
                  />

                  <button
                    @click="handleSearch"
                    :disabled="!searchQuery.trim()"
                    :class="`absolute bottom-4 right-4 p-2 rounded-lg transition-all duration-200 flex items-center justify-center ${
                      searchQuery.trim()
                        ? 'bg-purple-600 hover:bg-purple-700 text-white'
                        : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                    }`"
                  >
                    <Send class="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <section :class="`mx-auto max-w-7xl px-8 py-12 rounded-3xl my-10 border ${isDark ? 'bg-gradient-to-br from-slate-800/60 via-slate-700/70 to-slate-800/50 border-slate-500/30 backdrop-blur-sm' : 'bg-gradient-to-br from-cyan-50/30 via-white to-blue-50/20 border-gray-200/50 backdrop-blur-sm'} shadow-xl`">
        <h2 :class="`text-2xl font-bold mb-10 tracking-tight ${isDark ? 'text-white' : 'text-gray-900'}`">
          开源项目分享
        </h2>

        <div v-if="toolsLoading" class="flex flex-col items-center justify-center py-20">
          <div class="relative w-12 h-12">
            <div :class="`absolute inset-0 border-4 ${isDark ? 'border-purple-500' : 'border-blue-500'} border-t-transparent rounded-full animate-spin`"></div>
            <div :class="`absolute inset-2 border-4 ${isDark ? 'border-purple-400' : 'border-blue-400'} border-b-transparent rounded-full animate-spin`" style="animation-direction: reverse"></div>
          </div>
          <p :class="`mt-4 text-sm ${isDark ? 'text-gray-400' : 'text-gray-500'}`">加载中...</p>
        </div>

        <template v-else>
          <div v-if="tools.length === 0" class="flex flex-col items-center justify-center py-16">
            <div :class="`text-lg ${isDark ? 'text-gray-400' : 'text-gray-500'}`">暂无数据</div>
            <p :class="`text-sm mt-2 ${isDark ? 'text-gray-500' : 'text-gray-400'}`">暂无开源项目，敬请期待</p>
          </div>
          <div v-else class="mb-8 relative">
            <button
              @click="handleToolScroll(1, 'left')"
              :disabled="toolRow1Scroll <= 0"
              :class="`absolute -left-2 top-1/2 -translate-y-1/2 z-10 w-10 h-10 flex items-center justify-center rounded-lg disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-300 group ${isDark ? 'bg-slate-700/95 hover:bg-slate-600 border border-cyan-500/40 hover:border-cyan-400 shadow-lg shadow-cyan-500/10 hover:shadow-cyan-500/20' : 'bg-white/90 hover:bg-white border border-gray-200 hover:border-cyan-400'} backdrop-blur-sm shadow-md hover:shadow-lg`"
            >
              <ChevronLeft :class="`w-5 h-5 transition-all duration-300 ${isDark ? 'text-cyan-400 group-hover:text-cyan-300' : 'text-gray-400 group-hover:text-cyan-500'} group-disabled:opacity-50`" />
            </button>

            <div class="flex-1 overflow-hidden px-6">
              <div 
                class="flex transition-transform duration-300 ease-in-out gap-4"
                :style="{ transform: `translateX(-${toolRow1Scroll}px)` }"
              >
                <div
                  v-for="(tool, index) in tools.filter(t => !t.row || t.row === 'row1').slice(0, 6)"
                  :key="tool.id"
                  @click="goToTool(tool.path || 'https://www.baidu.com/')"
                  class="flex-shrink-0 w-[280px] flex flex-col gap-3 group cursor-pointer"
                >
                  <div :class="`h-36 rounded-lg border hover:shadow-md transition-all duration-300 overflow-hidden ${isDark ? 'bg-slate-800 border-slate-600 hover:border-slate-500' : 'bg-white border-gray-200 hover:border-gray-400'}`">
                    <img 
                      v-if="tool.image && !checkImageError(tool.id)"
                      :src="getImageUrl(tool.image)"
                      :alt="tool.name"
                      @error="(e) => handleImageError(e, tool.id)"
                      class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                    />
                    <div v-if="!tool.image || checkImageError(tool.id)" :class="`h-36 flex items-center justify-center ${isDark ? 'bg-slate-800 border-slate-600' : 'bg-white border-gray-200'}`">
                      <span :class="`text-4xl ${isDark ? 'text-gray-400' : 'text-gray-300'}`">{{ tool.name.charAt(0) }}</span>
                    </div>
                  </div>
                  
                  <div :class="`rounded-lg hover:shadow-md transition-all duration-300 p-4 overflow-visible ${isDark ? 'bg-slate-800' : 'bg-white'}`">
                    <h3 :class="`text-base font-semibold mb-2 group-hover:text-gray-200 transition-colors ${isDark ? 'text-white group-hover:text-gray-200' : 'text-gray-900 group-hover:text-gray-700'}`">
                      {{ tool.name }}
                    </h3>
                    <div v-if="isTextTruncated(tool.description)" class="relative h-10" @mouseenter="(e) => handleToolHover(e, tool.id, tool.description)" @mouseleave="handleToolLeave">
                      <p class="text-sm line-clamp-2 transition-all duration-200 leading-relaxed text-gray-400 dark:text-gray-400 text-gray-500" :class="{ 'text-blue-500': hoveredToolId === tool.id }">
                        {{ tool.description }}
                      </p>
                    </div>
                    <div v-else class="h-10">
                      <p class="text-sm line-clamp-2 transition-all duration-200 leading-relaxed text-gray-400 dark:text-gray-400 text-gray-500">
                        {{ tool.description }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <button
              @click="handleToolScroll(1, 'right')"
              :disabled="toolRow1Scroll >= 600 || tools.filter(t => !t.row || t.row === 'row1').length <= 4"
              :class="`absolute -right-3 top-1/2 -translate-y-1/2 z-10 w-10 h-10 flex items-center justify-center rounded-lg disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-300 group ${isDark ? 'bg-slate-700/95 hover:bg-slate-600 border border-cyan-500/40 hover:border-cyan-400 shadow-lg shadow-cyan-500/10 hover:shadow-cyan-500/20' : 'bg-white/90 hover:bg-white border border-gray-200 hover:border-cyan-400'} backdrop-blur-sm shadow-md hover:shadow-lg`"
            >
              <ChevronRight :class="`w-5 h-5 transition-all duration-300 ${isDark ? 'text-cyan-400 group-hover:text-cyan-300' : 'text-gray-400 group-hover:text-cyan-500'} group-disabled:opacity-50`" />
            </button>
          </div>

          <div v-if="tools.length > 6" class="relative">
            <button
              @click="handleToolScroll(2, 'left')"
              :disabled="toolRow2Scroll <= 0"
              :class="`absolute -left-2 top-1/2 -translate-y-1/2 z-10 w-10 h-10 flex items-center justify-center rounded-lg disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-300 group ${isDark ? 'bg-slate-700/95 hover:bg-slate-600 border border-cyan-500/40 hover:border-cyan-400 shadow-lg shadow-cyan-500/10 hover:shadow-cyan-500/20' : 'bg-white/90 hover:bg-white border border-gray-200 hover:border-cyan-400'} backdrop-blur-sm shadow-md hover:shadow-lg`"
            >
              <ChevronLeft :class="`w-5 h-5 transition-all duration-300 ${isDark ? 'text-cyan-400 group-hover:text-cyan-300' : 'text-gray-400 group-hover:text-cyan-500'} group-disabled:opacity-50`" />
            </button>

            <div class="flex-1 overflow-hidden px-6">
              <div 
                class="flex transition-transform duration-300 ease-in-out gap-4"
                :style="{ transform: `translateX(-${toolRow2Scroll}px)` }"
              >
                <div
                  v-for="(tool, index) in tools.filter(t => t.row === 'row2').slice(0, 6)"
                  :key="index"
                  @click="goToTool(tool.path || 'https://www.baidu.com/')"
                  class="flex-shrink-0 w-[280px] flex flex-col gap-3 group cursor-pointer"
                >
                  <div :class="`h-36 rounded-lg border hover:shadow-md transition-all duration-300 overflow-hidden ${isDark ? 'bg-slate-800 border-slate-600 hover:border-slate-500' : 'bg-white border-gray-200 hover:border-gray-400'}`">
                    <img 
                      v-if="tool.image && !checkImageError(tool.id)"
                      :src="getImageUrl(tool.image)"
                      :alt="tool.name"
                      @error="(e) => handleImageError(e, tool.id)"
                      class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                    />
                    <div v-if="!tool.image || checkImageError(tool.id)" :class="`h-36 flex items-center justify-center ${isDark ? 'bg-slate-800 border-slate-600' : 'bg-white border-gray-200'}`">
                      <span :class="`text-4xl ${isDark ? 'text-gray-400' : 'text-gray-300'}`">{{ tool.name.charAt(0) }}</span>
                    </div>
                  </div>
                  
                  <div :class="`rounded-lg hover:shadow-md transition-all duration-300 p-4 overflow-visible ${isDark ? 'bg-slate-800' : 'bg-white'}`">
                    <h3 :class="`text-base font-semibold mb-2 group-hover:text-gray-200 transition-colors ${isDark ? 'text-white group-hover:text-gray-200' : 'text-gray-900 group-hover:text-gray-700'}`">
                      {{ tool.name }}
                    </h3>
                    <div v-if="isTextTruncated(tool.description)" class="relative h-10" @mouseenter="(e) => handleToolHover(e, tool.id, tool.description)" @mouseleave="handleToolLeave">
                      <p class="text-sm line-clamp-2 transition-all duration-200 leading-relaxed text-gray-400 dark:text-gray-400 text-gray-500" :class="{ 'text-blue-500': hoveredToolId === tool.id }">
                        {{ tool.description }}
                      </p>
                    </div>
                    <div v-else class="h-10">
                      <p class="text-sm line-clamp-2 transition-all duration-200 leading-relaxed text-gray-400 dark:text-gray-400 text-gray-500">
                        {{ tool.description }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <button
              v-if="tools.length > 6"
              @click="handleToolScroll(2, 'right')"
              :disabled="toolRow2Scroll >= 600 || tools.filter(t => t.row === 'row2').length <= 4"
              :class="`absolute -right-3 top-1/2 -translate-y-1/2 z-10 w-10 h-10 flex items-center justify-center rounded-lg disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-300 group ${isDark ? 'bg-slate-700/95 hover:bg-slate-600 border border-cyan-500/40 hover:border-cyan-400 shadow-lg shadow-cyan-500/10 hover:shadow-cyan-500/20' : 'bg-white/90 hover:bg-white border border-gray-200 hover:border-cyan-400'} backdrop-blur-sm shadow-md hover:shadow-lg`"
            >
              <ChevronRight :class="`w-5 h-5 transition-all duration-300 ${isDark ? 'text-cyan-400 group-hover:text-cyan-300' : 'text-gray-400 group-hover:text-cyan-500'} group-disabled:opacity-50`" />
            </button>
          </div>
        </template>
      </section>

      <section :class="`mx-auto max-w-7xl px-8 py-12 rounded-3xl shadow-lg my-10 overflow-hidden ${isDark ? 'bg-gradient-to-br from-slate-800/80 via-slate-700/90 to-slate-800/60 backdrop-blur-sm' : 'bg-gradient-to-br from-white/90 via-white to-cyan-50/40 backdrop-blur-sm'} border border-gray-200/30`">
        <div class="mb-8">
          <h2 :class="`text-2xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`">
            文档资料
          </h2>
          <div class="mt-4 flex flex-wrap gap-3">
            <Badge
              :class="`${isDark ? 'bg-slate-700 text-gray-200 hover:bg-slate-600' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'} cursor-pointer transition-colors duration-200 px-3 py-1 ${
                selectedCategory === 'all' ? 'ring-2 ring-offset-2 ring-blue-500' : ''
              }`"
              @click="selectedCategory = 'all'"
            >
              全部
            </Badge>
            <Badge
              v-for="cat in documentCategories"
              :key="cat.id"
              :class="`${getCategoryColorClass(cat.color, isDark)} cursor-pointer transition-colors duration-200 px-3 py-1 ${
                selectedCategory === cat.name ? 'ring-2 ring-offset-2 ring-blue-500' : ''
              }`"
              @click="selectedCategory = cat.name"
            >
              {{ cat.name }}
            </Badge>
          </div>
        </div>

        <div class="mt-8">
          <div v-if="filteredRecommendations.length === 0" class="flex flex-col items-center justify-center py-16">
            <div :class="`text-lg ${isDark ? 'text-gray-400' : 'text-gray-500'}`">暂无数据</div>
            <p :class="`text-sm mt-2 ${isDark ? 'text-gray-500' : 'text-gray-400'}`">切换其他分类或等待数据加载</p>
          </div>
          <div v-else>
            <div v-if="documentsRow1.length > 0" class="relative mb-6 overflow-hidden group">
              <div class="flex gap-6 animate-scroll-left w-max">
                <Card v-for="(item, index) in [...documentsRow1, ...documentsRow1, ...documentsRow1]" :key="`left-${index}`" :class="`cursor-pointer transition-all duration-200 hover:shadow-lg w-[280px] flex-shrink-0 border-2 ${isDark ? 'hover:border-blue-300 border-slate-600' : 'hover:border-blue-300 border-gray-200'}`">
                  <CardHeader>
                    <div class="flex items-center justify-between mb-3">
                      <Badge :class="getBadgeClass(item.category, isDark)">
                        {{ item.category }}
                      </Badge>
                    </div>
                    <CardTitle :class="`text-lg font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`">
                      {{ item.title }}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div v-if="isTextTruncated(item.description)" class="relative h-10" @mouseenter="(e) => handleDocHover(e, `doc-left-${index}`, item.description)" @mouseleave="handleDocLeave">
                      <CardDescription :class="`text-sm line-clamp-2 ${isDark ? 'text-gray-400' : 'text-gray-600'}`">
                        {{ item.description }}
                      </CardDescription>
                    </div>
                    <CardDescription v-else :class="`text-sm line-clamp-2 ${isDark ? 'text-gray-400' : 'text-gray-600'}`">
                      {{ item.description }}
                    </CardDescription>
                    <div class="mt-4 flex items-center text-blue-600 text-sm font-medium cursor-pointer" @click="goToDocument(item.url || 'https://www.baidu.com/')">
                      阅读更多
                      <ArrowRight class="ml-1 h-4 w-4" />
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>

            <div v-if="documentsRow2.length > 0" class="relative overflow-hidden group">
              <div class="flex gap-6 animate-scroll-right w-max">
                <Card v-for="(item, index) in [...documentsRow2, ...documentsRow2, ...documentsRow2]" :key="`right-${index}`" :class="`cursor-pointer transition-all duration-200 hover:shadow-lg w-[280px] flex-shrink-0 border-2 ${isDark ? 'hover:border-blue-300 border-slate-600' : 'hover:border-blue-300 border-gray-200'}`">
                  <CardHeader>
                    <div class="flex items-center justify-between mb-3">
                      <Badge :class="getBadgeClass(item.category, isDark)">
                        {{ item.category }}
                      </Badge>
                    </div>
                    <CardTitle :class="`text-lg font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`">
                      {{ item.title }}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div v-if="isTextTruncated(item.description)" class="relative h-10" @mouseenter="(e) => handleDocHover(e, `doc-right-${index}`, item.description)" @mouseleave="handleDocLeave">
                      <CardDescription :class="`text-sm line-clamp-2 ${isDark ? 'text-gray-400' : 'text-gray-600'}`">
                        {{ item.description }}
                      </CardDescription>
                    </div>
                    <CardDescription v-else :class="`text-sm line-clamp-2 ${isDark ? 'text-gray-400' : 'text-gray-600'}`">
                      {{ item.description }}
                    </CardDescription>
                    <div class="mt-4 flex items-center text-blue-600 text-sm font-medium cursor-pointer" @click="goToDocument(item.url || 'https://www.baidu.com/')">
                      阅读更多
                      <ArrowRight class="ml-1 h-4 w-4" />
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section :class="`mx-auto max-w-7xl px-8 py-12 rounded-3xl shadow-lg my-10 ${isDark ? 'bg-gradient-to-br from-slate-800/80 via-slate-700/90 to-slate-800/60 backdrop-blur-sm' : 'bg-gradient-to-br from-white/90 via-white to-blue-50/40 backdrop-blur-sm'} border border-gray-200/30`">
        <h2 :class="`text-xl font-bold mb-4 ${isDark ? 'text-white' : 'text-[#333333]'}`">
          用户评价
        </h2>

        <Card class="mb-6 rounded-lg review-mask-both" style="box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08)">
          <CardContent class="p-6 space-y-4" style="height: 360px; overflow: hidden">
            <div v-if="expandedReviews.length === 0" class="flex flex-col items-center justify-center h-full">
              <div :class="`text-lg ${isDark ? 'text-gray-400' : 'text-gray-500'}`">暂无数据</div>
              <p :class="`text-sm mt-2 ${isDark ? 'text-gray-500' : 'text-gray-400'}`">暂无用户评价，快来发表第一条评价吧</p>
            </div>
            <div v-else 
              :class="disableTransition ? '' : 'transition-all duration-700 ease-in-out'" 
              :style="{ transform: `translateY(-${reviewScrollIndex * 124}px)` }"
            >
              <div v-for="(review, index) in expandedReviews" :key="`${review.id}-${index}`" class="flex items-start gap-3" style="min-height: 124px">
                <div
                  class="flex h-10 w-10 items-center justify-center rounded-full text-white font-semibold text-sm flex-shrink-0"
                  :style="{ backgroundColor: review.avatar_color }"
                >
                  {{ review.avatar }}
                </div>

                <div class="flex-1">
                  <div class="mb-1">
                    <span :class="`text-base font-semibold ${isDark ? 'text-white' : 'text-[#333333]'}`">
                      {{ review.name }}
                    </span>
                    <div class="flex items-center gap-4">
                      <div class="flex">
                        <Star v-for="i in 5" :key="i" :class="`h-3.5 w-3.5 ${i <= review.rating ? 'fill-[#FFC107] text-[#FFC107]' : 'text-gray-300'}`" />
                      </div>
                      <span :class="`text-sm ${isDark ? 'text-gray-400' : 'text-[#999999]'}`">
                        {{ review.date }}
                      </span>
                    </div>
                  </div>
                  <p :class="`text-sm leading-relaxed ${isDark ? 'text-gray-300' : 'text-[#666666]'}`">
                    {{ review.content }}
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card class="rounded-lg" style="box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08)">
          <CardHeader>
            <CardTitle :class="`text-lg font-bold ${isDark ? 'text-white' : 'text-[#333333]'}`">
              发表您的评价
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div class="mb-4">
              <Textarea
                placeholder="分享您的使用体验..."
                v-model="reviewContent"
                class="min-h-[100px] overflow-y-auto"
                :maxlength="500"
                style="border-color: #E0E0E0"
              />
              <div :class="`text-right text-xs ${isDark ? 'text-gray-400' : 'text-[#999999]'} mt-2`">
                {{ reviewContent.length }}/500
              </div>
            </div>
            <Button
              @click="handleReviewSubmit"
              :disabled="!reviewContent.trim()"
              class="text-sm font-bold text-white rounded"
              style="background-color: #1A5F9D; width: 100px; height: 36px; border-radius: 4px"
            >
              提交评价
            </Button>
          </CardContent>
        </Card>
      </section>

      <footer :class="`${isDark ? 'bg-slate-900 border-slate-700' : 'bg-gray-50 border-gray-200'} border-t px-8 py-20`">
        <div class="mx-auto max-w-[1800px] xl:max-w-[2000px] 2xl:max-w-[2200px]">
          <div class="flex items-center justify-center space-x-10">
            <div :class="`flex items-center space-x-3 flex-shrink-0`">
                <div 
                  v-if="footerLoading"
                  :class="`h-16 w-16 rounded-lg flex items-center justify-center ${isDark ? 'bg-slate-700' : 'bg-gray-100'}`"
                >
                  <Spinner :class="`w-6 h-6 ${isDark ? 'text-gray-400' : 'text-gray-400'}`" />
                </div>
                <template v-else-if="footerConfig.logo_url">
                  <img 
                    :src="footerConfig.logo_url" 
                    alt="Logo" 
                    class="h-16 w-16 rounded-lg object-contain"
                  />
                </template>
                <div 
                  v-else
                  :class="`h-16 w-16 rounded-lg border flex items-center justify-center ${isDark ? 'bg-slate-800 border-slate-600' : 'bg-white border-gray-200'}`"
                >
                  <svg :class="`w-8 h-8 ${isDark ? 'text-slate-600' : 'text-gray-300'}`" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <div v-if="footerLoading" :class="`flex flex-col space-y-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`">
                  <div class="h-4 w-32 bg-gray-200 dark:bg-slate-700 rounded animate-pulse"></div>
                  <div class="h-4 w-24 bg-gray-200 dark:bg-slate-700 rounded animate-pulse"></div>
                </div>
                <div v-else-if="footerConfig.slogan" :class="`flex flex-col space-y-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`">
                  <p v-for="(line, lineIndex) in footerSloganLines" :key="lineIndex" class="text-sm leading-relaxed whitespace-pre-wrap">
                    {{ line }}
                  </p>
                </div>
                <div v-else :class="`flex flex-col space-y-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`">
                  <div class="h-4 w-32 bg-gray-200 dark:bg-slate-700 rounded animate-pulse"></div>
                  <div class="h-4 w-24 bg-gray-200 dark:bg-slate-700 rounded animate-pulse"></div>
                </div>
              </div>

            <div :class="`h-24 w-px flex-shrink-0 ${isDark ? 'bg-slate-600' : 'bg-gray-300'}`"></div>

            <div v-if="footerLoading" class="flex flex-col gap-2">
              <div class="flex gap-8">
                <div v-for="i in 5" :key="i" class="h-4 w-16 bg-gray-200 dark:bg-slate-700 rounded animate-pulse"></div>
              </div>
              <div class="flex gap-8">
                <div v-for="i in 5" :key="i + 5" class="h-4 w-16 bg-gray-200 dark:bg-slate-700 rounded animate-pulse"></div>
              </div>
            </div>
            <div v-else-if="footerLinks.length > 0" :class="`flex flex-col space-y-2 text-sm ${isDark ? 'text-gray-300' : 'text-gray-600'}`">
              <div class="flex items-center space-x-8">
                <template v-for="link in footerLinks.slice(0, 5)" :key="link.id">
                  <a
                    v-if="link.url && link.url.trim()"
                    :href="link.url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="inline-block hover:text-blue-600 transition-colors whitespace-nowrap cursor-pointer"
                  >
                    {{ link.title }}
                  </a>
                  <span
                    v-else
                    class="inline-block whitespace-nowrap"
                  >
                    {{ link.title }}
                  </span>
                </template>
              </div>
              <div class="flex items-center space-x-8">
                <template v-for="link in footerLinks.slice(5, 10)" :key="link.id">
                  <a
                    v-if="link.url && link.url.trim()"
                    :href="link.url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="inline-block hover:text-blue-600 transition-colors whitespace-nowrap cursor-pointer"
                  >
                    {{ link.title }}
                  </a>
                  <span
                    v-else
                    class="inline-block whitespace-nowrap"
                  >
                    {{ link.title }}
                  </span>
                </template>
              </div>
            </div>
            <div v-else class="flex flex-col gap-2">
              <div class="flex gap-8">
                <div v-for="i in 5" :key="i" class="h-4 w-16 bg-gray-200 dark:bg-slate-700 rounded animate-pulse"></div>
              </div>
              <div class="flex gap-8">
                <div v-for="i in 5" :key="i + 5" class="h-4 w-16 bg-gray-200 dark:bg-slate-700 rounded animate-pulse"></div>
              </div>
            </div>
          </div>
        </div>
      </footer>

      <Teleport to="body">
        <div v-if="isDialogOpen" class="fixed inset-0 z-[9999] flex items-center justify-center" @click="isDialogOpen = false; inviteCode = ''; errorMessage = ''">
          <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-md"></div>
          <div class="relative w-full max-w-md mx-4" @click.stop>
            <div class="relative bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 dark:border-slate-700/50 overflow-hidden" style="box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(255,255,255,0.1) inset;">
              <button
                @click="isDialogOpen = false; inviteCode = ''; errorMessage = ''"
                class="absolute top-4 right-4 z-10 w-8 h-8 flex items-center justify-center rounded-full hover:bg-slate-100 dark:hover:bg-slate-700 transition-all duration-200 group"
              >
                <svg class="w-5 h-5 text-slate-500 dark:text-slate-400 group-hover:text-red-500 dark:group-hover:text-red-400 group-hover:rotate-90 transition-all duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
              <div class="absolute inset-0 bg-gradient-to-br from-violet-500/10 via-transparent to-indigo-500/10"></div>
              <div class="relative p-8 text-center">
                <div class="inline-flex items-center justify-center w-20 h-20 mb-6 bg-gradient-to-br from-violet-500 to-indigo-600 rounded-2xl shadow-xl shadow-violet-500/30">
                  <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                  </svg>
                </div>
                <h2 class="text-2xl font-bold text-slate-900 dark:text-white mb-2">填写邀请码</h2>
                <p :class="`mb-4 ${errorMessage ? 'text-red-500 dark:text-red-400' : 'text-slate-500 dark:text-slate-400'}`">
                  {{ errorMessage || '请输入授权码进行验证' }}
                </p>
                <div class="mb-8">
                  <Input
                    type="text"
                    placeholder="请输入邀请码"
                    v-model="inviteCode"
                    class="h-14 text-base text-center bg-slate-50/50 dark:bg-slate-900/50 border-2 border-slate-200/50 dark:border-slate-700/50 focus:border-violet-500 dark:focus:border-violet-400 focus:ring-0 rounded-2xl transition-all duration-300"
                    @keydown="(e: KeyboardEvent) => { if (e.key === 'Enter') { handleInviteCode(); } }"
                  />
                </div>
                <div class="flex gap-4">
                  <Button
                    @click="isDialogOpen = false; inviteCode = ''; errorMessage = ''"
                    class="flex-1 h-12 bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 font-medium rounded-xl transition-all duration-300"
                  >
                    取消
                  </Button>
                  <Button
                    @click="handleInviteCode"
                    class="flex-1 h-12 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white font-medium rounded-xl shadow-lg shadow-violet-500/30 hover:shadow-violet-500/50 transition-all duration-300 hover:scale-[1.02] active:scale-[0.98]"
                  >
                    确认
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="isCancelAuthDialogOpen" class="fixed inset-0 z-[9999] flex items-center justify-center" @click="isCancelAuthDialogOpen = false">
          <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-md"></div>
          <div class="relative w-full max-w-md mx-4" @click.stop>
            <div class="relative bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 dark:border-slate-700/50 overflow-hidden" style="box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(255,255,255,0.1) inset;">
              <div class="absolute inset-0 bg-gradient-to-br from-red-500/10 via-transparent to-orange-500/10"></div>
              <div class="relative p-8 text-center">
                <div class="inline-flex items-center justify-center w-20 h-20 mb-6 bg-gradient-to-br from-red-500 to-orange-500 rounded-2xl shadow-xl shadow-red-500/30">
                  <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <h2 class="text-2xl font-bold text-slate-900 dark:text-white mb-2">取消授权</h2>
                <p class="text-slate-500 dark:text-slate-400 mb-8">确定要取消授权吗？取消后将需要重新输入邀请码才能使用。</p>
                <div class="flex gap-4">
                  <Button
                    @click="isCancelAuthDialogOpen = false"
                    class="flex-1 h-12 bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 font-medium rounded-xl transition-all duration-300"
                  >
                    取消
                  </Button>
                  <Button
                    @click="handleCancelAuth"
                    class="flex-1 h-12 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-500 hover:to-orange-500 text-white font-medium rounded-xl shadow-lg shadow-red-500/30 hover:shadow-red-500/50 transition-all duration-300 hover:scale-[1.02] active:scale-[0.98]"
                  >
                    确认取消
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Teleport>

      <Teleport to="body">
        <div v-if="isReviewConfirmDialogOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div class="bg-white dark:bg-slate-800 rounded-lg shadow-lg max-w-md w-full mx-4">
            <div class="p-6">
              <h2 class="text-xl font-bold mb-2">确认提交评价</h2>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">确定要提交您的评价吗？</p>
              <div class="flex justify-end gap-3 mt-6">
                <Button
                  variant="outline"
                  @click="isReviewConfirmDialogOpen = false"
                >
                  取消
                </Button>
                <Button
                  @click="handleReviewConfirm"
                  class="bg-blue-600 hover:bg-blue-700 text-white"
                >
                  确定
                </Button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="isAgentDialogOpen" class="fixed inset-0 z-[9999] flex items-center justify-center" @click="isAgentDialogOpen = false; tempSelectedAgent = selectedAgent; agentSearchQuery = ''">
          <div class="absolute inset-0 bg-black/20" @click="isAgentDialogOpen = false; tempSelectedAgent = selectedAgent; agentSearchQuery = ''"></div>
          <div class="relative z-[10000] w-full max-w-md bg-white dark:bg-slate-800 rounded-2xl shadow-[0_0_40px_rgba(139,92,246,0.3)] border border-purple-200 dark:border-purple-800 animate-scale-in" @click.stop>
            <div class="p-6 pb-4">
                <div class="flex items-center gap-3 mb-1">
                  <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center shadow-lg shadow-purple-500/25">
                    <Bot class="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h2 class="text-lg font-bold text-slate-800 dark:text-white">智能体列表</h2>
                  </div>
                </div>
                <p class="text-sm text-slate-500 dark:text-slate-400">请选择您要使用的智能体类型</p>
              </div>
              
              <div class="px-3 pb-3 max-h-[50vh] sm:max-h-[320px] overflow-y-auto custom-scrollbar">
                <div class="space-y-2 px-3">
                  <button
                    v-for="(agent) in filteredAgents"
                    :key="agent.id"
                    @click="tempSelectedAgent = agent.id"
                    class="w-full group relative p-3 rounded-xl transition-all duration-300"
                    :class="tempSelectedAgent === agent.id 
                      ? 'bg-gradient-to-r from-purple-500/15 to-blue-500/15 dark:from-purple-500/10 dark:to-blue-500/10 border-2 border-purple-500 dark:border-purple-400 shadow-lg shadow-purple-500/10' 
                      : 'hover:bg-slate-100 dark:hover:bg-slate-700 border-2 border-transparent'"
                  >
                    <div class="flex items-center gap-3">
                      <div 
                        class="relative w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300"
                        :class="tempSelectedAgent === agent.id 
                          ? 'bg-gradient-to-br from-purple-500 to-blue-500 shadow-lg shadow-purple-500/30' 
                          : 'bg-gradient-to-br from-slate-100 to-slate-50 dark:from-slate-700 dark:to-slate-800 group-hover:from-purple-100 group-hover:to-blue-100 dark:group-hover:from-slate-600 dark:group-hover:to-slate-700'"
                      >
                        <Bot :class="`w-6 h-6 ${tempSelectedAgent === agent.id ? 'text-white' : 'text-slate-600 dark:text-slate-300'}`" />
                      </div>
                      <div class="flex-1 text-left min-w-0">
                        <h3 
                          class="font-semibold truncate transition-colors text-base"
                          :class="tempSelectedAgent === agent.id 
                            ? 'text-purple-700 dark:text-purple-300' 
                            : 'text-slate-700 dark:text-slate-200'"
                        >
                          {{ agent.name }}
                        </h3>
                      </div>
                      <div 
                        class="w-6 h-6 rounded-full flex items-center justify-center transition-all duration-300"
                        :class="tempSelectedAgent === agent.id 
                          ? 'bg-gradient-to-r from-purple-500 to-blue-500 scale-100' 
                          : 'scale-0 opacity-0'"
                      >
                        <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                    </div>
                  </button>
                </div>
              </div>
              
              <div class="p-4 mt-2 border-t border-slate-200 dark:border-slate-700">
                <div class="flex justify-end gap-3">
                  <button
                    @click="isAgentDialogOpen = false; tempSelectedAgent = selectedAgent; agentSearchQuery = ''"
                    class="px-5 py-2.5 rounded-xl text-sm font-medium text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 transition-all duration-200"
                  >
                    取消
                  </button>
                  <button
                    @click="handleAgentConfirm"
                    class="px-6 py-2.5 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 shadow-lg shadow-purple-500/25 hover:shadow-purple-500/40 transition-all duration-300 hover:scale-105 active:scale-95"
                  >
                    确认选择
                  </button>
                </div>
              </div>
          </div>
        </div>
      </Teleport>
    </div>

    <!-- Tool Hover Tooltip -->
    <Teleport to="body">
      <Transition name="tooltip">
        <div
          v-if="hoveredToolId"
          class="fixed z-[9999] pointer-events-none"
          :style="{ left: `${hoveredToolPosition.x}px`, top: `${hoveredToolPosition.y}px`, transform: 'translateY(-50%)' }"
        >
          <div :class="`relative px-4 py-3 rounded-2xl shadow-2xl text-sm max-w-[260px] border ${isDark ? 'bg-gradient-to-br from-slate-800 to-slate-900 border-cyan-500/30 text-gray-100' : 'bg-gradient-to-br from-white to-slate-50 border-cyan-400/40 text-gray-800'} backdrop-blur-md`">
            <p class="leading-relaxed whitespace-normal">{{ hoveredToolDescription }}</p>
            <div :class="`absolute top-1/2 -translate-y-1/2 -left-[14px] w-0 h-0 border-t-[11px] border-b-[11px] border-r-[14px] ${isDark ? 'border-r-cyan-500/30' : 'border-r-cyan-400/40'} border-t-transparent border-b-transparent`"></div>
            <div :class="`absolute top-1/2 -translate-y-1/2 -left-[12px] w-0 h-0 border-t-[10px] border-b-[10px] border-r-[12px] ${isDark ? 'border-r-slate-800' : 'border-r-white'} border-t-transparent border-b-transparent`"></div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Document Hover Tooltip -->
    <Teleport to="body">
      <Transition name="tooltip">
        <div
          v-if="hoveredDocId"
          class="fixed z-[9999] pointer-events-none"
          :style="{ left: `${hoveredDocPosition.x}px`, top: `${hoveredDocPosition.y}px`, transform: 'translate(-50%, -100%)' }"
        >
          <div :class="`relative px-4 py-3 rounded-2xl shadow-2xl text-sm max-w-[260px] border ${isDark ? 'bg-gradient-to-br from-slate-800 to-slate-900 border-cyan-500/30 text-gray-100' : 'bg-gradient-to-br from-white to-slate-50 border-cyan-400/40 text-gray-800'} backdrop-blur-md`">
            <p class="leading-relaxed whitespace-normal text-center">{{ hoveredDocDescription }}</p>
            <div :class="`absolute top-full left-1/2 -translate-x-1/2 -mt-[2px] w-0 h-0 border-l-[11px] border-r-[11px] border-t-[11px] border-l-transparent border-r-transparent ${isDark ? 'border-t-cyan-500/30' : 'border-t-cyan-400/40'}`"></div>
            <div :class="`absolute top-full left-1/2 -translate-x-1/2 w-0 h-0 border-l-[10px] border-r-[10px] border-t-[10px] border-l-transparent border-r-transparent ${isDark ? 'border-t-slate-800' : 'border-t-white'}`"></div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Toast Notification -->
    <Transition name="toast">
      <div
        v-if="showToast"
        class="fixed top-8 left-1/2 transform -translate-x-1/2 z-[1000]"
      >
        <p 
          class="text-base font-medium"
          :class="toastType === 'success' ? 'text-green-600' : 'text-red-600'"
        >{{ toastMessage }}</p>
      </div>
    </Transition>
  </div>
</template>

<style>
/* Tooltip animation */
.tooltip-enter-active {
  animation: tooltipFadeIn 0.2s ease-out;
}

.tooltip-leave-active {
  animation: tooltipFadeOut 0.15s ease-in;
}

@keyframes tooltipFadeIn {
  0% {
    opacity: 0;
    transform: translateY(-50%) translateX(-8px);
  }
  100% {
    opacity: 1;
    transform: translateY(-50%) translateX(0);
  }
}

@keyframes tooltipFadeOut {
  0% {
    opacity: 1;
    transform: translateY(-50%) translateX(0);
  }
  100% {
    opacity: 0;
    transform: translateY(-50%) translateX(-8px);
  }
}

/* Toast enter animation */
.toast-enter-active {
  animation: toastSlideIn 0.3s ease-out;
}

.toast-leave-active {
  animation: toastSlideOut 0.3s ease-in;
}

@keyframes toastSlideIn {
  0% {
    opacity: 0;
    transform: translate(-50%, -100%);
  }
  100% {
    opacity: 1;
    transform: translate(-50%, 0);
  }
}

@keyframes toastSlideOut {
  0% {
    opacity: 1;
    transform: translate(-50%, 0);
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -100%);
  }
}
</style>
