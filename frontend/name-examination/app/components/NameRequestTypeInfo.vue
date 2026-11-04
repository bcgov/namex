<template>
  <div class="flex flex-col justify-center font-bold">
    <p data-testid="nrType">
      {{ requestTypeText }}
    </p>
    <p v-if="jurisdiction">
      {{ jurisdictionDisplay }}
    </p>
  </div>
</template>

<script setup lang="ts">
/** Displays a given request type and jurisdiction (if applicable) */
import jurisdictionsData from '~/data/jurisdictions.json'

const props = defineProps<{
  requestTypeText: string
  jurisdiction?: string
  jurisdictionNumber?: string
}>()

const jurisdictionDisplay = computed(() => {
  let text = props.jurisdiction
  if (text?.length === 2) {
    // if the jurisdiction name is two letters, it's likely a code for a province, so get the full name
    const province = jurisdictionsData.find(
      (j) => j.value === props.jurisdiction
    )
    if (province) {
      text = province.text
    }
  }
  if (props.jurisdictionNumber) {
    text = `${text} (${props.jurisdictionNumber})`
  }
  return text
})
</script>
