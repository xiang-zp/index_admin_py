<script setup lang="ts">
import { computed } from 'vue';
import { cn } from '@/lib/utils';

interface Props {
  class?: string;
  modelValue?: number;
  min?: number;
  max?: number;
  step?: number;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  min: 0,
  max: 100,
  step: 1,
  disabled: false,
});

const emit = defineEmits<{
  'update:modelValue': [value: number];
  input: [event: Event];
  change: [event: Event];
}>();

const sliderClass = computed(() =>
  cn(
    'relative flex w-full touch-none select-none items-center',
    props.class
  )
);

const inputClass = computed(() =>
  cn(
    'relative h-1.5 w-full appearance-none rounded-full bg-primary/20 outline-none cursor-pointer disabled:cursor-not-allowed disabled:opacity-50',
    '[&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary [&::-webkit-slider-thumb]:shadow-sm [&::-webkit-slider-thumb]:transition-all [&::-webkit-slider-thumb]:hover:scale-110',
    '[&::-moz-range-thumb]:appearance-none [&::-moz-range-thumb]:h-4 [&::-moz-range-thumb]:w-4 [&::-moz-range-thumb]:rounded-full [&::-moz-range-thumb]:bg-primary [&::-moz-range-thumb]:shadow-sm [&::-moz-range-thumb]:transition-all [&::-moz-range-thumb]:hover:scale-110'
  )
);
</script>

<template>
  <div :class="sliderClass">
    <input
      type="range"
      :class="inputClass"
      :min="min"
      :max="max"
      :step="step"
      :disabled="disabled"
      :value="modelValue"
      @input="emit('update:modelValue', Number(($event.target as HTMLInputElement).value)); emit('input', $event)"
      @change="emit('change', $event)"
    />
  </div>
</template>
