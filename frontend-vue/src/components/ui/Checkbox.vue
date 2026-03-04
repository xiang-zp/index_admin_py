<script setup lang="ts">
import { computed } from 'vue';
import { cn } from '@/lib/utils';

interface Props {
  class?: string;
  modelValue?: boolean;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
});

const emit = defineEmits<{
  'update:modelValue': [value: boolean];
  change: [event: Event];
}>();

const checkboxClass = computed(() =>
  cn(
    'peer h-4 w-4 shrink-0 rounded-sm border border-primary ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground',
    props.class
  )
);
</script>

<template>
  <input
    type="checkbox"
    :class="checkboxClass"
    :checked="modelValue"
    :disabled="disabled"
    :data-state="modelValue ? 'checked' : 'unchecked'"
    @change="emit('update:modelValue', ($event.target as HTMLInputElement).checked); emit('change', $event)"
  />
</template>
