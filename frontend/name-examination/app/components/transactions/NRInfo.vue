<template>
  <div class="flex text-sm">
    <div class="grid grow grid-cols-4">
      <span class="font-bold">Submitted Date</span>
      <span>{{ submittedDate }}</span>

      <span class="font-bold">Expiry Date</span>
      <span>
        {{ expirationDate }}
      </span>

      <span class="font-bold">Request Status</span>
      <span>{{ statusDisplay }}</span>

      <span class="font-bold">Consent</span>
      <span>{{ consentDisplay }}</span>

      <span class="font-bold">Additional Information</span>
      <span>{{ data.additionalInfo }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ConsentFlag } from '~/enums/codes'
import type { Status } from '~/enums/nr-status'
import { useTransactions } from '~/store/transactions'
import type { NameRequest } from '~/types'
import { parseDate, getFormattedDateWithTimeAndZone } from '~/util/date'

const { data } = defineProps<{
  data: NameRequest
}>()

const transactions = useTransactions()

const submittedDate = computed(() =>
  getFormattedDateWithTimeAndZone(parseDate(data.submittedDate))
)

const expirationDate = computed(() =>
  data.expirationDate
    ? getFormattedDateWithTimeAndZone(parseDate(data.expirationDate))
    : 'N/A'
)

const statusDisplay = computed(() =>
  transactions.getStatusDisplay(data.stateCd as Status, data.names)
)

const consentDisplay = computed(() =>
  transactions.getConsentDisplay(
    data.consent_dt,
    data.consentFlag || ConsentFlag.Waived
  )
)
</script>
