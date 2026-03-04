import { get } from '@/lib/api';

export async function getCarousels(): Promise<string[]> {
  return get<string[]>('/api/carousels/');
}
