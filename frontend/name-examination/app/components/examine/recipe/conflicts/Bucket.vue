<template>
  <div class="flex flex-col space-y-1">
    <div class="rounded bg-gray-200 p-2 text-sm font-semibold">
      {{ title }}
    </div>
    <div class="px-1">
      <div v-if="conflictLists">
        <ExamineRecipeConflictsList
          ref="listElems"
          v-if="conflictLists.length > 0"
          v-for="list in conflictLists"
          :key="list.text"
          :list="list"
        />
        <span v-else class="px-1 italic">No results</span>
      </div>
      <div v-else-if="conflictItems" class="flex flex-col space-y-1">
        <ExamineRecipeConflictsListItem
          v-if="conflictItems.length > 0"
          v-for="item in conflictItems"
          :key="item.nrNumber"
          :conflict-item="item"
        />
        <span v-else class="px-1 italic">No results</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * A conflicts bucket that displays a list of conflict lists, or a list of conflict items
 */
import Accordion from '~/components/Accordion.vue'
import type { ConflictList, ConflictListItem } from '~/types'
import { isConflictList } from '~/util'
import { emitter } from '~/util/emitter'

const props = defineProps<{
  title: string
  /** If a list of `ConflictList`s is provided, it will be displayed instead of the `ConflictListItems`s */
  conflictLists?: Array<ConflictList>
  /** If a list of `ConflictListItem`s is provided, it will be displayed instead of the `ConflictList`s */
  conflictItems?: Array<ConflictListItem>
}>()

const listElems = ref<Array<InstanceType<typeof Accordion>>>([])

emitter.on('scrollToConflictObject', async ({ obj, instant }) => {
  if (isConflictList(obj) && props.conflictLists?.includes(obj)) {
    const index = props.conflictLists.indexOf(obj)
    const element = listElems.value[index].$el as HTMLElement
    await nextTick()
    element
      .getElementsByClassName('accordion-title')
      .item(0)
      ?.scrollIntoView({
        behavior: instant ? 'instant' : 'smooth',
        block: 'center',
      })
  }
})
</script>
