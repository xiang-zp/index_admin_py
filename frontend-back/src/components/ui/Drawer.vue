<script setup lang="ts">
import { computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  open: boolean
  title?: string
  position?: 'left' | 'right'
  width?: string
}>()

const emit = defineEmits<{
  close: []
}>()

const drawerClass = computed(() => {
  const baseClass = 'fixed inset-y-0 z-50 bg-white shadow-2xl transform transition-transform duration-300 ease-in-out'
  
  if (props.position === 'left') {
    return `${baseClass} left-0 ${props.open ? 'translate-x-0' : '-translate-x-full'}`
  } else {
    return `${baseClass} right-0 ${props.open ? 'translate-x-0' : 'translate-x-full'}`
  }
})

const overlayClass = computed(() => {
  return [
    'fixed inset-0 bg-black/50 z-40 transition-opacity duration-300',
    props.open ? 'opacity-100' : 'opacity-0 pointer-events-none'
  ]
})

const handleOverlayClick = () => {
  emit('close')
}

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    emit('close')
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})

watch(() => props.open, (newVal) => {
  if (newVal) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})
</script>

<template>
  <Teleport to="body">
    <div v-if="open">
      <div 
        :class="overlayClass"
        @click="handleOverlayClick"
      />
      
      <aside :class="drawerClass" :style="{ width: width || '480px' }">
        <div class="flex flex-col h-full">
          <div class="flex items-center justify-between h-16 px-6 border-b">
            <h2 class="text-lg font-semibold text-gray-900">{{ title || '详情' }}</h2>
            <button 
              @click="emit('close')"
              class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <div class="flex-1 overflow-y-auto">
            <slot />
          </div>
        </div>
      </aside>
    </div>
  </Teleport>
</template>
