<template>
  <div class="flex flex-col gap-y-2">
    <div v-if="examine.clientFirstName || examine.clientLastName">
      <h3 class="font-bold">Client</h3>
      <p data-testid="clientName">{{ examine.clientFirstName }} {{ examine.clientLastName }}</p>
    </div>

    <div v-if="examine.firstName || examine.lastName">
      <h3 class="font-bold">Applicant</h3>
      <p data-testid="applicantName">{{ examine.firstName }} {{ examine.lastName }}</p>
    </div>

    <div>
      <h3 class="font-bold">Address</h3>
      <p data-testid="addressLine1">{{ examine.addressLine1 }}</p>
      <p data-testid="addressLine2">{{ examine.addressLine2 }}</p>
      <p data-testid="addressLine3">{{ examine.addressLine3 }}</p>
      <p data-testid="addressCityProvince">{{ examine.city }} {{ examine.province }}</p>
      <p data-testid="addressPostalCode">{{ examine.postalCode }}</p>
      <p data-testid="addressCountry">{{ examine.country }}</p>
    </div>

    <div v-if="examine.phone">
      <h3 class="font-bold">Phone</h3>
      <p data-testid="phone">{{ examine.phone }}</p>
    </div>

    <div v-if="examine.fax">
      <h3 class="font-bold">Fax</h3>
      <p data-testid="fax">{{ examine.fax }}</p>
    </div>

    <div v-if="examine.conEmail">
      <h3 class="font-bold">Email</h3>
      <p data-testid="email">{{ examine.conEmail }}</p>
    </div>

    <div v-if="examine.contactName">
      <h3 class="font-bold">Contact</h3>
      <p data-testid="contact">{{ examine.contactName }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useExamination } from '~/store/examine'
const examine = useExamination()
</script>
