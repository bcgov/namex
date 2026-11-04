<template>
  <div class="flex items-center space-x-3">
    <!-- Edit Button -->
    <IconButton
      v-if="examine.canEdit && notHistoricalReservedConsumed"
      light
      @click="examine.edit"
      mnemonic="d"
      data-testid="actionEditBtn"
    >
      <PencilSquareIcon class="h-5 w-5" />
      <template #text>E<u>d</u>it Request</template>
    </IconButton>

    <!-- Toggle Details Button -->
    <IconButton 
      light 
      @click="toggleDetails" 
      mnemonic="b"
      :data-testid="examine.isHeaderShown ? 'actionHideDetailsBtn' : 'actionShowDetailsBtn'"
    >
      <ArrowsPointingInIcon
        v-if="examine.isHeaderShown"
        class="h-5 w-5"
      />
      <ArrowsPointingOutIcon v-else class="h-5 w-5" />

      <template #text v-if="examine.isHeaderShown"
        >Hide Details (<u>b</u>)
      </template>
      <template #text v-else>Show Details (<u>b</u>)</template>
    </IconButton>

    <!-- Get Next Button -->
    <IconButton
      v-if="examine.userHasApproverRole && !examine.isMyCurrentNr"
      @click="examine.getNextCompany"
      light
      mnemonic="n"
      data-testid="actionNextBtn"
    >
      <ChevronDoubleRightIcon class="h-5 w-5" />
      <template #text>Get&nbsp;<u>N</u>ext</template>
    </IconButton>

    <!-- Cancel Request Button -->
    <IconButton
      v-if="examine.canCancel && notHistoricalReservedConsumed"
      light
      text="Cancel Request"
      @click="showCancelDialog"
    >
      <XMarkIcon class="h-5 w-5" />
    </IconButton>

    <!-- Hold Button -->
    <IconButton
      v-if="examine.isMyCurrentNr"
      light
      @click="examine.holdRequest"
      mnemonic="h"
      data-testid="actionHoldBtn"
    >
      <PauseIcon class="h-5 w-5 stroke-2" />
      <template #text><u>H</u>old Request</template>
    </IconButton>

    <div
      v-if="showReopenAndResetButtons && notHistoricalReservedConsumed"
      class="space-x-3"
    >
      <!-- Reopen (unfurnished) Button -->
      <IconButton
        v-if="examine.furnished === 'N'"
        light
        text="Reopen"
        @click="examine.reOpen"
      >
        <PowerIcon class="h-5 w-5" />
      </IconButton>

      <!-- Reset (from furnished) Button -->
      <IconButton v-else @click="examine.resetNr" light text="Reset">
        <ArrowUturnLeftIcon class="h-5 w-5" />
      </IconButton>
    </div>

    <!-- Examine Button -->
    <IconButton
      v-if="examine.canClaim && notHistoricalReservedConsumed"
      light
      @click="examine.claimNr"
      mnemonic="x"
      data-testid="actionExamineBtn"
    >
      <DocumentCheckIcon class="h-5 w-5" />
      <template #text>E<u>x</u>amine</template>
    </IconButton>

    <PopupDialog :show="showCancelRequestDialog">
      <template #title>Cancel Name Request</template>
      <ExamineCancelRequestForm
        @submit="showCancelRequestDialog = false"
        @cancel="showCancelRequestDialog = false"
      />
    </PopupDialog>
  </div>
</template>

<script setup lang="ts">
/** Buttons for performing various actions in the examination screen, like editing, holding the request, etc.
 * Changes what buttons are displayed based on variables from the examination store
 */
import {
  ArrowUturnLeftIcon,
  ArrowsPointingInIcon,
  ArrowsPointingOutIcon,
  ChevronDoubleRightIcon,
  DocumentCheckIcon,
  PauseIcon,
  PencilSquareIcon,
  PowerIcon,
  XMarkIcon,
} from '@heroicons/vue/24/outline'
import { Status } from '~/enums/nr-status'
import { useExamination } from '~/store/examine'

const examine = useExamination()
const showCancelRequestDialog = ref(false)

/** Returns true if the NR is not historical, reserved, or consumed. */
const notHistoricalReservedConsumed = computed(
  () =>
    ![Status.Historical, Status.ConditionalReserved, Status.Reserved].includes(
      examine.nrStatus
    ) && !examine.consumptionDate
)

const showReopenAndResetButtons = computed(
  () =>
    examine.userHasEditRole &&
    examine.isComplete &&
    examine.nrStatus !== Status.Cancelled &&
    !examine.isApprovedAndExpired
)

function toggleDetails() {
  examine.isHeaderShown = !examine.isHeaderShown
}

function showCancelDialog() {
  showCancelRequestDialog.value = true
}
</script>

<style scoped>
u {
  margin: 0 !important;
}
</style>
