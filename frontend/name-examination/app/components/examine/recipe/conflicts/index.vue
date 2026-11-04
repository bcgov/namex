<template>
  <div
    :id="recipe.CONFLICTS_AREA_ID"
    class="h-full w-full outline-none"
    tabindex="0"
    @keydown="recipe.handleKeyDown"
    @focus="recipe.focusArea"
    @focusout="recipe.unfocusArea"
  >
    <div
      v-if="conflicts.loading"
      class="flex h-full items-center justify-center"
    >
      <LoadingSpinner />
    </div>
    <div v-else class="flex w-full flex-col space-y-2 rounded bg-white p-2">
      <ExamineRecipeConflictsBucket
        title="Exact Match"
        :conflict-items="conflicts.exactMatches"
      />

      <ExamineRecipeConflictsBucket
        title="Exact Word Order + Synonym Match"
        :conflict-lists="conflicts.synonymMatches"
      />

      <ExamineRecipeConflictsBucket
        title="Character Swap Match"
        :conflict-lists="conflicts.cobrsPhoneticMatches"
      />

      <ExamineRecipeConflictsBucket
        title="Phonetic Match (experimental)"
        :conflict-lists="conflicts.phoneticMatches"
      />

    </div>
  </div>
</template>

<script setup lang="ts">
/** Conflicts tab in the recipe area */
import { useConflicts } from '~/store/examine/conflicts'
import { useExaminationRecipe } from '~/store/examine/recipe'
import { useExaminationTabCyle } from '~/store/examine/tab-cycle'

const conflicts = useConflicts()
const recipe = useExaminationRecipe()

onMounted(() => {
  useExaminationTabCyle().register(2, 'conflicts-tab')
})
</script>
