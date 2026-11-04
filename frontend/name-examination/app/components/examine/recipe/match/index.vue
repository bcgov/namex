<template>
  <div v-if="isLoading" class="flex items-center justify-center">
    <LoadingSpinner />
  </div>
  <div v-else-if="conflictData">
    <ExamineRecipeMatchNames
      v-if="conflict.source === 'NAMEREQUEST' || conflict.source === 'NRO'"
      :conflict="(conflictData as NameRequest)"
    />
    <ExamineRecipeMatchBCCorp
      v-else-if="conflict.source === 'CORP' && (conflictData as Corporation).jurisdiction === 'BC'"
      :data="(conflictData as BCCorporation)"
    />
    <ExamineRecipeMatchXproCorp
      v-else-if="conflict.source === 'CORP' && (conflictData as Corporation).jurisdiction !== 'BC'"
      :conflict="(conflictData as XproCorporation)"
    />
    <div v-else>Failed to determine conflict info type</div>
  </div>
  <div v-else>
    <p>Failed to retrieve conflict data</p>
    <a
      class="cursor-pointer text-blue-800 underline"
      @click="tryToGetConflictData"
    >
      Try again
    </a>
  </div>
</template>

<script setup lang="ts">
import { useConflictData } from '~/store/examine/conflict-data'
import type {
  BCCorporation,
  ConflictListItem,
  ConflictData,
  NameRequest,
  XproCorporation,
  Corporation,
} from '~/types'

const props = defineProps<{
  conflict: ConflictListItem
}>()

const { getConflictData } = useConflictData()
const conflictData = ref<ConflictData>()
const isLoading = ref(false)

async function tryToGetConflictData() {
  isLoading.value = true
  try {
    conflictData.value = await getConflictData(props.conflict)
  } catch (e) {
    conflictData.value = undefined
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {
  await tryToGetConflictData()
})

onUnmounted(() => {
  conflictData.value = undefined
})
</script>
