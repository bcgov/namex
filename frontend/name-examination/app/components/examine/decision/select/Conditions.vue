<template>
  <div>
    <h3 class="font-semibold">Conditions</h3>
    <ListSelect
      v-model="examine.selectedConditions"
      :options="options"
      :options-display="(condition: Condition) => condition.phrase"
      options-style="!max-h-48"
      :disabled="examine.decisionSelectionsDisabled"
      multiple
      close-on-select
    >
      <Chips
        v-if="examine.selectedConditions.length > 0"
        v-model="examine.selectedConditions"
        :display="(condition: Condition) => condition.phrase"
      />
    </ListSelect>
  </div>
</template>

<script setup lang="ts">
/** A dropdown for selecting conditions */
import { useExamination } from '~/store/examine'
import type { Condition } from '~/types'

const examine = useExamination()

const options = computed(() =>
  examine.conditions.filter((c) => c.instructions !== '')
)
</script>
