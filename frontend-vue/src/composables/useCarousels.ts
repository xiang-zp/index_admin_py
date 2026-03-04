import { ref } from 'vue';
import * as carousels from '@/services/carousels';

export function useCarousels() {
  const messages = ref<string[]>([]);
  const loading = ref(true);
  const error = ref<string | null>(null);
  const isError = ref(false);

  const loadData = async () => {
    try {
      loading.value = true;
      const data = await carousels.getCarousels();
      if (data && data.length > 0) {
        messages.value = data;
        isError.value = false;
      } else {
        messages.value = ['获取轮播文案失败，请刷新页面！'];
        isError.value = true;
      }
      error.value = null;
    } catch (err) {
      error.value = err instanceof Error ? err.message : '加载失败';
      messages.value = ['获取轮播文案失败，请刷新页面！'];
      isError.value = true;
    } finally {
      loading.value = false;
    }
  };

  loadData();

  return { messages, loading, error, isError };
}
