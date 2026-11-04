<template>
  <Accordion
    :open="list.ui.open"
    :arrow="list.children.length > 0"
    :disabled="list.children.length === 0"
    :button-style="{ 'bg-sky-100': list.ui.focused }"
    @title-clicked="recipe.clickObject(list)"
  >
    <template #title>
      <div class="flex w-full justify-between font-medium">
        <div>
          <span v-html="list.highlightedText"></span>
          <span v-if="list.meta" class="italic">
            &nbsp;&ndash;&nbsp;{{ list.meta.toLowerCase() }}
          </span>
        </div>
        <span v-if="list.children.length > 0">
          {{ list.children.length }}
        </span>
      </div>
    </template>
    <template #content>
      <div class="flex flex-col space-y-1">
        <ExamineRecipeConflictsListItem
          v-for="item in list.children"
          :key="item.nrNumber"
          :conflict-item="item"
        />
      </div>
    </template>
  </Accordion>
</template>

<script setup lang="ts">
import { useExaminationRecipe } from '~/store/examine/recipe'
import type { ConflictList } from '~/types'

defineProps<{
  list: ConflictList
}>()

const recipe = useExaminationRecipe()
</script>
