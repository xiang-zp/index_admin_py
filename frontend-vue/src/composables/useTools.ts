import { ref, onMounted } from 'vue';
import * as tools from '@/services/tools';

export function useTools() {
  const toolsList = ref<tools.Tool[]>([]);
  const loading = ref(true);
  const error = ref<string | null>(null);

  onMounted(async () => {
    try {
      loading.value = true;
      const data = await tools.getTools();
      toolsList.value = data;
      error.value = null;
    } catch (err) {
      error.value = err instanceof Error ? err.message : '加载失败';
      toolsList.value = [];
    } finally {
      loading.value = false;
    }
  });

  return { tools: toolsList, loading, error };
}
