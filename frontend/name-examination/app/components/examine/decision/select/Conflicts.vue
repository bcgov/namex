<template>
  <div>
    <h3 class="font-semibold">Conflicts</h3>
    <ListSelect
      v-model="conflicts.selectedConflicts"
      :options="options"
      options-style="!max-h-48 !max-w-md"
      :options-display="(option: ConflictListItem) => option.text"
      :disabled="examine.decisionSelectionsDisabled"
      @change="(_) => conflicts.syncSelectedAndComparedConflicts()"
      multiple
      close-on-select
    >
      <Chips
        v-if="conflicts.selectedConflicts.length > 0"
        v-model="conflicts.selectedConflicts"
        :display="(conflict: ConflictListItem) => conflict.text"
        :get-key="(conflict: ConflictListItem) => conflict.nrNumber"
        @chip-removed="conflicts.syncSelectedAndComparedConflicts()"
      />
      <template #no-data>
        {{
          conflicts.autoAdd
            ? 'No conflicts'
            : 'No conflicts selected (and auto add is off)'
        }}
      </template>
    </ListSelect>
  </div>
</template>

<script setup lang="ts">
/** A dropdown for selecting conflicts */
import { useExamination } from '~/store/examine'
import { useConflicts } from '~/store/examine/conflicts'
import type { ConflictListItem } from '~/types'

const examine = useExamination()
const conflicts = useConflicts()

const options = computed<Array<ConflictListItem>>(() => {
  if (!conflicts.autoAdd) {
    return conflicts.comparedConflicts
  }

  const allConflicts = [
    ...conflicts.exactMatches,
    ...conflicts.synonymMatches.map((c) => c.children).flat(),
    ...conflicts.cobrsPhoneticMatches.map((c) => c.children).flat(),
    ...conflicts.phoneticMatches.map((c) => c.children).flat(),
  ]

  const seenNRs: Array<string> = []
  return allConflicts.filter((conflict) => {
    const alreadySeen = seenNRs.includes(conflict.nrNumber)
    if (!alreadySeen) {
      seenNRs.push(conflict.nrNumber)
      return true
    } else {
      return false
    }
  })
})
</script>
