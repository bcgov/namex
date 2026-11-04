<template>
  <input
    :value="modelValue"
    @change="(e: Event) => $emit('update:modelValue', (e.target as HTMLInputElement).value)"
    type="date"
    class="rounded border border-gray-300 px-3 py-1"
    :class="{ 'border-2 border-red-600': errorStyle }"
    :min="minToday ? today : undefined"
  />
</template>

<script setup lang="ts">
/** An input for selecting dates */
import { DateTime } from 'luxon'

defineProps<{
  modelValue: any
  /** Set the minimum possible date value to today */
  minToday?: boolean
  /** Style this input to show an error */
  errorStyle?: boolean
}>()

const today = computed(() => DateTime.now().toFormat('yyyy-MM-dd'))
</script>
