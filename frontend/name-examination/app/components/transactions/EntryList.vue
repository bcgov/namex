<template>
  <div class="flex h-full flex-col overflow-y-auto">
    <!-- Tabs -->
    <div class="flex space-x-2 border-b mb-2 bg-gray-200 rounded-t">
      <button
        class="px-4 py-2 -mb-px border-b-2 rounded-t border border-b-0"
        :class="selectedFilter === 'default'
          ? 'border-blue-500 bg-white text-bcgov-blue3 font-bold'
          : 'border-gray-300 bg-gray-300 text-gray-500'"
        @click="selectedFilter = 'default'"
        data-testid="showDefaultTab"
      >
        Default
      </button>
      <button
        class="px-4 py-2 -mb-px border-b-2 rounded-t border border-b-0"
        :class="selectedFilter === 'notifications'
          ? 'border-blue-500 bg-white text-bcgov-blue3 font-bold'
          : 'border-gray-300 bg-gray-300 text-gray-500'"
        @click="selectedFilter = 'notifications'"
        data-testid="showNotificationsTab"
      >
        Notifications
      </button>
      <button
        class="px-4 py-2 -mb-px border-b-2 rounded-t border border-b-0"
        :class="selectedFilter === 'all'
          ? 'border-blue-500 bg-white text-bcgov-blue3 font-bold'
          : 'border-gray-300 bg-gray-300 text-gray-500'"
        @click="selectedFilter = 'all'"
        data-testid="showSystemTransactionsTab"
      >
        System/All Transactions
      </button>
    </div>

    <div v-if="loading" class="flex items-center justify-center">
      <LoadingSpinner />
    </div>

    <div
      v-else-if="entries.length === 0"
      class="flex items-center justify-center py-2"
    >
      <span class="text-xl font-bold">No transactions available</span>
    </div>

    <div v-else class="flex flex-col overflow-y-auto">
      <template v-for="(entry, i) in filteredEntries" :key="entry.eventDate + entry.user_action + entry.stateCd">
        <!-- Render TransactionsNotificationEntry if user_action is 'notification' -->
        <TransactionsNotificationEntry
          v-if="entry.user_action === 'notification'"
          :entry="entry"
          :class="{ 'bg-neutral-100': i % 2 == 0 }"
          data-testid="notificationEntry"
        />
        <!-- Render TransactionsEntry otherwise -->
        <TransactionsEntry
          v-else
          :entry="entry"
          :class="{ 'bg-neutral-100': i % 2 == 0 }"
          data-testid="transactionEntry"
        />
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TransactionEntry } from '~/types'

const props = defineProps<{
  entries: Array<TransactionEntry>
  loading?: boolean
}>()

const DEFAULT_TRANSACTIONS = [
  'Cancelled in Name Request',
  'Created NR (Payment Completed)',
  'Created NR (Unknown)',
  'Decision',
  'Edit NR Details (Name Request)',
  'Edit NR Details (NameX)',
  'Edit NR Details after Completion',
  'Marked on Hold',
  'Reapplied NR (Unknown)',
  'Reset',
  'Staff Comment',
]

const selectedFilter = ref<'all' | 'notifications' | 'default'>('default')

const filteredEntries = computed(() => {
  if (selectedFilter.value === 'all') {
    return props.entries
  }
  if (selectedFilter.value === 'notifications') {
    return props.entries.filter(item => item.user_action === 'notification')
  }
  // default
  return props.entries.filter((item) =>
    DEFAULT_TRANSACTIONS.includes(item.user_action)
  )
})

const headerText = computed(() => {
  const baseText = 'Transaction History'
  const count = filteredEntries.value.length
  if (count > 0) {
    const itemsText = `${count} item${count === 1 ? '' : 's'}`
    return `${baseText} (${itemsText})`
  } else {
    return baseText
  }
})
</script>
