import { ref, onMounted } from 'vue';
import * as footer from '@/services/footer';

export function useFooter() {
  const config = ref<footer.FooterConfig>({
    logo_url: '',
    slogan: '',
    updated_at: null
  });
  const links = ref<footer.FooterLink[]>([]);
  const loading = ref(true);
  const error = ref<string | null>(null);

  const loadData = async () => {
    try {
      loading.value = true;
      error.value = null;

      const [configData, linksData] = await Promise.all([
        footer.getFooterConfig(),
        footer.getFooterLinks()
      ]);

      config.value = configData;
      links.value = linksData;
    } catch (err) {
      error.value = err instanceof Error ? err.message : '加载失败';
    } finally {
      loading.value = false;
    }
  };

  onMounted(() => {
    loadData();
  });

  return { config, links, loading, error, loadData };
}
