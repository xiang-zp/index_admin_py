<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  class?: string
}>()

const badgeClass = computed(() => {
  return ['inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2', props.class].join(' ')
})
</script>

<template>
  <div :class="badgeClass">
    <slot />
  </div>
</template>
