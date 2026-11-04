<template>
  <div class="flex items-center space-x-3">
    <IconButton
      :disabled="savingEdit"
      light
      mnemonic="s"
      @click="save"
      class="w-1/2 whitespace-pre py-1"
      data-testid="actionSaveBtn"
    >
      <CheckIcon v-if="!savingEdit" class="h-5 w-5 stroke-2" />
      <ArrowPathIcon v-else class="mr-0.5 h-5 w-5 animate-spin stroke-2" />
      <template #text><u>S</u>ave Edits</template>
    </IconButton>

    <IconButton
      :disabled="savingEdit"
      light
      mnemonic="c"
      @click="examine.cancelEdits"
      class="w-1/2 py-1"
      data-testid="actionCancelBtn"
    >
      <XMarkIcon class="h-5 w-5 stroke-2" />
      <template #text><u>C</u>ancel</template>
    </IconButton>
  </div>
</template>

<script setup lang="ts">
/** Save/cancel buttons for the edit request view. */
import { useExamination } from '~/store/examine'
import { ArrowPathIcon, CheckIcon, XMarkIcon } from '@heroicons/vue/24/outline'

const examine = useExamination()

const savingEdit = ref(false)

async function save() {
  savingEdit.value = true
  await examine.saveEdits()
  savingEdit.value = false
}
</script>
