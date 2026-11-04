<template>
  <div class="flex items-center">
    <h2 class="font-bold">Expiry:&nbsp;</h2>
    <span v-if="examine.expiryDate" data-testid="expiryDate">
      {{ examine.expiryDate }}
    </span>
    <span v-else data-testid="expiryDate">n/a</span>
  </div>

  <div v-if="examine.nrStatus === Status.Conditional">
    <div class="flex items-center">
      <h2 class="font-bold">Consent:&nbsp;</h2>
      <span>{{ consentText }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ConsentFlag } from '~/enums/codes'
import { Status } from '~/enums/nr-status'
import { useExamination } from '~/store/examine'

const examine = useExamination()

const consentText = computed(() => {
  switch (examine.consentFlag) {
    case ConsentFlag.Received:
      return examine.consentDate
    case ConsentFlag.Required:
      return 'Required'
    case ConsentFlag.Waived:
      return 'Waived'
    default:
      return '-'
  }
})
</script>
