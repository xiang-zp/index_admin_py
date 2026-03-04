<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  class?: string
}>()

const cardClass = computed(() => {
  return ['rounded-lg border bg-card text-card-foreground shadow-sm', props.class].join(' ')
})
</script>

<template>
  <div :class="cardClass">
    <slot />
  </div>
</template>
