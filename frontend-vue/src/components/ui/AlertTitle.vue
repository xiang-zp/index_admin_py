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

const alertTitleClass = computed(() =>
  cn(
    'mb-1 font-medium leading-none tracking-tight',
    props.class
  )
);
</script>

<template>
  <h5 :class="alertTitleClass">
    <slot />
  </h5>
</template>
