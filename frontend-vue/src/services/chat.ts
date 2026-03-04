import { get } from '@/lib/api';

export interface Agent {
  id: string;
  name: string;
  description: string;
}

export async function getAgents(): Promise<Agent[]> {
  return get<Agent[]>('/api/chat/agents');
}
