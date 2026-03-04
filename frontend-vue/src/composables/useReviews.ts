import { ref, onMounted } from 'vue';
import * as reviews from '@/services/reviews';

const generateAvatar = (name: string): string => {
  return name.slice(0, 2).toUpperCase();
};

const formatDate = (dateStr: string | null): string => {
  if (!dateStr) {
    const now = new Date();
    return `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日`;
  }
  const date = new Date(dateStr);
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
};

export function useReviews() {
  const reviewsList = ref<reviews.Review[]>([]);
  const loading = ref(true);
  const error = ref<string | null>(null);

  const submitReview = async (data: reviews.ReviewCreateRequest) => {
    try {
      const newReview = await reviews.createReview(data);
      console.log('submitReview success:', newReview);
      const reviewWithDisplay: reviews.Review = {
        ...newReview,
        avatar: generateAvatar(newReview.name),
        date: formatDate(newReview.created_at)
      };
      reviewsList.value = [reviewWithDisplay, ...reviewsList.value];
      return { success: true };
    } catch (error) {
      console.error('submitReview error:', error);
      return { 
        success: false, 
        message: error instanceof Error ? error.message : '提交失败' 
      };
    }
  };

  const refreshReviews = async () => {
    try {
      loading.value = true;
      const data = await reviews.getReviews();
      console.log('refreshReviews data:', data);
      reviewsList.value = (data.list || []).map(r => ({
        ...r,
        avatar: generateAvatar(r.name),
        date: formatDate(r.created_at)
      }));
      console.log('refreshReviews updated list:', reviewsList.value);
      error.value = null;
    } catch (err) {
      console.error('refreshReviews error:', err);
      error.value = err instanceof Error ? err.message : '加载失败';
      reviewsList.value = [];
    } finally {
      loading.value = false;
    }
  };

  onMounted(async () => {
    await refreshReviews();
  });

  return { reviews: reviewsList, submitReview, loading, error, refreshReviews };
}
