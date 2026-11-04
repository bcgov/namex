<template>
  <div class="flex flex-col">
    <div class="flex items-center">
      <span
        class="mr-2 flex flex-col"
        :class="{
          'font-bold': (current || choiceApproved) && highlight,
          'text-bcgov-blue3': choiceApproved && highlight,
        }"
       :data-testid="testID && `${testID}-text`"
      >
        {{ choice.name }}
      </span>

      <span v-if="choiceApproved" :data-testid="`${testID}-checkmark`">
        <CheckIcon class="h-5 w-5 stroke-2 text-lime-600" />
      </span>
      <span v-else-if="choice.state === Status.Rejected" :data-testid="`${testID}-xmark`">
        <XMarkIcon class="h-5 w-5 stroke-2 text-red-600" />
      </span>
      <span v-else-if="indicateDraft" class="italic">(Draft)</span>
      
      <IconButton
        v-if="undoable"
        @click="undo?.(choice)"
        white
        text="Undo Decision"
        class="border-none text-sm text-blue-800 !px-1.5"
      />
    </div>

    <span
      class="max-w-1/2 text-sm"
      :class="{
        'text-[#1359A0]': choiceApproved && highlight,
      }"
      :data-testid="`${testID}-decisiontxt`"
    >
      {{ choice.decision_text }}
    </span>
  </div>
</template>

<script setup lang="ts">
/** Component for showing a single name choice */
import { CheckIcon, XMarkIcon } from '@heroicons/vue/24/outline'
import { Status } from '~/enums/nr-status'
import type { NameChoice } from '~/types'

const props = defineProps<{
  choice: NameChoice
  /** Decision text for this name choice, shown under the name */
  decisionText: string
  /** Whether this choice is undoable */
  undoable?: boolean
  /** Function called when the user requests to undo this name choice */
  undo?: (choice: NameChoice) => Promise<void>
  /** Whether this choice is the current one being examined */
  current?: boolean
  highlight?: boolean
  indicateDraft?: boolean
  testID?: string
}>()

const choiceApproved = computed(
  () =>
    props.choice.state === Status.Approved ||
    props.choice.state === Status.Condition
)
</script>
