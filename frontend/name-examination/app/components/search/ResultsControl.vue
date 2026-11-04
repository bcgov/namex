<template>
  <div class="flex items-center">
    <a
      href="#"
      class="mr-4 font-semibold text-blue-800 transition duration-150 hover:text-blue-900"
      @click="reset"
      >{{ CLEAR_FILTERS_TEXT }}</a
    >

    <ListSelect
      class="z-10 w-48"
      v-model="search.selectedColumns"
      :options="search.fixedColumns"
      multiple
    >
      Columns to Show
    </ListSelect>

    <div class="z-10 ml-auto flex items-center space-x-2">
      <span class="mr-4 font-semibold">Results: {{ search.resultNum }}</span>

      <span>Display: </span>
      <ListSelect v-model="search.selectedDisplay" :options="DISPLAY_OPTIONS">
        {{ search.selectedDisplay }}
      </ListSelect>

      <span>Page: </span>
      <ComboSelect
        v-model="search.selectedPage"
        :options="computed(() => pageOptions)"
        class="w-24"
      />
      <span>of {{ search.lastPageNumber }}</span>
    </div>

    <div class="ml-4 space-x-2">
      <IconButton
        class="!py-[0.3125rem] px-5"
        @click="search.goToPreviousPage()"
      >
        <ChevronLeftIcon class="h-6 stroke-2" />
      </IconButton>
      <IconButton class="!py-[0.3125rem] px-5" @click="search.goToNextPage()">
        <ChevronRightIcon class="h-6 stroke-2" />
      </IconButton>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * A component that contains disply, page, and column controls for the search page
 */
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/24/outline'
import { useSearchStore } from '~/store/search'

const CLEAR_FILTERS_TEXT = 'Clear Filters'

const search = useSearchStore()

// dropdown option values
const DISPLAY_OPTIONS = [5, 10, 20, 50, 100]

// create array of values in range [1, lastPageNumber]
const pageOptions = computed(() =>
  Array.from({ length: search.lastPageNumber }, (_, key) => key + 1)
)

function reset() {
  search.resetFilters()
  search.resetDisplayAndPage()
}
</script>
