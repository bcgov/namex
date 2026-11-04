<template>
  <div class="flex">
    <h2 class="font-bold">Submit:&nbsp;</h2>
    <span data-testid="submitDate">
      {{
        examine.submittedDate
          ? getDateWithTimeFromDateTime(examine.submittedDate)
          : '-'
      }}
    </span>
  </div>

  <div v-if="examine.corpNum" class="flex">
    <h2 class="font-bold">Corp Num:&nbsp;</h2>
    <span>{{ examine.corpNum }}</span>
  </div>

  <div class="flex">
    <h2 class="font-bold">Consumed:&nbsp;</h2>
    <span data-testid="consumedDate">
      {{ consumptionDateDisplay ? consumptionDateDisplay : 'n/a' }}
    </span>
  </div>

  <div class="flex">
    <h2 class="font-bold">Consumed By:&nbsp;</h2>
    <span data-testid="consumedBy">{{ examine.consumedBy ? examine.consumedBy : 'n/a' }}</span>
  </div>
</template>

<script setup lang="ts">
import { useExamination } from '~/store/examine'
import {
  getDateWithTimeFromDateTime,
  getFormattedDate,
  parseDate,
} from '~/util/date'

const examine = useExamination()

const consumptionDateDisplay = computed(() => {
  if (examine.consumptionDate && parseDate(examine.consumptionDate).isValid) {
    return getFormattedDate(examine.consumptionDate)
  }
})
</script>
