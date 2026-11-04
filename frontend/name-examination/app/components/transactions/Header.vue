<template>
  <div v-if="loading" class="flex items-center justify-center">
    <LoadingSpinner />
  </div>

  <div v-else class="flex flex-col space-y-4 p-4">
    <div class="flex items-center divide-x-2 divide-gray-300">
      <NRNumber
        :nr-number="data.nrNum"
        :priority="isPriority"
        class="pr-2 !text-xl"
      />
      <PriorityLabel
        v-if="isPriority"
        class="px-2 text-xl"
        icon-style="h-5 w-5"
      />
      <NameRequestTypeInfo
        class="!flex-row items-center space-x-2 pl-2 text-xl"
        :request-type-text="requestTypeDisplay"
        :jurisdiction="data.xproJurisdiction || undefined"
        :jurisdiction-number="data.homeJurisNum || undefined"
      />
    </div>
    <ExamineNamesList class="pl-4" :choices="data.names" highlight />
    <TransactionsNRInfo :data="data" class="w-full" />
  </div>
</template>

<script setup lang="ts">
import type { NameRequest } from '~/types'
import NameRequestTypeInfo from '../NameRequestTypeInfo.vue'
import { useTransactions } from '~/store/transactions'

const { data } = defineProps<{
  data: NameRequest
  loading?: boolean
}>()

const transactions = useTransactions()

const isPriority = computed(() => data.priorityCd === 'Y')
const requestTypeDisplay = computed(() =>
  transactions.nr
    ? transactions.getRequestTypeDisplay(
        transactions.nr.requestTypeCd,
        transactions.nr.request_action_cd
      )
    : 'N/A'
)
</script>
