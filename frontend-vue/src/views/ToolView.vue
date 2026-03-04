<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Button from '@/components/ui/Button.vue';
import Card from '@/components/ui/Card.vue';
import CardHeader from '@/components/ui/CardHeader.vue';
import CardTitle from '@/components/ui/CardTitle.vue';
import CardDescription from '@/components/ui/CardDescription.vue';
import CardContent from '@/components/ui/CardContent.vue';
import Textarea from '@/components/ui/Textarea.vue';
import { ArrowLeft, Upload, FileText, Sparkles } from 'lucide-vue-next';

interface ToolConfig {
  name: string;
  description: string;
  icon: any;
  features: string[];
}

const toolConfig: Record<string, ToolConfig> = {
  'smart-assistant': {
    name: '智能助手',
    description: 'AI驱动的对话助手',
    icon: Sparkles,
    features: ['智能对话', '多轮交互', '知识问答', '任务协助']
  },
  'doc-analysis': {
    name: '文档分析',
    description: '快速解析文档内容',
    icon: FileText,
    features: ['文档上传', '智能解析', '内容提取', '摘要生成']
  },
  'content-creation': {
    name: '内容创作',
    description: 'AI辅助内容生成',
    icon: Sparkles,
    features: ['文案生成', '文章创作', '营销文案', '社交媒体']
  },
  'code-assistant': {
    name: '代码助手',
    description: '编程问题解决方案',
    icon: Sparkles,
    features: ['代码生成', '代码审查', '错误修复', '优化建议']
  },
  'data-analysis': {
    name: '数据分析',
    description: '数据洞察与可视化',
    icon: Sparkles,
    features: ['数据导入', '智能分析', '可视化展示', '报告生成']
  },
  'language-translation': {
    name: '语言翻译',
    description: '多语言实时翻译',
    icon: Sparkles,
    features: ['多语言支持', '实时翻译', '批量翻译', '语音翻译']
  },
  'mind-map': {
    name: '思维导图',
    description: '知识结构可视化',
    icon: Sparkles,
    features: ['思维导图', '知识结构', '可视化编辑', '导出分享']
  },
  'qa-system': {
    name: '问答系统',
    description: '智能问答与解答',
    icon: Sparkles,
    features: ['智能问答', '知识库检索', '多轮对话', '答案溯源']
  }
};

const route = useRoute();
const router = useRouter();

const tool = computed(() => toolConfig[route.params.tool as string]);
const input = ref('');
const result = ref('');
const isProcessing = ref(false);

const Icon = computed(() => tool.value?.icon || Sparkles);

const handleProcess = () => {
  if (!input.value.trim()) return;
  isProcessing.value = true;

  setTimeout(() => {
    result.value = `这是${tool.value?.name}的处理结果：\n\n您输入的内容是："${input.value}"\n\n经过AI处理后，我们为您生成了以下内容...\n\n（此处将显示实际的工具处理结果）`;
    isProcessing.value = false;
  }, 2000);
};

const goBack = () => {
  router.push('/');
};
</script>

<template>
  <div v-if="!tool" class="min-h-screen bg-gray-50 flex items-center justify-center">
    <Card class="max-w-md">
      <CardHeader>
        <CardTitle>工具不存在</CardTitle>
      </CardHeader>
      <CardContent>
        <Button @click="goBack">返回首页</Button>
      </CardContent>
    </Card>
  </div>

  <div v-else class="min-h-screen bg-gray-50">
    <header class="bg-white border-b border-gray-200 px-8 py-4">
      <div class="mx-auto max-w-6xl flex items-center justify-between">
        <Button variant="ghost" size="sm" @click="goBack">
          <ArrowLeft class="h-4 w-4 mr-2" />
          返回首页
        </Button>
        <div class="flex items-center space-x-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-100">
            <component :is="Icon" class="h-6 w-6 text-blue-600" />
          </div>
          <div>
            <h1 class="text-xl font-bold text-gray-900">{{ tool.name }}</h1>
            <p class="text-sm text-gray-600">{{ tool.description }}</p>
          </div>
        </div>
      </div>
    </header>

    <main class="mx-auto max-w-6xl px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>输入内容</CardTitle>
              <CardDescription>
                请输入您需要{{ tool.name }}处理的内容
              </CardDescription>
            </CardHeader>
            <CardContent class="space-y-4">
              <div v-if="route.params.tool === 'doc-analysis'" class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition-colors cursor-pointer">
                <Upload class="h-12 w-12 mx-auto text-gray-400 mb-4" />
                <p class="text-sm text-gray-600 mb-2">点击或拖拽上传文档</p>
                <p class="text-xs text-gray-400">支持 PDF、Word、TXT 等格式</p>
              </div>

              <Textarea
                placeholder="请输入您的需求或内容..."
                v-model="input"
                class="min-h-[200px]"
                :disabled="isProcessing"
              />

              <Button
                @click="handleProcess"
                :disabled="!input.trim() || isProcessing"
                class="w-full bg-blue-600 hover:bg-blue-700 text-white"
              >
                {{ isProcessing ? '处理中...' : `使用${tool.name}` }}
              </Button>
            </CardContent>
          </Card>

          <Card v-if="result">
            <CardHeader>
              <CardTitle>处理结果</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="bg-gray-50 rounded-lg p-4">
                <pre class="whitespace-pre-wrap text-sm text-gray-700">{{ result }}</pre>
              </div>
            </CardContent>
          </Card>
        </div>

        <div class="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>功能特性</CardTitle>
            </CardHeader>
            <CardContent>
              <ul class="space-y-3">
                <li v-for="(feature, index) in tool.features" :key="index" class="flex items-center text-sm">
                  <div class="h-2 w-2 rounded-full bg-blue-600 mr-3" />
                  {{ feature }}
                </li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>使用提示</CardTitle>
            </CardHeader>
            <CardContent>
              <p class="text-sm text-gray-600 leading-relaxed">
                使用{{ tool.name }}时，请提供清晰明确的输入内容，这将有助于AI更准确地理解您的需求并提供更好的结果。
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  </div>
</template>
