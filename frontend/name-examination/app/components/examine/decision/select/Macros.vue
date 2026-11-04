<template>
  <div>
    <h3 class="font-semibold">Macros</h3>
    <ListSelect
      v-model="examine.selectedMacros"
      :disabled="examine.decisionSelectionsDisabled"
      :options="examine.macros"
      :options-display="(option: Macro) => option.name"
      options-style="!max-h-48"
      multiple
      close-on-select
    >
      <Chips
        v-if="examine.selectedMacros.length > 0"
        v-model="examine.selectedMacros"
        :display="(macro: Macro) => macro.name"
      />
    </ListSelect>
  </div>
</template>

<script setup lang="ts">
/** A dropdown for selecting macros */
import { useExamination } from '~/store/examine'
import type { Macro } from '~/types'

const examine = useExamination()
</script>
