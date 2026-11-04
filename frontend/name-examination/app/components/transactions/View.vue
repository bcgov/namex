<template>
  <div class="flex h-full flex-col">
    <TransactionsHeader
      v-if="transactions.nr"
      :data="transactions.nr"
      :loading="transactions.loadingNr"
    />
    <TransactionsEntryList
      :entries="transactions.transactions"
      :loading="transactions.loadingTransactions"
    />
  </div>
</template>

<script setup lang="ts">
import { useTransactions } from '~/store/transactions'

const props = defineProps<{
  nrNumber: string
}>()

const transactions = useTransactions()

onMounted(async () => {
  await transactions.initialize(props.nrNumber)
})
</script>
