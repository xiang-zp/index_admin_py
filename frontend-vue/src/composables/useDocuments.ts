import { ref, onMounted, watch } from 'vue';
import * as documents from '@/services/documents';

export function useDocuments(category?: string) {
  const documentsList = ref<documents.Document[]>([]);
  const categories = ref<documents.Category[]>([]);
  const loading = ref(true);
  const error = ref<string | null>(null);

  const loadData = async () => {
    try {
      loading.value = true;
      const [documentsData, categoriesData] = await Promise.all([
        documents.getDocuments({ category, page: 1, page_size: 100 }),
        documents.getDocumentCategories()
      ]);
      documentsList.value = documentsData.items;
      categories.value = categoriesData;
      error.value = null;
    } catch (err) {
      error.value = err instanceof Error ? err.message : '加载失败';
      documentsList.value = [];
      categories.value = [];
    } finally {
      loading.value = false;
    }
  };

  onMounted(() => {
    loadData();
  });

  if (category) {
    watch(() => category, () => {
      loadData();
    }, { immediate: true });
  }

  return { documents: documentsList, categories, loading, error };
}