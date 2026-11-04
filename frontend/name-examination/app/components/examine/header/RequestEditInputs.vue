<template>
  <div>
    <ListSelect
      v-model="selectedRequestType"
      :options="examine.listRequestTypes"
      :options-display="(rt: RequestType) => rt.text"
      @change="onRequestTypeChanged"
      aria-label="Name Request Type"
      testID="editCompanyTypeDropdown"
    >
      {{ selectedRequestType.text }}
    </ListSelect>

    <div class="flex flex-col space-x-1">
      <div v-if="examine.jurisdictionRequired" class="flex flex-col">
        <label for="jurisdiction" class="text-sm font-bold">
          Jurisdiction
        </label>
        <ListSelect
          id="jurisdiction"
          v-model="jurisdiction"
          :options="examine.listJurisdictions.map((j) => j.text)"
          @change="jursidictionErrorText = ''"
          :error-style="jursidictionErrorText != ''"
        >
          {{ jurisdiction ? jurisdiction : 'Select' }}
        </ListSelect>
        <span class="text-sm font-bold text-red-600">
          {{ jursidictionErrorText }}
        </span>
      </div>

      <div v-if="examine.corpNumRequired" class="flex flex-col py-0.5">
        <label for="corpNum" class="text-sm font-bold">Related Corp #</label>
        <TextInput
          id="corpNum"
          v-model="corpNum"
          placeholder="Corp Number"
          :error-style="corpNumError"
          @input="corpNumErrorText = ''"
        />
        <span class="text-sm font-bold text-red-600">
          {{ corpNumErrorText }}
        </span>
      </div>

      <div v-if="examine.prevNrRequired" class="flex flex-col">
        <label for="prevNr" class="text-sm font-bold"> Previous NR</label>
        <TextInput
          id="prevNr"
          v-model="previousNr"
          placeholder="NR Number"
          :error-style="previousNrErrorText != ''"
          @input="previousNrErrorText = ''"
        />

        <span class="text-sm font-bold text-red-600">
          {{ previousNrErrorText }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useExamination } from '~/store/examine'
import type { RequestType } from '~/types'
import {
  corpExists,
  isValidCorpNumFormat,
  isValidNrFormat,
  nrExists,
} from '~/util'

const examine = useExamination()

const selectedRequestType = ref(examine.requestTypeObject)

const jurisdiction = ref(examine.jurisdiction)
const jursidictionErrorText = ref('')

const corpNum = ref(examine.corpNum)
const corpNumErrorText = ref('')
const corpNumError = computed(() => corpNumErrorText.value != '')

const previousNr = ref(examine.previousNr)
const previousNrErrorText = ref('')

function resetErrorTexts() {
  jursidictionErrorText.value = ''
  corpNumErrorText.value = ''
  previousNrErrorText.value = ''
}

function resetInputs() {
  jurisdiction.value = undefined
  corpNum.value = undefined
  previousNr.value = undefined
}

function setDefaultInputValues() {
  jurisdiction.value = examine.jurisdiction
  corpNum.value = examine.corpNum
  previousNr.value = examine.previousNr
  selectedRequestType.value = examine.requestTypeObject
}

function trimInputs() {
  corpNum.value = corpNum.value?.trim()
  previousNr.value = previousNr.value?.trim()
}

function onRequestTypeChanged(newRequestType: RequestType) {
  resetInputs()
  resetErrorTexts()
  examine.updateRequestTypeRules(newRequestType)
}

async function validateCorpNum(corpNum: string) {
  if (!isValidCorpNumFormat(corpNum)) {
    corpNumErrorText.value = 'Invalid corp number format'
    return false
  }
  try {
    if (!(await corpExists(corpNum))) {
      corpNumErrorText.value = 'Could not find corp in database'
      return false
    } else {
      return true
    }
  } catch (e) {
    corpNumErrorText.value = 'Failed to check corp number. Please try again.'
    return false
  }
}

async function validatePreviousNr(previousNr: string) {
  if (!isValidNrFormat(previousNr)) {
    previousNrErrorText.value = 'NR number format must be NR xxxxxxx'
    return false
  } else if (!(await nrExists(previousNr))) {
    previousNrErrorText.value = 'Could not find NR in database'
    return false
  } else {
    return true
  }
}

async function validateInputs() {
  const validationResults = []
  if (examine.jurisdictionRequired && jurisdiction.value == null) {
    jursidictionErrorText.value = 'Please select a jurisdiction'
    validationResults.push(false)
  }
  if (examine.corpNumRequired && corpNum.value) {
    validationResults.push(await validateCorpNum(corpNum.value))
  }
  if (examine.prevNrRequired && previousNr.value) {
    validationResults.push(await validatePreviousNr(previousNr.value))
  }
  return validationResults.every((r) => r === true)
}

examine.addEditAction({
  async validate() {
    resetErrorTexts()
    if (examine.isClosed) {
      return true
    }
    trimInputs()
    return await validateInputs()
  },
  update() {
    examine.requestType = selectedRequestType.value.value
    if (examine.jurisdictionRequired) {
      examine.jurisdiction = jurisdiction.value
    } else {
      examine.jurisdiction = undefined
    }
    if (examine.corpNumRequired && corpNum.value) {
      examine.corpNum = corpNum.value
    } else {
      examine.corpNum = undefined
    }
    if (examine.prevNrRequired && previousNr.value) {
      examine.previousNr = previousNr.value
    } else {
      examine.previousNr = undefined
    }
  },
  cancel: setDefaultInputValues,
})

onMounted(() => {
  examine.updateRequestTypeRules(examine.requestTypeObject)
})
</script>
