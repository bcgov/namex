<template>
  <div class="flex items-center">
    <h2 class="font-bold">Expiry:&nbsp;</h2>
    <span v-if="!examine.expiryDate">n/a</span>
    <div v-else class="flex flex-col">
      <DateInput
        min-today
        v-model="expiry"
        :error-style="expiryDateErrorText != ''"
        @change="expiryDateErrorText = ''"
      />
      <span class="text-sm font-bold text-red-600">
        {{ expiryDateErrorText }}
      </span>
    </div>
  </div>

  <div v-if="examine.nrStatus === Status.Conditional">
    <div class="flex flex-col space-y-1">
      <div class="flex items-center">
        <h2 class="font-bold">Consent:&nbsp;</h2>
        <ListSelect
          class="w-1/2"
          v-model="consentFlag"
          :options="consentOptions"
          :options-display="(option: ConsentFlag | undefined) => option ? consentDisplayStrings[option] : 'Empty'"
        >
          {{ selectedConsentOptionText ? selectedConsentOptionText : 'Empty' }}
        </ListSelect>
      </div>

      <div
        v-if="consentFlag === ConsentFlag.Received"
        class="flex items-center"
      >
        <h2 class="font-bold">Consent Date:&nbsp;</h2>
        <div class="flex flex-col">
          <DateInput
            v-model="consentDate"
            :error-style="consentDateErrorText != ''"
            @change="consentDateErrorText = ''"
          />
          <span class="text-sm font-bold text-red-600">
            {{ consentDateErrorText }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DateTime } from 'luxon'
import { ConsentFlag } from '~/enums/codes'
import { Status } from '~/enums/nr-status'
import { useExamination } from '~/store/examine'

const examine = useExamination()

const expiry = ref<string>()
const consentFlag = ref<ConsentFlag>()
const consentDate = ref<string>()

const expiryDateErrorText = ref('')
const consentDateErrorText = ref('')

const consentOptions = computed(() => [
  ...Object.values(ConsentFlag),
  undefined,
])

const consentDisplayStrings = {
  [ConsentFlag.Required]: 'Required',
  [ConsentFlag.Received]: 'Received',
  [ConsentFlag.Waived]: 'Waived',
}

const selectedConsentOptionText = computed(() =>
  consentFlag.value ? consentDisplayStrings[consentFlag.value] : undefined
)

function setDefaultInputValues() {
  expiry.value = examine.expiryDate
  consentFlag.value = examine.consentFlag
  consentDate.value = examine.consentDate ?? DateTime.now().toISODate()
}

examine.addEditAction({
  validate() {
    let isValid = true
    if (examine.expiryDate) {
      if (expiry.value) {
        isValid = DateTime.fromISO(expiry.value).startOf('day') >= DateTime.now().startOf('day')
        expiryDateErrorText.value = isValid ? '' : 'Expiry date must be today or later';
      } else {
        expiryDateErrorText.value = 'Expiry date is required'
        isValid = false
      }
    }

    if (consentFlag.value === ConsentFlag.Received && !consentDate.value) {
      consentDateErrorText.value = 'Consent date is required'
      isValid = false
    }
    return isValid
  },
  update() {
    examine.expiryDate = expiry.value

    if (examine.nrStatus === Status.Conditional) {
      examine.consentFlag = consentFlag.value
    } else {
      examine.consentFlag = undefined
    }

    if (examine.consentFlag === ConsentFlag.Received) {
      examine.consentDate = consentDate.value
    } else {
      examine.consentDate = undefined
    }
  },
  cancel: setDefaultInputValues,
})

onMounted(() => {
  setDefaultInputValues()
})
</script>
