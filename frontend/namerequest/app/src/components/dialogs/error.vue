<template>
  <v-dialog v-model="showModal">
    <v-card>
      <v-card-title class="d-flex justify-space-between">
        <div v-if="isEditLockError">
          Changes Temporarily Unavailable
        </div>
        <div v-else>
          Name Request encountered an error
        </div>
      </v-card-title>
      <div v-if="isEditLockError">
        <v-card-text class="copy-normal pt-8">
          Another user may be making updates to this Name Request and this action is unavailable
          at this time. Please try again later. Typical reasons are as follows:
          <br>
          <br>
          <ul>
            <li>Another user may be editing this name request</li>
            <li>BC Registries staff may be currently reviewing this Name Request</li>
            <li>Status of this Name Request has changed</li>
          </ul>
          <br>
          <br>
          For assistance, please contact BC Registries staff:
        </v-card-text>
      </div>
      <div v-else-if="isExists">
        <v-card-text class="copy-normal pt-8">
          You have already created an identical name request. Please wait for the system to complete
          processing the submission. If you are requesting identical names for DBA purposes, please
          wait 2 minutes between each submission.
          <br>
          <br>
          For assistance, please contact BC Registries staff:
        </v-card-text>
      </div>
      <div v-else>
        <v-card-text class="copy-normal pt-8">
          If you have paid for a new NR, please do not try submitting your payment again.
        </v-card-text>

        <v-card-text class="copy-normal pt-6">
          If your payment was successful, you should receive a receipt by email within 1 hour.
          If you do not receive the email, please contact BC Registries staff:
        </v-card-text>
      </div>
      <v-card-text class="copy-normal pt-6">
        <ContactInfo direction="col" />
      </v-card-text>

      <v-card-actions class="justify-center pt-8">
        <v-btn
          text
          class="px-8"
          @click="hideModal()"
        >
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useErrorStore } from '@/store'
import ContactInfo from '@/components/common/contact-info.vue'
import { ErrorI } from '@/interfaces'

@Component({
  components: { ContactInfo }
})
export default class ErrorDialog extends Vue {
  @Getter(useErrorStore) hasErrors!: boolean
  @Getter(useErrorStore) getErrors!: () => ErrorI[]
  @Action(useErrorStore) clearAppErrors!: () => void

  get showModal () {
    return this.hasErrors
  }

  async hideModal () {
    await this.clearAppErrors()
  }

  get isExists () {
    const errors = this.getErrors
    return errors[0] && errors[0].id === 'entry-already-exists'
  }

  get isEditLockError () {
    const errors = this.getErrors
    return errors[0] && errors[0].id === 'edit-lock-error'
  }
}
</script>

<style lang="scss" scoped>
::v-deep .v-dialog {
  width: 45rem;
  min-width: 33rem;
}
</style>
