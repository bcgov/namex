<template>
  <div class="flex justify-between justify-self-end">
    <IconButton
      light
      class="bg-lime-600"
      mnemonic="a"
      @click="examine.makeDecision(Status.Approved)"
      data-testid="primaryApprovalBtn"
    >
      <CheckIcon class="h-5 w-5 stroke-2" />
      <template v-if="examine.consentRequired" #text>
        Conditionally <u>A</u>pprove
      </template>
      <template v-else #text><u>A</u>pprove Name</template>
    </IconButton>

    <IconButton
      light
      class="bg-red-error"
      mnemonic="r"
      @click="examine.makeDecision(Status.Rejected)"
      data-testid="primaryRejectionBtn"
    >
      <XMarkIcon class="h-5 w-5 stroke-2" />
      <template #text><u>R</u>eject Name</template>
    </IconButton>
  </div>
</template>

<script setup lang="ts">
/** Approve/reject buttons for the decision area */
import { useExamination } from '~/store/examine'
import { CheckIcon, XMarkIcon } from '@heroicons/vue/24/outline'
import { Status } from '~/enums/nr-status'
const examine = useExamination()
</script>
