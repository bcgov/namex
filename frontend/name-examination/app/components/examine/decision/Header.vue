<template>
  <div class="flex">
    <h2 class="text-2xl font-bold">Decision</h2>

    <label class="ml-auto flex items-center space-x-1" for="consent">
      <input
        id="consent"
        class="h-4 w-4"
        type="checkbox"
        v-model="examine.consentRequired"
        data-testid="consentCheckbox"
      />
      <span>Consent</span>
    </label>
  </div>
</template>

<script setup lang="ts">
/** Decision area header and consent flag checkbox */
import { useExamination } from '~/store/examine'
const examine = useExamination()
</script>
