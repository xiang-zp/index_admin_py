import { get, post } from '@/lib/api';

export interface Review {
  id: string;
  name: string;
  avatar?: string;
  avatar_color: string;
  rating: number;
  date?: string;
  content: string;
  created_at: string | null;
}

export interface ReviewCreateRequest {
  name: string;
  rating: number;
  content: string;
}

export interface ReviewsResponse {
  list: Review[];
  total: number;
}

export async function getReviews(): Promise<ReviewsResponse> {
  return get<ReviewsResponse>('/api/reviews/');
}

export async function createReview(data: ReviewCreateRequest): Promise<Review> {
  return post<Review>('/api/reviews/', data);
}
