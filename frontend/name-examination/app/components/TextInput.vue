<template>
  <input
    type="text"
    class="w-full rounded border border-gray-300 px-2 py-1.5"
    :class="{ 'border-2 border-red-600 outline-red-600': errorStyle }"
    :value="modelValue"
    @input="
      $emit('update:modelValue', ($event.target as HTMLInputElement).value)
    "
  />
</template>

<script setup lang="ts">
/** Generic input component for inputting single-line text. */
defineProps<{
  /** Text input's string value */
  modelValue?: string
  /** Style this input as an error, useful to indicate invalid inputs */
  errorStyle?: boolean
}>()
</script>
