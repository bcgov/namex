<template>
  <div>
    <p>{{ examine.firstName }} {{ examine.lastName }}</p>
    <p>{{ examine.addressLine1 }}</p>
    <p v-if="examine.addressLine2">{{ examine.addressLine2 }}</p>
    <p v-else-if="examine.addressLine3">{{ examine.addressLine3 }}</p>
    <p v-else>
      {{ examine.city }} {{ examine.province }} {{ examine.postalCode }}
      {{ examine.country }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { useExamination } from '~/store/examine'
const examine = useExamination()
</script>
