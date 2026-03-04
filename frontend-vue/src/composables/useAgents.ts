import { ref, onMounted } from 'vue';
import * as chat from '@/services/chat';

const STORAGE_KEY = 'selectedAgentId';

export function useAgents() {
  const agents = ref<chat.Agent[]>([]);
  const selectedAgent = ref('');
  const loading = ref(true);
  const error = ref<string | null>(null);

  const loadData = async () => {
    try {
      loading.value = true;
      const data = await chat.getAgents();
      agents.value = data;
      error.value = null;

      const cached = localStorage.getItem(STORAGE_KEY);
      if (cached && data.some(a => a.id === cached)) {
        selectedAgent.value = cached;
      } else if (data.length > 0) {
        selectedAgent.value = data[0]!.id;
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : '加载失败';
      agents.value = [];
    } finally {
      loading.value = false;
    }
  };

  const setSelectedAgent = (id: string) => {
    selectedAgent.value = id;
    localStorage.setItem(STORAGE_KEY, id);
  };

  onMounted(() => {
    loadData();
  });

  return { agents, selectedAgent, setSelectedAgent, loading, error, loadData };
}
