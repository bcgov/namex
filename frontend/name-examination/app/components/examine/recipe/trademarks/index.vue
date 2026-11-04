<template>
  <ExamineRecipeTable
    class="h-full w-full"
    :columns="['Name', 'Description', 'Status']"
    :rows="rows"
    :highlight-row="highlightRow"
  />
</template>

<script setup lang="ts">
import { useExamination } from '~/store/examine'
const examine = useExamination()

type Row = [name: string, description: string, status: string]

const rows = computed<Array<Row>>(() =>
  examine.trademarks.map((tm) => [tm.name, tm.description, tm.status])
)

/** Return a unique string identifier for a trademark */
function hashTrademark(trademarkName: string, trademarkDesc: string): string {
  return trademarkName + trademarkDesc
}

const selectedTrademarkNames = computed(() =>
  examine.selectedTrademarks.map((t) => hashTrademark(t.name, t.description))
)

const highlightRow = (row: Array<any>) =>
  selectedTrademarkNames.value.includes(hashTrademark(row[0], row[1]))
</script>
