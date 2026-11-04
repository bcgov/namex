<template>
  <div class="flex flex-col gap-y-1">
    <h3 class="font-bold">Client</h3>
    <TextInput
      v-model="clientFirstName"
      placeholder="First Name"
      maxlength="200"
      data-testid="editClientFirstNameTxt"
    />
    <TextInput
      v-model="clientLastName"
      placeholder="Last Name"
      maxlength="200"
      data-testid="editClientLastNameTxt"
    />

    <h3 class="font-bold">Applicant</h3>
    <TextInput 
      v-model="firstName" 
      placeholder="First Name" 
      maxlength="200" 
      data-testid="editApplicantFirstNameTxt"
    />
    <TextInput 
      v-model="middleName" 
      placeholder="Middle Name" 
      maxlength="200" 
      data-testid="editApplicantMiddleNameTxt"
    />
    <TextInput
      v-model="lastName"
      placeholder="Last Name"
      maxlength="200"
      :error-style="lastNameErrorText != ''"
      @input="lastNameErrorText = ''"
      data-testid="editApplicantLastNameTxt"
    />
    <p class="font-bold text-red-600">{{ lastNameErrorText }}</p>

    <h3 class="font-bold">Address</h3>
    <TextInput 
      v-model="addressLine1" 
      placeholder="Line 1" 
      maxlength="200" 
      data-testid="editApplicantAddressTxt1"
    />
    <TextInput 
      v-model="addressLine2" 
      placeholder="Line 2" 
      maxlength="200" 
      data-testid="editApplicantAddressTxt2"
    />
    <TextInput 
      v-model="addressLine3" 
      placeholder="Line 3" 
      maxlength="200" 
      data-testid="editApplicantAddressTxt3"
    />
    <div class="flex gap-x-1">
      <TextInput
        v-model="city"
        placeholder="City"
        class="basis-2/3"
        maxlength="200"
        data-testid="editApplicantCityTxt"
      />
      <TextInput
        v-model="province"
        placeholder="Province"
        class="basis-1/3"
        maxlength="2"
        data-testid="editApplicantProvinceTxt"
      />
    </div>

    <div class="flex gap-x-1">
      <TextInput
        v-model="postalCode"
        placeholder="Postal Code"
        class="basis-2/3"
        maxlength="20"
        data-testid="editApplicantPostalCodeTxt"
      />
      <TextInput
        v-model="country"
        placeholder="Country"
        class="basis-1/3"
        maxlength="2"
        data-testid="editApplicantCountryTxt"
      />
    </div>

    <h3 class="font-bold">Phone</h3>
    <TextInput 
      v-model="phone" 
      placeholder="Phone Number" 
      maxlength="30" 
      data-testid="editApplicantPhoneTxt"
    />

    <h3 class="font-bold">Fax</h3>
    <TextInput 
      v-model="fax" 
      placeholder="Fax Number" 
      maxlength="30" 
      data-testid="editApplicantFaxTxt"
    />

    <h3 class="font-bold">Email</h3>
    <TextInput 
      v-model="conEmail" 
      placeholder="Contact Email" 
      maxlength="75" 
      data-testid="editApplicantEmailTxt"
    />

    <h3 class="font-bold">Contact</h3>
    <TextInput
      v-model="contactName"
      placeholder="Contact Name"
      maxlength="200"
      data-testid="editApplicantContactTxt"
    />
  </div>
</template>

<script setup lang="ts">
import { useExamination } from '~/store/examine'
const examine = useExamination()

const clientFirstName = ref(examine.clientFirstName)
const clientLastName = ref(examine.clientLastName)
const firstName = ref(examine.firstName)
const middleName = ref(examine.middleName)
const lastName = ref(examine.lastName)
const addressLine1 = ref(examine.addressLine1)
const addressLine2 = ref(examine.addressLine2)
const addressLine3 = ref(examine.addressLine3)
const city = ref(examine.city)
const province = ref(examine.province)
const postalCode = ref(examine.postalCode)
const country = ref(examine.country)
const phone = ref(examine.phone)
const fax = ref(examine.fax)
const conEmail = ref(examine.conEmail)
const contactName = ref(examine.contactName)

const lastNameErrorText = ref('')
const lastNameEmpty = computed(() => lastName.value?.trim().length === 0)

examine.addEditAction({
  validate: () => {
    if (lastNameEmpty.value) {
      lastNameErrorText.value = 'Last name cannot be empty'
      return false
    }
    return true
  },
  update: () => {
    examine.clientFirstName = clientFirstName.value
    examine.clientLastName = clientLastName.value
    examine.firstName = firstName.value
    examine.middleName = middleName.value
    examine.lastName = lastName.value
    examine.addressLine1 = addressLine1.value
    examine.addressLine2 = addressLine2.value
    examine.addressLine3 = addressLine3.value
    examine.city = city.value
    examine.province = province.value
    examine.postalCode = postalCode.value
    examine.country = country.value
    examine.phone = phone.value
    examine.fax = fax.value
    examine.conEmail = conEmail.value
    examine.contactName = contactName.value
  },
  cancel() {},
})
</script>
