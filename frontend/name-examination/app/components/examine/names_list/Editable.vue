<template>
  <ol class="ml-4 basis-1/3 list-decimal space-y-2">
    <li v-for="(_input, i) in nameInputs">
      <TextInput
        v-model="nameInputs[i]"
        @input="clearErrorOnInput(i)"
        :error-style="errorMessage?.choice === i"
        :data-testid="`editNameChoiceTxt${i + 1}`"
      />
      <span
        v-if="errorMessage && errorMessage.choice === i"
        class="text-sm font-bold text-red-600"
      >
        {{ errorMessage.text }}
      </span>
    </li>
  </ol>
</template>

<script setup lang="ts">
/** Displays a list of editable name choices */
import { useExamination } from '~/store/examine'

const examine = useExamination()

const nameInputs = ref(examine.nameChoices.map((nc) => nc.name ?? ''))

const errorMessage = ref<{ choice: number; text: string }>()

function clearErrorOnInput(inputChoice: number) {
  if (errorMessage.value?.choice === inputChoice) {
    errorMessage.value = undefined
  }
}

examine.addEditAction({
  validate() {
    if (!nameInputs.value[0]) {
      errorMessage.value = {
        choice: 0,
        text: 'The first name choice is required',
      }
      return false
    }
    if (nameInputs.value[2] && !nameInputs.value[1]) {
      errorMessage.value = {
        choice: 1,
        text: 'To include a 3rd name choice the 2nd name choice is first required',
      }
      return false
    }
    if (
      examine.currentChoice &&
      !nameInputs.value[examine.currentChoice - 1].trim()
    ) {
      errorMessage.value = {
        choice: examine.currentChoice - 1,
        text: 'Cannot clear currently examining name',
      }
      return false
    }
    return true
  },
  update() {
    for (const [i, choice] of examine.nameChoices.entries()) {
      const oldName = choice.name?.slice()
      choice.name = nameInputs.value[i].trim()
      if (examine.currentChoice === choice.choice && choice.name !== oldName) {
        examine.fetchAndLoadRecipeData(examine.currentName || '', '')
      }
    }
  },
  cancel() {},
})
</script>
