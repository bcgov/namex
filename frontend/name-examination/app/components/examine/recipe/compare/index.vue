<template>
  <div class="flex h-full flex-col space-y-2 overflow-auto p-2">
    <ExamineRecipeCompareItem
      v-for="conflict in conflicts.comparedConflicts"
      :conflict="conflict"
    />

    <div
      v-if="conflicts.comparedConflicts.length === 0"
      class="flex h-full items-center justify-center"
    >
      <p class="text-xl">
        Add conflicts to compare in the <b>Conflicts</b> tab
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
/** Compare tab in the recipe area */
import { useConflicts } from '~/store/examine/conflicts'
const conflicts = useConflicts()
</script>
