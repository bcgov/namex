<template>
  <div class="flex flex-col space-y-4 border-y px-8 py-4 text-sm">
    <div class="grid grid-cols-4 gap-y-1">
      <span class="font-bold">Date/Time</span>
      <span>{{ eventDate }}</span>

      <span class="font-bold">Expiry Date</span>
      <span>{{ expiryDate }}</span>

      <span class="font-bold">Transaction Type</span>
      <span>{{ entry.user_action }}</span>

      <span class="font-bold">User ID</span>
      <span>{{ entry.user_name }}</span>

      <span class="font-bold">Request Status</span>
      <span>{{ statusDisplay }}</span>

      <span class="font-bold">Queue</span>
      <PriorityLabel v-if="entry.priorityCd === 'Y'" />
      <span v-else>Regular</span>

      <span class="font-bold">Request Type</span>
      <span>{{ requestTypeDisplay }}</span>

      <span class="font-bold">Consent</span>
      <span>{{ consentDisplay }}</span>

      <span class="font-bold">Additional Info</span>
      <span>{{ entry.additionalInfo }}</span>

      <span v-if="isStaffCommentAction" class="font-bold">Staff Comment</span>
      <span v-else></span>
      <span v-if="isStaffCommentAction">{{ entry.comment }}</span>
      <span v-else></span>
    </div>

    <TransactionsEntryNamesList :names="entry.names" />
  </div>
</template>

<script setup lang="ts">
import { DateTime } from 'luxon'
import { useTransactions } from '~/store/transactions'
import type { TransactionEntry } from '~/types'
import { getFormattedDateWithTimeAndZone, parseDate } from '~/util/date'

const { entry } = defineProps<{
  entry: TransactionEntry
}>()

const transactions = useTransactions()

const eventDate = computed(() =>
  getFormattedDateWithTimeAndZone(DateTime.fromHTTP(entry.eventDate))
)

const statusDisplay = computed(() =>
  transactions.getStatusDisplay(entry.stateCd, entry.names)
)

const expiryDate = computed(() => {
  if (!entry.expirationDate) return 'N/A'

  const isoDate = parseDate(entry.expirationDate)
  if (isoDate.isValid) return getFormattedDateWithTimeAndZone(isoDate)

  const customDate = DateTime.fromFormat(
    entry.expirationDate,
    'yyyy-MM-dd hh:mm:ss'
  )
  if (customDate.isValid) return getFormattedDateWithTimeAndZone(customDate)

  return 'N/A'
})

const requestTypeDisplay = computed(() =>
  transactions.getRequestTypeDisplay(
    entry.requestTypeCd,
    entry.request_action_cd
  )
)

const consentDisplay = computed(() =>
  transactions.getConsentDisplay(entry.consent_dt, entry.consentFlag)
)

const isStaffCommentAction = computed(
  () => entry.user_action === 'Staff Comment'
)
</script>
