<template>
  <span>
    <v-dialog
      v-if="payments"
      width="40rem"
      :value="isConfirmModalVisible"
      persistent
    >
      <v-card>
        <v-card-title class="d-flex justify-space-between">
          <div>Cancel and Refund</div>
          <v-btn
            icon
            large
            class="dialog-close"
            @click="hideConfirmModal()"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="text-body-1">
          This will cancel your Name Request and refund the Name Request fee, Priority Request
          fee (if any), and Service fees.
        </v-card-text>

        <v-card-text>
          <v-alert
            v-if="fetchError"
            color="error"
            icon="mdi-alert"
            outlined
            class="my-0"
            v-html="fetchError"
          />
          <refund-summary
            v-else
            :payments="payments"
          />
        </v-card-text>

        <v-card-text class="text-body-2">
          The refund will be applied to your original payment method and the requested name will not be
          examined for use. <template v-if="emailAddress">An email confirming the cancellation and
            refund of this Name Request will be sent to <strong>{{ emailAddress }}</strong>.</template>
        </v-card-text>

        <v-card-actions class="justify-center">
          <v-btn
            id="cancel-nr-btn"
            class="px-6 button-normal"
            :loading="loading"
            @click="confirmRefund()"
          >Cancel this Name Request</v-btn>
          <v-btn
            id="keep-nr-btn"
            class="px-6 button-blue"
            @click="hideConfirmModal()"
          >Keep this Name Request</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      width="40rem"
      :value="isResponseModalVisible"
      persistent
    >
      <v-card>
        <v-card-title class="d-flex justify-space-between">
          <div>Cancel and Refund</div>
          <v-btn
            icon
            large
            class="dialog-close"
            @click="hideResponseModal()"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="text-body-1">
          <span v-html="getRefundParams.refundMessageText1" />
        </v-card-text>

        <v-card-text
          v-if="getRefundParams.refundMessageText2"
          class="text-body-1"
        >
          <span v-html="getRefundParams.refundMessageText2" />
        </v-card-text>

        <v-card-text
          v-if="getRefundParams.showStaffContact"
          class="text-body-2"
        >
          <ContactInfo
            id="tooltip-contact-info"
            direction="col"
          />
        </v-card-text>

        <v-card-actions class="justify-center">
          <v-btn
            id="keep-nr-btn"
            class="px-6 button-normal"
            @click="hideResponseModal()"
          >OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </span>
</template>

<script lang="ts">
import { Component, Mixins, Watch } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore, usePaymentStore } from '@/store'
import RefundSummary from '@/components/payment/refund-summary.vue'
import ContactInfo from '@/components/common/contact-info.vue'
import { NrAction } from '@/enums'
import { PaymentMixin, PaymentSessionMixin } from '@/mixins'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import NamexServices from '@/services/namex-services'

@Component({
  components: {
    RefundSummary,
    ContactInfo
  }
})
export default class RefundDialog extends Mixins(PaymentMixin, PaymentSessionMixin) {
  @Getter(useStore) getNrId!: number
  @Getter(usePaymentStore) refundModalIsVisible!: boolean

  @Action(useStore) loadExistingNameRequest!: ActionBindingIF
  @Action(useStore) setDisplayedComponent!: ActionBindingIF
  @Action(usePaymentStore) toggleRefundModal!: ActionBindingIF

  /** Used to display a fetch error, if any. */
  protected fetchError = ''

  /** Used to show loading state on button. */
  protected loading = false

  /** The model value for the confirm dialog component. */
  protected isConfirmModalVisible = false

  /** The model value for the response dialog component. */
  protected isResponseModalVisible = false

  get emailAddress (): string {
    return this.getApplicant?.emailAddress
  }

  /** Whether this modal should be shown (per store property). */
  get showConfirmModal (): boolean {
    return this.refundModalIsVisible
  }

  /** Clears store property to hide this modal. */
  protected async hideConfirmModal (): Promise<void> {
    await this.toggleRefundModal(false)
  }

  /** Depending on value, fetches data and makes this modal visible or hides it. */
  @Watch('showConfirmModal')
  private async onShowConfirmModal (val: boolean) {
    if (val) {
      // only make visible on success, otherwise hide it
      if (await this.fetchData()) {
        this.isConfirmModalVisible = true
      } else {
        await this.hideConfirmModal()
      }
    } else {
      this.isConfirmModalVisible = false
    }
  }

  /** Called when user clicks "Cancel this NR" button. */
  protected async confirmRefund (): Promise<void> {
    this.loading = true
    const data = await NamexServices.patchNameRequestsByAction(this.getNrId, NrAction.REQUEST_REFUND)
    if (data) {
      await this.loadExistingNameRequest(data)
      this.buildRefundParams()
      this.loading = false
      await this.hideConfirmModal()
      this.isResponseModalVisible = true
    } else {
      this.loading = false
      await this.hideConfirmModal()
    }
  }

  /** Hides the response modal */
  protected hideResponseModal (): void {
    this.isResponseModalVisible = false
  }

  /**
   * Fetches the NR's payments.
   * @returns True if successful, otherwise False
   */
  private async fetchData (): Promise<boolean> {
    if (!this.getNrId) return false
    // NB: errors are handled by PaymentMixin
    return this.fetchNrPayments(this.getNrId)
  }

  @Watch('isConfirmModalVisible')
  private onVisibleChanged (val: boolean) {
    if (val) {
      this.$nextTick(() => {
        if (this.$el?.querySelector instanceof Function) {
          // add classname to button text (for more detail in breadcrumbs)
          const refundCancelBtn = this.$el.querySelector('#cancel-nr-btn > span')
          if (refundCancelBtn) refundCancelBtn.classList.add('refund-cancel-btn')
          const refundKeepBtn = this.$el.querySelector('#keep-nr-btn > span')
          if (refundKeepBtn) refundKeepBtn.classList.add('refund-keep-btn')
        }
      })
    }
  }
}
</script>
