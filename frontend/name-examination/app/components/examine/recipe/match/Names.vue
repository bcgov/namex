<template>
  <div class="flex flex-col space-y-2 p-2 text-sm">
    <div class="flex space-x-2">
      <div class="grid basis-2/3 grid-cols-[30%_70%] overflow-x-auto">
        <h3 class="font-bold">Applicant</h3>
        <div>
          <p>
            {{ applicants.firstName }}
            {{ applicants.lastName }}
          </p>
          <p>{{ applicants.addrLine1 }}</p>
          <p>{{ applicants.addrLine2 }}</p>
          <p>{{ applicants.addrLine3 }}</p>
          <p>
            {{ applicants.city }}
            {{ applicants.stateProvinceCd }}
            {{ applicants.postalCd }}
            {{ applicants.countryTypeCd }}
          </p>
        </div>

        <h3 class="font-bold">Phone</h3>
        <p>{{ applicants.phoneNumber }}</p>

        <h3 class="font-bold">Email</h3>
        <p>{{ applicants.emailAddress }}</p>
      </div>

      <div class="grid basis-1/3 grid-cols-2 overflow-x-auto">
        <h3 class="font-bold" v-if="clientExists">Client</h3>
        <p v-if="clientExists">
          {{ applicants.clientFirstName }} {{ applicants.clientLastName }}
        </p>

        <h3 class="font-bold" v-if="applicants.contact">Contact</h3>
        <p v-if="applicants.contact">{{ applicants.contact }}</p>

        <h3 class="font-bold">Name State</h3>
        <p>{{ conflict.state }}</p>
      </div>
    </div>

    <div v-if="conflict.comments && conflict.comments.length > 0">
      <h3 class="font-bold">Comments</h3>
      <ExamineCommentsBox
        :comments="conflict.comments"
        class="max-h-48 overflow-auto rounded border border-gray-400 p-2 children:bg-sky-50"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { NameRequest } from '~/types'

const { conflict } = defineProps<{
  conflict: NameRequest
}>()

const applicants = conflict.applicants

const clientExists = computed(
  () => applicants.clientFirstName || applicants.clientLastName
)
</script>
