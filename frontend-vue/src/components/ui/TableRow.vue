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

const tableRowClass = computed(() =>
  cn(
    'border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted',
    props.class
  )
);
</script>

<template>
  <tr :class="tableRowClass">
    <slot />
  </tr>
</template>
