<template>
  <div class="text-sm">
    <ExamineRequestInfoExpandable title="Nature of Business">
      <template #minimized>
        <p>{{ examine.natureOfBusiness }}</p>
      </template>

      <template #popup>
        <p>{{ examine.natureOfBusiness }}</p>
      </template>

      <template #default>
        <p>{{ examine.natureOfBusiness }}</p>
        <div v-if="examine.prevNrRequired" class="flex items-center">
          <h2 class="font-bold">Previous NR:&nbsp;</h2>
          <span>{{ examine.previousNr }}</span>
        </div>

        <div v-if="examine.corpNumRequired" class="flex items-center">
          <h2 class="font-bold">Related Corp #:&nbsp;</h2>
          <span>{{ examine.corpNum }}</span>
        </div>
      </template>
    </ExamineRequestInfoExpandable>
  </div>
</template>

<script setup lang="ts">
import { useExamination } from '~/store/examine'
const examine = useExamination()
</script>
