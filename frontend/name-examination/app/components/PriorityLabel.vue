<template>
  <div class="flex items-center font-bold text-red-600">
    <StarIcon :class="iconStyle ?? 'h-4 w-4'" />
    <p data-testid="priorityLabel">Priority</p>
  </div>
</template>

<script setup lang="ts">
/** Component usually used to indicate an NR is a priority. */
import { StarIcon } from '@heroicons/vue/24/solid'

defineProps<{
  /** Tailwind style string passed to the label's icon. */
  iconStyle?: string
}>()
</script>
