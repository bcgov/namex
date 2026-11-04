<template>
  <div>
    <h3 class="font-semibold">Trademarks</h3>
    <ListSelect
      v-model="examine.selectedTrademarks"
      :options="examine.trademarks"
      options-style="!max-h-40"
      :options-display="displayTrademark"
      :disabled="examine.decisionSelectionsDisabled"
      multiple
      close-on-select
    >
      <Chips
        v-if="examine.selectedTrademarks.length > 0"
        :display="(trademark: Trademark) => trademark.name"
        v-model="examine.selectedTrademarks"
      />
    </ListSelect>
  </div>
</template>

<script setup lang="ts">
/** A dropdown for selecting trademarks */
import { useExamination } from '~/store/examine'
import type { Trademark } from '~/types'

const examine = useExamination()

const trademarkCounts = computed(() => {
  const counts: { [trademarkName: string]: number } = {}
  for (const trademark of examine.trademarks) {
    if (trademark.name in counts) {
      counts[trademark.name] += 1
    } else {
      counts[trademark.name] = 1
    }
  }
  return counts
})

/**
 * Get the display string for a trademark object.
 * If there are multiple trademarks with the same name, append the application number.
 */
const displayTrademark = (trademark: Trademark) =>
  trademarkCounts.value[trademark.name] > 1
    ? `${trademark.name} (#${trademark.application_number})`
    : trademark.name
</script>
