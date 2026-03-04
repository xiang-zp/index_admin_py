import { get } from '@/lib/api';

export interface FooterConfig {
  logo_url: string;
  slogan: string;
  updated_at: string | null;
}

export interface FooterLink {
  id: string;
  title: string;
  url: string;
  sort_order: number;
  created_at: string | null;
  updated_at: string | null;
}

export async function getFooterConfig(): Promise<FooterConfig> {
  return get<FooterConfig>('/api/footer/config');
}

export async function getFooterLinks(): Promise<FooterLink[]> {
  return get<FooterLink[]>('/api/footer/links');
}
