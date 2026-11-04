<template>
  <div class="divide-y divide-neutral-400 border-y border-neutral-400">
    <div v-for="name in names" class="grid grid-cols-4 py-2">
      <span>Name {{ name.choice }}</span>
      <ExamineNamesListChoice
        class="col-span-3"
        :choice="name"
        :decision-text="name.decision_text || ''"
        indicate-draft
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { NameChoice } from '~/types'

defineProps<{
  names: Array<NameChoice>
}>()
</script>
