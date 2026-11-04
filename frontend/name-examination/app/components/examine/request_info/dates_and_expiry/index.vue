<template>
  <div class="flex flex-col overflow-auto py-1 text-sm">
    <ExamineRequestInfoDatesAndExpiryBase />
    <ExamineRequestInfoDatesAndExpiryAndConsent v-if="!examine.isEditing" />
    <ExamineRequestInfoDatesAndExpiryAndConsentEditable v-else />
  </div>
</template>

<script setup lang="ts">
import { useExamination } from '~/store/examine'

const examine = useExamination()
</script>
