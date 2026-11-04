<template>
  <div class="flex h-screen items-center justify-center">
    <TransactionsView
      v-if="nrNumber"
      :nr-number="nrNumber"
      class="w-2/3 border-x-2 border-neutral-300"
    />
    <span v-else>Invalid</span>
  </div>
</template>

<script setup lang="ts">
const nrNumber = ref()

useHead({ title: 'BC Registry: Name Examination - Transactions' })

definePageMeta({ layout: 'empty' })

onMounted(() => {
  const route = useRoute()
  const nrParam = route.query.nr as string
  nrNumber.value = `NR ${nrParam}`
})
</script>
