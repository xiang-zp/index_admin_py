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

const emptyClass = computed(() =>
  cn(
    'flex min-h-[400px] flex-col items-center justify-center rounded-md border border-dashed p-8 text-center',
    props.class
  )
);
</script>

<template>
  <div :class="emptyClass">
    <slot />
  </div>
</template>
