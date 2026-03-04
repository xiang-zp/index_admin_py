<script setup lang="ts">
import { computed } from 'vue';
import { cn } from '@/lib/utils';

interface Props {
  class?: string;
  placeholder?: string;
  disabled?: boolean;
  modelValue?: string;
  rows?: number;
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
  rows: 3,
});

const emit = defineEmits<{
  'update:modelValue': [value: string];
  input: [event: Event];
  focus: [event: FocusEvent];
  blur: [event: FocusEvent];
}>();

const textareaClass = computed(() =>
  cn(
    'flex min-h-[60px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-base shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 md:text-sm',
    props.class
  )
);
</script>

<template>
  <textarea
    :class="textareaClass"
    :placeholder="placeholder"
    :disabled="disabled"
    :value="modelValue"
    :rows="rows"
    @input="emit('update:modelValue', ($event.target as HTMLTextAreaElement).value); emit('input', $event)"
    @focus="emit('focus', $event)"
    @blur="emit('blur', $event)"
  />
</template>
