import { post } from '@/lib/api';

export interface VerifyCodeRequest {
  invite_code: string;
}

export interface VerifyCodeResponse {
  is_authorized: boolean;
  expire_time?: string;
  auth_location?: string;
  description?: string;
}

export interface RevokeResponse {
  is_authorized: boolean;
}

export async function verifyInviteCode(inviteCode: string): Promise<{ data?: VerifyCodeResponse; error?: string; code?: number }> {
  const response = await post<{ code: number; message: string; data: VerifyCodeResponse }>(
    '/api/auth/verify',
    { invite_code: inviteCode }
  );
  
  if (response.code !== 200) {
    return { error: response.message, code: response.code };
  }
  
  return { data: response.data };
}

export async function revokeAuthorization(): Promise<RevokeResponse> {
  const response = await post<{ code: number; message: string; data: RevokeResponse }>(
    '/api/auth/revoke'
  );
  
  if (response.code !== 200) {
    throw new Error(response.message);
  }
  
  return response.data;
}
