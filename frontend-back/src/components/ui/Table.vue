<script setup lang="ts">
const props = defineProps<{
  class?: string
}>()
</script>

<template>
  <table :class="['w-full caption-bottom text-sm', props.class]">
    <slot />
  </table>
</template>
