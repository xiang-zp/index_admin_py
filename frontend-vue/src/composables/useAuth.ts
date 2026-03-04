import { ref } from 'vue';
import * as auth from '@/services/auth';

const AUTH_KEY = 'auth_info';
const AUTH_EXPIRE_DAYS = 7;

interface AuthInfo {
  inviteCode: string;
  authLocation: string;
  expireTime: string | null;
  authorizedAt: number;
}

function getStoredAuth(): AuthInfo | null {
  if (typeof window === 'undefined') return null;
  
  const stored = localStorage.getItem(AUTH_KEY);
  if (!stored) return null;
  
  try {
    const authInfo: AuthInfo = JSON.parse(stored);
    const now = Date.now();
    const expireMs = AUTH_EXPIRE_DAYS * 24 * 60 * 60 * 1000;
    
    if (now - authInfo.authorizedAt > expireMs) {
      localStorage.removeItem(AUTH_KEY);
      return null;
    }
    
    return authInfo;
  } catch {
    return null;
  }
}

export function useAuth() {
  const isAuthorized = ref(false);
  const authLocation = ref<string>('global');
  const inviteCode = ref<string>('');
  const errorMessage = ref<string>('');

  const initAuth = () => {
    const stored = getStoredAuth();
    if (stored) {
      isAuthorized.value = true;
      authLocation.value = stored.authLocation || 'global';
      inviteCode.value = stored.inviteCode;
    }
  };

  initAuth();

  const verifyInviteCode = async (code: string) => {
    errorMessage.value = '';
    
    try {
      const result = await auth.verifyInviteCode(code);
      
      if (result.error) {
        const errorMsg = `您输入的「${code}」${result.error}，请重新输入！`;
        errorMessage.value = errorMsg;
        return { success: false, message: errorMsg };
      }
      
      if (result.data?.is_authorized) {
        isAuthorized.value = true;
        authLocation.value = result.data.auth_location || 'global';
        inviteCode.value = code;
        
        const authInfo: AuthInfo = {
          inviteCode: code,
          authLocation: result.data.auth_location || 'global',
          expireTime: result.data.expire_time || null,
          authorizedAt: Date.now()
        };
        localStorage.setItem(AUTH_KEY, JSON.stringify(authInfo));
        
        return { success: true };
      }
      
      const defaultErrorMsg = '您输入的「' + code + '」授权验证失败，请重新输入！';
      errorMessage.value = defaultErrorMsg;
      return { success: false, message: defaultErrorMsg };
    } catch (error) {
      const errorMsg = '服务异常，请刷新页面重试！';
      errorMessage.value = errorMsg;
      return { success: false, message: errorMsg };
    }
  };

  const revokeAuthorization = async () => {
    try {
      await auth.revokeAuthorization();
      isAuthorized.value = false;
      authLocation.value = 'global';
      inviteCode.value = '';
      localStorage.removeItem(AUTH_KEY);
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        message: error instanceof Error ? error.message : '取消授权失败' 
      };
    }
  };

  const hasPermission = (requiredLocation: string): boolean => {
    if (!isAuthorized.value) return false;
    if (authLocation.value === 'global') return true;
    return authLocation.value === requiredLocation;
  };

  const checkPermission = (requiredLocation: string): { hasPermission: boolean; message?: string } => {
    if (!isAuthorized.value) {
      return { 
        hasPermission: false, 
        message: '请先输入授权码进行授权！' 
      };
    }
    
    if (authLocation.value !== 'global' && authLocation.value !== requiredLocation) {
      const locationNames: Record<string, string> = {
        'agents': '智能体',
        'tools': '开源项目',
        'documents': '文档资料'
      };
      return { 
        hasPermission: false, 
        message: `当前授权码暂无查看${locationNames[requiredLocation] || requiredLocation}权限，请更换授权码！` 
      };
    }
    
    return { hasPermission: true };
  };

  return {
    isAuthorized,
    authLocation,
    inviteCode,
    errorMessage,
    verifyInviteCode,
    revokeAuthorization,
    hasPermission,
    checkPermission,
  };
}
