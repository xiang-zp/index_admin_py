<script setup lang="ts">
import { computed } from 'vue'
import { toasts } from '@/lib/toast'

const toastItems = computed(() => toasts.value)

const typeClass = (type: 'success' | 'error' | 'info') => {
  if (type === 'success') return 'border-emerald-200 bg-emerald-50 text-emerald-800'
  if (type === 'error') return 'border-red-200 bg-red-50 text-red-800'
  return 'border-gray-200 bg-white text-gray-800'
}
</script>

<template>
  <Teleport to="body">
    <div class="fixed top-8 left-1/2 -translate-x-1/2 z-[9999] space-y-3">
      <TransitionGroup name="toast" tag="div" class="space-y-3">
        <div
          v-for="t in toastItems"
          :key="t.id"
          :class="[
            'min-w-[220px] max-w-[360px] px-4 py-3 rounded-lg border shadow-lg backdrop-blur-sm',
            typeClass(t.type)
          ]"
        >
          <p class="text-sm font-medium leading-5 break-words">{{ t.message }}</p>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.18s ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>

