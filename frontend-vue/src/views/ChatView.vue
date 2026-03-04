<script setup lang="ts">
import { ref, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import Button from '@/components/ui/Button.vue';
import Input from '@/components/ui/Input.vue';
import Card from '@/components/ui/Card.vue';
import { Send, ArrowLeft, Bot, User } from 'lucide-vue-next';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const router = useRouter();

const messages = ref<Message[]>([
  {
    id: '1',
    role: 'assistant',
    content: '您好！我是智能搜索助手。请问有什么我可以帮助您的？',
    timestamp: new Date()
  }
]);
const input = ref('');
const isLoading = ref(false);
const messagesEndRef = ref<HTMLDivElement | null>(null);

const scrollToBottom = () => {
  nextTick(() => {
    messagesEndRef.value?.scrollIntoView({ behavior: 'smooth' });
  });
};

watch(messages, () => {
  scrollToBottom();
}, { deep: true });

const handleSend = async () => {
  if (!input.value.trim()) return;

  const userMessage: Message = {
    id: Date.now().toString(),
    role: 'user',
    content: input.value,
    timestamp: new Date()
  };

  messages.value = [...messages.value, userMessage];
  input.value = '';
  isLoading.value = true;

  setTimeout(() => {
    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: `我理解您的问题是："${userMessage.content}"。\n\n这是一个很好的问题。让我来为您详细解答：\n\n根据我的知识库，我可以为您提供以下信息...\n\n如果您需要更详细的解释或者有其他问题，请随时告诉我！`,
      timestamp: new Date()
    };
    messages.value = [...messages.value, assistantMessage];
    isLoading.value = false;
  }, 1500);
};

const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !isLoading.value) {
    handleSend();
  }
};

const goBack = () => {
  router.push('/');
};
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <header class="bg-white border-b border-gray-200 px-8 py-4">
      <div class="mx-auto max-w-4xl flex items-center">
        <Button variant="ghost" size="sm" class="mr-4" @click="goBack">
          <ArrowLeft class="h-4 w-4 mr-2" />
          返回首页
        </Button>
        <h1 class="text-xl font-bold text-gray-900">智能搜索助手</h1>
      </div>
    </header>

    <main class="flex-1 overflow-y-auto px-8 py-8">
      <div class="mx-auto max-w-4xl space-y-6">
        <div
          v-for="message in messages"
          :key="message.id"
          :class="['flex', message.role === 'user' ? 'justify-end' : 'justify-start']"
        >
          <div
            :class="['flex items-start gap-3 max-w-[80%]', message.role === 'user' ? 'flex-row-reverse' : 'flex-row']"
          >
            <div
              :class="['flex h-8 w-8 items-center justify-center rounded-full', message.role === 'user' ? 'bg-blue-600' : 'bg-green-600']"
            >
              <User v-if="message.role === 'user'" class="h-5 w-5 text-white" />
              <Bot v-else class="h-5 w-5 text-white" />
            </div>
            <Card
              :class="['p-4', message.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white']"
            >
              <p class="whitespace-pre-wrap text-sm leading-relaxed">
                {{ message.content }}
              </p>
              <p :class="['text-xs mt-2', message.role === 'user' ? 'text-blue-100' : 'text-gray-400']">
                {{ message.timestamp.toLocaleTimeString('zh-CN', {
                  hour: '2-digit',
                  minute: '2-digit'
                }) }}
              </p>
            </Card>
          </div>
        </div>

        <div v-if="isLoading" class="flex justify-start">
          <div class="flex items-start gap-3">
            <div class="flex h-8 w-8 items-center justify-center rounded-full bg-green-600">
              <Bot class="h-5 w-5 text-white" />
            </div>
            <Card class="p-4 bg-white">
              <div class="flex space-x-2">
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
              </div>
            </Card>
          </div>
        </div>
        <div ref="messagesEndRef" />
      </div>
    </main>

    <footer class="bg-white border-t border-gray-200 px-8 py-4">
      <div class="mx-auto max-w-4xl flex items-center space-x-2">
        <Input
          type="text"
          placeholder="请输入您的问题..."
          v-model="input"
          @keydown="handleKeyDown"
          :disabled="isLoading"
          class="flex-1"
        />
        <Button
          @click="handleSend"
          :disabled="!input.trim() || isLoading"
          class="bg-red-600 hover:bg-red-700 text-white"
        >
          <Send class="h-5 w-5" />
        </Button>
      </div>
    </footer>
  </div>
</template>
