<script setup lang="ts">
import { computed } from 'vue';
import { cn } from '@/lib/utils';

interface Props {
  class?: string;
  modelValue?: string;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
});

const emit = defineEmits<{
  'update:modelValue': [value: string];
  input: [event: Event];
  focus: [event: FocusEvent];
  blur: [event: FocusEvent];
}>();

const skeletonClass = computed(() =>
  cn(
    'animate-pulse rounded-md bg-primary/10',
    props.class
  )
);
</script>

<template>
  <div :class="skeletonClass" />
</template>
