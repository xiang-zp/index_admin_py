<script setup lang="ts">
const props = defineProps<{
  class?: string
}>()
</script>

<template>
  <div :class="['space-y-1.5 p-6', props.class]">
    <slot />
  </div>
</template>
