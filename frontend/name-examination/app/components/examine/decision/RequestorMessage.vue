<template>
  <div class="flex basis-1/2 flex-col space-y-2">
    <div class="flex justify-between">
      <h3 class="font-semibold">
        Message To Requestor
        <span
          v-if="examine.customerMessageOverride"
          class="font-bold text-red-600"
        >
          (Edited)
        </span>
      </h3>
      <div class="flex h-7 space-x-1">
        <IconButton
          v-if="examine.customerMessageOverride"
          white
          text="Clear"
          @click="clearEdits"
        >
          <BackspaceIcon class="h-5 w-5" />
        </IconButton>
        <IconButton white text="Edit" @click="showEditDialog()">
          <PencilSquareIcon class="h-5 w-5" />
        </IconButton>
      </div>
    </div>
    <EditableTextBox
      class="grow"
      v-model="examine.requestorMessage"
      readonly
      hide-submit
      hide-cancel
      :character-limit="characterLimit"
      :key="key"
    />
    <span
      v-if="examine.requestorMessage.length > characterLimit"
      class="text-sm font-bold text-red-600"
    >
      {{ characterLimitDisplay }}
    </span>
  </div>

  <PopupDialog :show="showEditRequestorMessageDialog">
    <template #title>Edit Message</template>
    <div class="flex flex-col">
      <EditableTextBox
        class="h-72"
        v-model="customerMessageOverrideTemp"
        :character-limit="characterLimit"
        @submit="onRequestorMessageSubmit()"
        @cancel="onRequestorMessageCancel()"
      />

      <span
        v-if="customerMessageOverrideTemp!.length > characterLimit"
        class="text-sm font-bold text-red-600"
      >
        {{ characterLimitDisplay }}
      </span>
    </div>
  </PopupDialog>
</template>

<script setup lang="ts">
/** Component for showing the requestor message, shows a popup dialog when editing it */
import { useExamination } from '~/store/examine'
import { BackspaceIcon, PencilSquareIcon } from '@heroicons/vue/24/outline'

let key = ref(0)
const examine = useExamination()

// we need this work-around to make the text box update its output
// whenever Requestor Message changes; for some reason, it's not
// reacting normally
watch(
    () => [examine.requestorMessage],
    async (_state) => {
      key.value++
    }
  )

const characterLimit = 955
const characterLimitDisplay = `Message cut off at ${characterLimit} characters`

const showEditRequestorMessageDialog = ref(false)

const customerMessageOverrideTemp = ref(examine.customerMessageOverride || '')

function showEditDialog() {
  showEditRequestorMessageDialog.value = true
  customerMessageOverrideTemp.value = examine.requestorMessage
}

function onRequestorMessageSubmit() {
  showEditRequestorMessageDialog.value = false
  if (customerMessageOverrideTemp.value !== examine.requestorMessage)
    examine.customerMessageOverride = customerMessageOverrideTemp.value
}

function onRequestorMessageCancel() {
  showEditRequestorMessageDialog.value = false
}

function clearEdits() {
  examine.customerMessageOverride = undefined
}
</script>
