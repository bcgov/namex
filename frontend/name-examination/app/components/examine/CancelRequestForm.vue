<template>
  <div class="flex h-60 flex-col space-y-1">
    <p>Please provide comments to explain why the NR is being cancelled</p>
    <EditableTextBox
      class="grow"
      v-model="comment"
      placeholder="Write comment..."
      text-required
      @submit="handleSubmit"
      @cancel="emit('cancel')"
      @input="showSubmitError = false"
    >
      <template #confirmText>Submit</template>
      <template #errorText> A comment is required </template>
    </EditableTextBox>
  </div>
</template>

<script setup lang="ts">
/** Form for cancelling an NR */
import { useExamination } from '~/store/examine'

const emit = defineEmits<{
  submit: [text: string]
  cancel: []
}>()

const examine = useExamination()

const comment = ref('')
const showSubmitError = ref(false)

async function handleSubmit(text: string) {
  if (text === '') {
    showSubmitError.value = true
  } else {
    showSubmitError.value = false
    emit('submit', text)
    await examine.cancelNr(text)
  }
}
</script>
