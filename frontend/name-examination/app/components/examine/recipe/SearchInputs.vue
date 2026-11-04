<template>
  <div class="flex w-full space-x-2">
    <SearchInput
      :input-id="NAME_SEARCH_ID"
      v-model="searchString"
      class="grow"
      placeholder="name"
      @submit.prevent="onNameSearchSubmit"
      focus-mnemonic="s"
      :clear="examine.currentName ?? undefined"
      input-required
    />
    <SearchInput
      :input-id="EXACT_SEARCH_ID"
      v-model="exactSearchString"
      placeholder="exact phrase"
      @submit.prevent="onExactSearchSubmit"
      clear=""
    />
  </div>
</template>

<script setup lang="ts">
import { useExamination } from '~/store/examine'
import { useExaminationTabCyle } from '~/store/examine/tab-cycle'
import { emitter } from '~/util/emitter'

const examine = useExamination()
const tabCycle = useExaminationTabCyle()

const NAME_SEARCH_ID = 'nameSearchInput'
const EXACT_SEARCH_ID = 'exactSearchInput'

const searchString = ref(examine.currentName ?? '')
const exactSearchString = ref('')

async function loadRecipe(searchQuery: string, exactPhrase: string) {
  try {
    await examine.fetchAndLoadRecipeData(searchQuery, exactPhrase)
  } catch (e: any) {
    emitter.emit('error', {
      title: 'Failed to load Recipe area',
      message: e.message,
    })
  }
}

function onNameSearchSubmit(_event: Event) {
  loadRecipe(searchString.value, '')
}

function onExactSearchSubmit(_event: Event) {
  const phrase = exactSearchString.value.trim()
  if (!phrase) return
  loadRecipe(searchString.value, phrase)
}

onMounted(() => {
  tabCycle.register(0, NAME_SEARCH_ID)
  tabCycle.register(1, EXACT_SEARCH_ID)
})

watch(
  () => [examine.currentName],
  async (_state) => {
    searchString.value = examine.currentName ?? ''
    exactSearchString.value = ''
    await examine.fetchAndLoadRecipeData(
      searchString.value,
      exactSearchString.value
    )
  },
  { deep: true }
)
</script>
