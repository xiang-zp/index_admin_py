import { get } from '@/lib/api';

export interface Tool {
  id: string;
  name: string;
  description: string;
  path: string | null;
  icon: string | null;
  image: string | null;
  row?: string;
  is_visible: boolean;
  is_active: boolean;
  sort_order: number;
  created_at: string | null;
  updated_at: string | null;
}

export async function getTools(): Promise<Tool[]> {
  return get<Tool[]>('/api/tools/');
}
