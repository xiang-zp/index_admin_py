<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  type?: string
  class?: string
}>()

const modelValue = defineModel<string | number>()

const inputClass = computed(() => {
  return [
    'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
    props.class
  ].join(' ')
})

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  modelValue.value = target.value
}
</script>

<template>
  <input 
    :type="type || 'text'"
    :value="modelValue"
    :class="inputClass"
    @input="handleInput"
  />
</template>
