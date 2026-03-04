import { ref } from 'vue'

export type ToastType = 'success' | 'error' | 'info'

export interface ToastItem {
  id: string
  type: ToastType
  message: string
  durationMs: number
}

export const toasts = ref<ToastItem[]>([])

const removeToast = (id: string) => {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

export const toast = {
  show(message: string, type: ToastType = 'info', durationMs = 2200) {
    const id = `${Date.now()}-${Math.random().toString(16).slice(2)}`
    toasts.value = [...toasts.value, { id, type, message, durationMs }]
    window.setTimeout(() => removeToast(id), durationMs)
  },
  success(message: string, durationMs = 2200) {
    toast.show(message, 'success', durationMs)
  },
  error(message: string, durationMs = 2600) {
    toast.show(message, 'error', durationMs)
  },
  info(message: string, durationMs = 2200) {
    toast.show(message, 'info', durationMs)
  }
}

