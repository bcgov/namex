<template>
  <div
    v-if="conditions.length > 0"
    class="rounded border border-gray-400 bg-sky-100 p-2 text-xs"
  >
    <p v-for="condition in conditions">
      <b>{{ condition.phrase }} &ndash;</b>
      {{ condition.text }}
    </p>
  </div>
</template>

<script setup lang="ts">
/** Component that lists conditions in a small banner */
import type { Condition } from '~/types'

defineProps<{
  conditions: Array<Condition>
}>()
</script>
