<template>
  <div class="flex h-9 space-x-1">
    <IconButton 
      white 
      class="border-none whitespace-pre" 
      @click="quickApprove"
      data-testid="quickApproveBtn"
    >
      <CheckCircleIcon class="h-7 w-7 text-lime-600" />
      <template #text>Quick Approve</template>
    </IconButton>

    <IconButton
      white
      class="border-none whitespace-pre"
      mnemonic="i"
      @click="rejectDistinctive"
      data-testid="quickRejectDistBtn"
    >
      <XCircleIcon class="h-7 w-7 text-red-error" />
      <template #text>Reject D<u>i</u>stinctive</template>
    </IconButton>

    <IconButton
      white
      class="border-none whitespace-pre"
      mnemonic="e"
      @click="rejectDescriptive"
      data-testid="quickRejectDescBtn"
    >
      <XCircleIcon class="h-7 w-7 text-red-error" />
      <template #text>Reject D<u>e</u>scriptive</template>
    </IconButton>
  </div>
</template>

<script setup lang="ts">
/** Buttons for quickly approving/rejecting an NR */
import { CheckCircleIcon, XCircleIcon } from '@heroicons/vue/24/solid'
import { Status } from '~/enums/nr-status'
import { useExamination } from '~/store/examine'
import { useConflicts } from '~/store/examine/conflicts';

const examine = useExamination()
const conflicts = useConflicts()

async function quickApprove() {
  if (examine.consentRequired) {
    await examine.makeDecision(Status.Approved)
  } else {
    conflicts.clearSelectedConflicts()
    await examine.makeQuickDecision(Status.Approved, '')
  }
}

async function rejectDescriptive() {
  await examine.makeQuickDecision(
    Status.Rejected,
    'Require descriptive second word or phrase * E.G. Construction, Gardening, Investments, Holdings, Etc.'
  )
}

async function rejectDistinctive() {
  await examine.makeQuickDecision(
    Status.Rejected,
    "Require distinctive, nondescriptive first word or prefix * E.G. Person's name, initials, geographic location, etc."
  )
}
</script>

<style scoped>
u {
  margin: 0 !important;
}
</style>
