<template>
  <div class="flex flex-col space-y-4">
    <div class="flex flex-col space-y-2 grow">
      <ExamineDecisionHeader />

      <ExamineDecisionConditionsInfo :conditions="examine.conditions" />

      <div class="!mt-4 flex space-x-2 h-[70%]">
        <!-- Layout the combo selects in reverse so they don't overlap each other https://stackoverflow.com/a/77210506 -->
        <div class="flex basis-1/2 flex-col-reverse justify-between">
          <ExamineDecisionSelectTrademarks />
          <ExamineDecisionSelectMacros />
          <ExamineDecisionSelectConflicts />
          <ExamineDecisionSelectConditions />
        </div>

        <ExamineDecisionRequestorMessage />
      </div>
    </div>

    <ExamineDecisionButtons />
  </div>
</template>

<script setup lang="ts">
/** The decision area */
import { useExamination } from '~/store/examine'
const examine = useExamination()
</script>
