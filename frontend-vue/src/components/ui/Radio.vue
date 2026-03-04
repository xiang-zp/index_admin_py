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
  change: [event: Event];
}>();

const radioClass = computed(() =>
  cn(
    'aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
    props.class
  )
);
</script>

<template>
  <input
    type="radio"
    :class="radioClass"
    :checked="modelValue"
    :disabled="disabled"
    @change="emit('update:modelValue', ($event.target as HTMLInputElement).value); emit('change', $event)"
  />
</template>
