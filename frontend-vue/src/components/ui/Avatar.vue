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

const avatarClass = computed(() =>
  cn(
    'relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full',
    props.class
  )
);
</script>

<template>
  <div :class="avatarClass">
    <slot />
  </div>
</template>
