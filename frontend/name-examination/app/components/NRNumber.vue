<template>
  <span class="text-3xl font-bold" :class="{ 'text-red-600': priority }">
    {{ nrNumber }}
  </span>
</template>

<script setup lang="ts">
/** Displays a given NR number */
defineProps<{
  nrNumber: string
  /** Whether the NR is a priority or not */
  priority?: boolean
}>()
</script>
