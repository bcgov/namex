<template>
  <v-dialog
    v-model="showModal"
    max-width="45rem"
  >
    <v-card>
      <v-card-title class="d-flex justify-space-between">
        <div>Payment Not Received</div>
        <div class="mt-3">
          <v-btn
            icon
            large
            class="dialog-close"
            @click="hideModal()"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
      </v-card-title>

      <v-card-text class="copy-normal pt-8">
        <p>
          The payment for this Name Request was not received; leaving this page will result in
          this Name Request being deleted from BC Registries. Stay on this page to retry payment.
        </p>
        <br>
        <p>
          If your Name Request is deleted you will need to resubmit your name(s) with a new Name Request.
        </p>
      </v-card-text>

      <v-card-actions class="justify-center pt-6">
        <v-btn
          class="px-12"
          @click="exit()"
        >
          OK
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import { DisplayedComponentMixin } from '@/mixins'
import { ActionBindingIF } from '@/interfaces/store-interfaces'

@Component({})
export default class ExitIncompletePaymentDialog extends DisplayedComponentMixin {
  @Getter(useStore) getExitIncompletePaymentVisible!: boolean
  @Action(useStore) setExitIncompletePaymentVisible!: ActionBindingIF

  get showModal () {
    return this.getExitIncompletePaymentVisible
  }

  set showModal (value: boolean) {
  }

  protected hideModal () {
    this.setExitIncompletePaymentVisible(false)
  }

  protected exit () {
    this.hideModal()
    this.cancelAndResetState()
  }
}
</script>
