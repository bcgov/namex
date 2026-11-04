<template>
  <div v-if="isLoading" class="flex items-center justify-center">
    <LoadingSpinner />
  </div>
  <div v-else-if="historiesInfo" class="flex-col p-4">
    <div class="flex gap-x-2 text-sm">
      <div class="flex basis-2/3 flex-col">
        <div v-if="applicants" class="grid grid-cols-2 gap-y-1 overflow-x-auto">
          <h3 class="font-bold">Client</h3>
          <p>
            {{ applicants.clientFirstName }} {{ applicants.clientLastName }}
          </p>

          <h3 class="font-bold">Applicant</h3>
          <div>
            <p>{{ applicants.firstName }} {{ applicants.lastName }}</p>
            <p>{{ applicants.addrLine1 }}</p>
            <p>{{ applicants.addrLine2 }}</p>
            <p>{{ applicants.addrLine3 }}</p>
            <p>
              {{ applicants.city }}
              {{ applicants.stateProvinceCd }}
              {{ applicants.postalCd }}
              {{ applicants.countryTypeCd }}
            </p>
          </div>

          <h3 class="font-bold">Phone</h3>
          <p>{{ applicants.phoneNumber }}</p>

          <h3 class="font-bold">Email</h3>
          <p>{{ applicants.emailAddress }}</p>

          <h3 class="font-bold">Contact</h3>
          <p>{{ applicants.contact }}</p>
        </div>
      </div>

      <div
        class="grid basis-1/3 auto-rows-min grid-cols-2 gap-y-1 overflow-x-auto"
      >
        <h3 class="font-bold">Name State</h3>
        <p>{{ nameState }}</p>

        <h3 v-if="conflicts.length > 0" class="font-bold">Conflicts</h3>
        <ol v-if="conflicts.length > 0" class="list-inside list-decimal">
          <li v-for="c in conflicts">{{ c }}</li>
        </ol>

        <h3 v-if="decisionText" class="font-bold">Decision</h3>
        <div class="flex flex-col">
          <p>{{ decisionText }}</p>
        </div>
      </div>
    </div>

    <div
      v-if="historiesInfo.comments && historiesInfo.comments.length > 0"
      class="mt-2 w-full"
    >
      <h3 class="font-bold">Comments</h3>
      <ExamineCommentsBox
        :comments="historiesInfo.comments"
        class="max-h-48 w-full overflow-auto rounded border border-gray-400 p-2 children:bg-sky-50"
      />
    </div>
  </div>
  <div v-else class="p-4 font-bold text-red-600">Failed to retrieve info.</div>
</template>

<script setup lang="ts">
import { type NameRequest, type HistoryEntry } from '~/types'
import { getNameRequest } from '~/util/namex-api';

const props = defineProps<{
  historyEntry: HistoryEntry
}>()

const isLoading = ref(false)

const historiesInfo = ref<NameRequest>()
const applicants = computed(() => historiesInfo.value?.applicants)

const nameState = computed(() => {
  if (!historiesInfo.value) return null

  for (const nameChoice of historiesInfo.value.names)
    if (nameChoice.name === props.historyEntry.name) return nameChoice.state

  return null
})

const decisionText = computed(() => {
  if (!historiesInfo.value) return null

  for (const nameChoice of historiesInfo.value.names) {
    if (
      nameChoice.name === props.historyEntry.name &&
      nameChoice.decision_text != ''
    ) {
      return nameChoice.decision_text
    }
  }
  return null
})

const conflicts = computed(() => {
  if (!historiesInfo.value) return []

  for (const nameChoice of historiesInfo.value.names)
    if (nameChoice.name === props.historyEntry.name) {
      return [
        nameChoice.conflict1,
        nameChoice.conflict2,
        nameChoice.conflict3,
      ].filter((choice) => choice != null && choice != '')
    }

  return []
})

onMounted(async () => {
  isLoading.value = true
  const nrResponse = await getNameRequest(props.historyEntry.nr_num)
  historiesInfo.value = await nrResponse.json()
  isLoading.value = false
})

onUnmounted(() => {
  historiesInfo.value = undefined
})
</script>
