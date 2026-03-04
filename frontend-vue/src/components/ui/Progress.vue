<script setup lang="ts">
import { computed } from 'vue';
import { cn } from '@/lib/utils';

interface Props {
  class?: string;
  modelValue?: number;
  max?: number;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  max: 100,
  disabled: false,
});

const emit = defineEmits<{
  'update:modelValue': [value: number];
}>();

const progressClass = computed(() =>
  cn(
    'relative h-2 w-full overflow-hidden rounded-full bg-primary/20',
    props.class
  )
);

const indicatorClass = computed(() =>
  cn(
    'h-full w-full flex-1 bg-primary transition-all duration-300 ease-in-out',
    props.disabled && 'opacity-50'
  )
);

const percentage = computed(() => {
  if (props.max === 0) return 0;
  return Math.min(100, Math.max(0, ((props.modelValue || 0) / props.max) * 100));
});
</script>

<template>
  <div :class="progressClass" role="progressbar" :aria-valuenow="modelValue" :aria-valuemax="max">
    <div :class="indicatorClass" :style="{ width: `${percentage}%` }" />
  </div>
</template>
