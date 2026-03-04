import { get } from '@/lib/api';

export interface Project {
  id: number;
  category: string;
  title: string;
  description: string;
  date: string;
  color: string;
}

export interface Category {
  id: string;
  name: string;
}

export interface ProjectsResponse {
  items: Project[];
}

export async function getProjects(params?: { category?: string }): Promise<ProjectsResponse> {
  const query = params?.category ? `?category=${params.category}` : '';
  return get<ProjectsResponse>(`/api/projects${query}`);
}

export async function getProjectCategories(): Promise<Category[]> {
  return get<Category[]>('/api/projects/categories');
}
