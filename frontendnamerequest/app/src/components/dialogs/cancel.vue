<template>
  <v-dialog
    v-if="payments"
    width="40rem"
    :value="isVisible"
    persistent
  >
    <v-card>
      <v-card-title class="d-flex justify-space-between">
        <div>Cancel Name Request</div>
        <v-btn
          icon
          large
          class="dialog-close"
          @click="hideModal()"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text class="text-body-1">
        The requested name choices will become available to be requested by other businesses.
      </v-card-text>

      <!-- FOR FUTURE USE -->
      <!-- <v-card-text class="text-body-1" v-if="emailAddress">
        An email confirming the cancellation of this Name Request will be sent to
        <strong>{{emailAddress}}</strong>.
      </v-card-text> -->

      <v-card-actions class="justify-center">
        <v-btn
          id="cancel-nr-btn"
          class="px-6 button-normal"
          :loading="loading"
          @click="confirmCancel()"
        >
          Cancel this Name Request
        </v-btn>
        <v-btn
          id="keep-nr-btn"
          class="px-6 button-blue"
          @click="hideModal()"
        >
          Keep this Name Request
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Mixins } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore, usePaymentStore } from '@/store'
import { PaymentMixin } from '@/mixins'
import { Sleep } from '@/plugins'
import { NrAction } from '@/enums'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import NamexServices from '@/services/namex-services'

@Component({})
export default class CancelDialog extends Mixins(PaymentMixin) {
  @Getter(useStore) getNrId!: number
  @Getter(usePaymentStore) cancelModalIsVisible!: boolean

  @Action(useStore) setDisplayedComponent!: ActionBindingIF
  @Action(useStore) setNameRequest!: ActionBindingIF
  @Action(usePaymentStore) toggleCancelModal!: ActionBindingIF

  /** Used to show loading state on button. */
  loading = false

  // FOR FUTURE USE
  // get emailAddress (): string {
  //   return this.getApplicant?.emailAddress
  // }

  get isVisible (): boolean {
    return this.cancelModalIsVisible
  }

  async showModal (): Promise<void> {
    await this.toggleCancelModal(true)
  }

  /** Called when user clicks "Cancel this NR" button. */
  async confirmCancel (): Promise<void> {
    this.loading = true
    const data = await NamexServices.patchNameRequestsByAction(this.getNrId, NrAction.CANCEL)
    if (data) {
      this.setNameRequest(data)
      this.loading = false
      await this.hideModal()
      this.setDisplayedComponent('Success')
      await Sleep(1000)
      this.setDisplayedComponent('ExistingRequestDisplay')
    } else {
      this.loading = false
      await this.hideModal()
    }
  }

  /** Called when user clicks "Keep this NR" button. */
  async hideModal (): Promise<void> {
    await this.toggleCancelModal(false)
  }
}
</script>
