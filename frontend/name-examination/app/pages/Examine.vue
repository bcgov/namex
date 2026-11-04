<template>
  <div
    v-if="examine.initializing"
    class="flex h-[75vh] items-center justify-center"
  >
    <LoadingSpinner />
  </div>
  <div
    v-else
    class="flex h-full flex-col"
    :class="{ 'bg-gray-100': examine.isEditing }"
  >
    <NoticeBanner v-if="examine.otherExaminerInProgress" type="lock">
      <span>
        This NR is being examined by
        <span class="font-bold">{{ examine.examiner }}</span>
      </span>
    </NoticeBanner>

    <NoticeBanner v-if="examine.exactHistoryMatch" type="warning">
      <span>
        Similar name previously
        <span class="font-bold">{{ examine.exactHistoryMatch }}</span>
      </span>
    </NoticeBanner>

    <ExamineHeader />
    <ExamineRequestInfo />

    <div class="flex justify-between p-4">
      <ExamineNamesList
        v-if="!examine.isEditing"
        class="ml-4 basis-1/2"
        :choices="examine.nameChoices"
        :current-choice="examine.currentChoice"
        :complete="examine.isComplete"
        :undoable="examine.isUndoable"
        :undo="examine.undoNameChoiceDecision"
        highlight
      />
      <div v-else class="flex w-full justify-between">
        <ExamineNamesListEditable />
        <ExamineEditActionButtons class="basis-1/5 self-start px-4" />
      </div>

      <ExamineQuickActionButtons v-if="showQuickActionButtons" />
    </div>

    <div
      v-if="
        !examine.isComplete && !reservedOrCondReserved && !examine.isEditing
      "
      class="flex grow flex-col space-x-3 bg-gray-100 p-4 2xl:flex-row"
    >
      <ExamineRecipe class="2xl:w-1/2" />
      <ExamineDecision v-if="showDecisionPanel" class="2xl:w-1/2" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Status } from '~/enums/nr-status'
import { Route } from '~/enums/routes'
import { useExamination } from '~/store/examine'
import { emitter } from '~/util/emitter'
const examine = useExamination()

const showQuickActionButtons = computed(
  () =>
    !examine.isComplete &&
    examine.isMakingDecision &&
    examine.userHasApproverRole &&
    examine.isMyCurrentNr &&
    !examine.isEditing
)

const showDecisionPanel = computed(
  () => examine.isCurrentExaminer && examine.isMakingDecision
)

const reservedOrCondReserved = computed(() =>
  [Status.ConditionalReserved, Status.Reserved].includes(examine.nrStatus)
)

onMounted(async () => {
  const query = useRoute().query
  if ('nr' in query) {
    try {
      const nrNumber = `NR ${query.nr}`
      await examine.initialize(nrNumber)
    } catch (e: any) {
      emitter.emit('error', { title: 'Failed to load NR', message: e })
      await navigateTo(Route.Search)
    }
  } else if (!examine.nrNumber || !examine.isMyCurrentNr) {
    try {
      await examine.initializeNext()
    } catch (e: any) {
      emitter.emit('error', { title: 'Failed to load next NR', message: e })
      await navigateTo(Route.Search)
    }
  } else {
    await examine.updateRoute(examine.nrNumber)
  }
})
</script>