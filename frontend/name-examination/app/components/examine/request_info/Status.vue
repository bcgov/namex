<template>
  <div class="space-y-1 py-1 text-sm">
    <PriorityLabel v-if="examine.priority" />

    <div class="flex items-center">
      <h2 class="font-bold">Status:&nbsp;</h2>
      <p data-testid="nrStatus">{{ nrStatus }}</p>
    </div>

    <div class="flex items-center">
      <h2 class="font-bold">Examiner:&nbsp;</h2>
      <p data-testid="nrExaminer">{{ examinerStatus }}</p>
    </div>

    <ExamineRequestInfoCommentsPopup />
  </div>
</template>

<script setup lang="ts">
import { Status } from '~/enums/nr-status'
import { useExamination } from '~/store/examine'
import { usePayments } from '~/store/examine/payments'
import { useTransactions } from '~/store/transactions'

const examine = useExamination()
const payments = usePayments()
const transactions = useTransactions()
const examinerStatus = ref(examine.examiner)

const nrStatus = computed(() => {
  const approvedName = examine.nameChoices.find((name) =>
    [Status.Approved, Status.Condition].includes(name.state)
  )
  if (approvedName) {
    const displayState =
      approvedName.state === Status.Condition
        ? 'CONDITIONALLY APPROVED'
        : 'APPROVED'
    if (examine.nrStatus == Status.Consumed) {
      return `${displayState} - CONSUMED`
    } else if (examine.isApprovedAndExpired) {
      return `${displayState} - EXPIRED`
    }
  }

  if (examine.nrStatus == Status.RefundRequested) {
    return `CANCELLED - ${payments.refundPaymentState}`
  }

  return examine.nrStatus
})

// Find the last Idir that edited the NR in transations
onMounted(async () => {
  if (!examinerStatus.value?.includes('idir')) {
    const lastIdirUpdate = await transactions.getLatestIdir(examine.nrNumber)
    if (lastIdirUpdate !== 'N/A') {
      examinerStatus.value = lastIdirUpdate
    }
  }
})
</script>
