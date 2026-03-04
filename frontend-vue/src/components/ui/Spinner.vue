<script setup lang="ts">
interface Props {
  class?: string;
}

const props = withDefaults(defineProps<Props>(), {});
</script>

<template>
  <div :class="['relative', props.class]">
    <div class="absolute inset-0 border-2 border-gray-300 dark:border-gray-600 border-t-gray-500 dark:border-t-gray-400 rounded-full animate-spin"></div>
    <div class="absolute inset-1 border-2 border-gray-400 dark:border-gray-500 border-b-gray-600 dark:border-b-gray-400 rounded-full animate-spin" style="animation-direction: reverse"></div>
  </div>
</template>
