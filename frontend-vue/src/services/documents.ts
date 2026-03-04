import { get } from '@/lib/api';

export interface Document {
  id: string;
  category: string;
  title: string;
  description: string;
  color: string;
  url?: string;
  row: string;
  is_visible: boolean;
  sort_order: number;
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: string;
  name: string;
  color: string;
  is_active: boolean;
  sort_order: number;
  created_at: string;
  updated_at: string;
}

export interface DocumentsResponse {
  items: Document[];
  total: number;
}

export async function getDocuments(params?: { category?: string; page?: number; page_size?: number }): Promise<DocumentsResponse> {
  const queryParams = new URLSearchParams();
  if (params?.category && params.category !== 'all') {
    queryParams.append('category', params.category);
  }
  if (params?.page) {
    queryParams.append('page', params.page.toString());
  }
  if (params?.page_size) {
    queryParams.append('page_size', params.page_size.toString());
  }
  
  const query = queryParams.toString() ? `?${queryParams.toString()}` : '';
  const response = await get<{ items: Document[]; total: number }>(`/api/documents/${query}`);
  
  return {
    items: response.items,
    total: response.total
  };
}

export async function getDocumentCategories(): Promise<Category[]> {
  return get<Category[]>('/api/documents/categories');
}