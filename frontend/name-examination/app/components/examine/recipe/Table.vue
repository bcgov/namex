<template>
  <table class="text-sm">
    <thead>
      <tr class="border-b-2 text-left text-gray-600">
        <th v-for="column in columns" class="px-4 py-2 font-normal">
          {{ column }}
        </th>
      </tr>
    </thead>

    <tbody class="text-sm">
      <!--
        Generate two <tr> elements for every row passed in:
        One contains the actual row data corresponding to the columns
        The second is optional content that is displayed when the row is expanded (i.e. clicked)
        The content is passed in by the user of this component with slots, so it can be any element
       -->
      <template v-if="rows.length > 0" v-for="(row, index) in rows">
        <tr
          :class="[
            'cursor-pointer transition hover:bg-gray-100',
            { 'bg-sky-100 hover:bg-sky-100': selectedRow === index },
            { '!bg-green-100': highlightRow ? highlightRow(row) : false },
          ]"
          @click="onRowClick(index, row)"
        >
          <td v-for="cell in row" class="px-4 py-2">{{ cell }}</td>
        </tr>
        <tr v-if="selectedRow === index && showSelectedRowHiddenContent">
          <td class="p-0" :colspan="columns.length">
            <div :class="{ 'border-0 bg-sky-100': selectedRow === index }">
              <slot :index="index" :row="row"></slot>
            </div>
          </td>
        </tr>
      </template>

      <tr v-else>
        <td :colspan="columns.length">
          <div class="flex w-full justify-center p-2">No data available</div>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
type Row = Array<any>

defineProps<{
  columns: Array<string>
  rows: Array<Row>
  /** Function for determining whether a row should be permanently highlighted or not */
  highlightRow?: (row: Row) => boolean
}>()

const emit = defineEmits<{
  rowClick: [row: Array<any>]
}>()

const selectedRow = ref()
const showSelectedRowHiddenContent = ref(false)

function onRowClick(index: number, row: Array<any>) {
  if (selectedRow.value === index) {
    showSelectedRowHiddenContent.value = !showSelectedRowHiddenContent.value
  } else {
    selectedRow.value = index
    showSelectedRowHiddenContent.value = true
  }
  emit('rowClick', row)
}
</script>
