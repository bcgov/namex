<template>
  <form
    @submit.prevent="emit('submit', startDate, endDate)"
    class="flex w-fit flex-col"
  >
    <label for="start_date" class="font-medium">Start date: </label>
    <DateInput v-model="startDate" id="start_date" :max="endDate" required />

    <label for="end_date" class="font-medium">End date: </label>
    <DateInput v-model="endDate" id="end_date" :min="startDate" required />

    <div class="mt-6 space-x-2">
      <IconButton white type="submit" class="px-3">Ok</IconButton>
      <IconButton white @click="emit('cancel')">Cancel</IconButton>
    </div>
  </form>
</template>

<script setup lang="ts">
/** Form for choosing a date range. */
const props = defineProps<{
  initialStart: string
  initialEnd: string
}>()

const emit = defineEmits<{
  (e: 'submit', startDate: string, endDate: string): void
  (e: 'cancel'): void
}>()

const startDate = ref(props.initialStart)
const endDate = ref(props.initialEnd)
</script>
