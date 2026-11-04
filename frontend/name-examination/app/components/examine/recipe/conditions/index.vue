<template>
  <ExamineRecipeTable
    class="h-full w-full"
    :columns="[
      'Word',
      'Allow',
      'Consent',
      'Examiner Information',
      'Instructions',
    ]"
    :rows="rows"
  />
</template>

<script setup lang="ts">
/** Conditions tab in the recipe area */
import { useExamination } from '~/store/examine'
const examine = useExamination()
const rows = computed(() =>
  examine.conditions.map((item) => [
    item.phrase,
    item.allow_use,
    item.consent_required,
    item.text,
    item.instructions,
  ])
)
</script>
