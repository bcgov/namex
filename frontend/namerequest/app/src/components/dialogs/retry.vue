<template>
  <v-dialog
    min-width="32rem"
    max-width="45rem"
    :value="isVisible"
    persistent
  >
    <v-card>
      <v-tabs id="retry-tabs">
        <v-tabs-items
          v-model="currentTab"
          touchless
        >
          <v-tab-item>
            <v-card-title class="d-flex justify-space-between">
              <div>Staff Payment for Name Request</div>
              <v-btn
                icon
                large
                class="dialog-close float-right"
                @click="hideModal()"
              >
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </v-card-title>

            <v-card-text class="copy-normal pt-5">
              <StaffPayment
                ref="staffPaymentComponent"
                @isValid="isStaffPaymentValid = $event"
              />
            </v-card-text>

            <v-card-actions class="justify-center pt-6">
              <v-btn
                id="retry-back-btn"
                class="button-blue px-10"
                :disabled="isLoadingPayment"
                @click="goBack()"
              >
                Back
              </v-btn>
              <v-btn
                id="retry-submit-btn"
                class="primary px-5"
                :loading="isLoadingPayment"
                @click="confirmPayment()"
              >
                Submit Name Request
              </v-btn>
            </v-card-actions>
          </v-tab-item>

          <v-tab-item>
            <v-card-title class="d-flex justify-space-between">
              <div>Retry Payment for Name Request</div>
              <v-btn
                icon
                large
                class="dialog-close float-right"
                @click="hideModal()"
              >
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </v-card-title>

            <v-card-text class="copy-normal">
              <p
                v-if="!isRoleStaff"
                class="mb-8"
              >
                If your Name Request payment was previously cancelled or did not go through, you
                can retry payment.
              </p>

              <FeeSummary
                :fees="[...paymentFees]"
              />
            </v-card-text>

            <v-card-actions class="pt-8 justify-center">
              <v-btn
                id="retry-cancel-btn"
                class="button button-blue px-5"
                @click="hideModal()"
              >
                Cancel
              </v-btn>
              <v-btn
                id="retry-continue-btn"
                class="primary px-5"
                :loading="isLoadingPayment"
                @click="confirmPayment()"
              >
                Continue to Payment
              </v-btn>
            </v-card-actions>
          </v-tab-item>
        </v-tabs-items>
      </v-tabs>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Mixins, Watch } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore, usePaymentStore } from '@/store'
import FeeSummary from '@/components/payment/fee-summary.vue'
import StaffPayment from '@/components/payment/staff-payment.vue'
import { FilingTypes } from '@/enums/filing-types'
import { Jurisdictions, PaymentStatus } from '@/enums'
import { PaymentMixin, PaymentSessionMixin, DisplayedComponentMixin } from '@/mixins'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { FetchFeesParams } from '@/interfaces'

@Component({
  components: {
    FeeSummary,
    StaffPayment
  }
})
export default class RetryDialog extends Mixins(
  PaymentMixin,
  PaymentSessionMixin,
  DisplayedComponentMixin
) {
  // the tab indices
  // NB: these are reversed to reverse the built-in slide transition
  readonly TAB_STAFF_PAYMENT = 0
  readonly TAB_RETRY_PAYMENT = 1

  // Refs
  $refs!: {
    staffPaymentComponent: StaffPayment
  }

  @Getter(useStore) getPriorityRequest!: boolean
  @Getter(useStore) isRoleStaff!: boolean
  @Getter(usePaymentStore) retryModalIsVisible!: boolean

  @Action(usePaymentStore) toggleRetryModal!: ActionBindingIF

  /** Whether staff payment is valid. */
  private isStaffPaymentValid = false

  /** The current tab to display. */
  private currentTab = this.TAB_RETRY_PAYMENT

  /** Whether payment redirection is in progress. */
  private isLoadingPayment = false

  /** Whether this dialog is visible. */
  private isVisible = false

  /** Whether this modal should be shown (per store property). */
  private get showModal (): boolean {
    return this.retryModalIsVisible
  }

  /** Clears store property to hide this modal. */
  async hideModal () {
    this.isLoadingPayment = false
    await this.toggleRetryModal(false)
  }

  /** Depending on value, fetches fees and makes this modal visible or hides it. */
  @Watch('showModal')
  async onShowModal (val: boolean): Promise<void> {
    if (val) {
      // reset tab id
      this.currentTab = this.TAB_RETRY_PAYMENT

      const params: FetchFeesParams = {
        filingType: FilingTypes.NM620,
        jurisdiction: Jurisdictions.BC,
        priorityRequest: this.getPriorityRequest // same value as originally
      }

      // only make visible on success, otherwise hide it
      if (await this.fetchFees(params)) {
        this.isVisible = true
      } else {
        await this.hideModal()
      }
    } else {
      this.isVisible = false
    }
  }

  /** Called when staff clicks "Back" button. */
  goBack () {
    // disable validation
    this.$refs.staffPaymentComponent && this.$refs.staffPaymentComponent.setValidation(false)
    // go to previous tab
    this.currentTab = this.TAB_RETRY_PAYMENT
  }

  /** Called when user clicks Continue/Submit button. */
  private async confirmPayment () {
    // FUTURE: enable this for staff payment if needed
    // if (this.isRoleStaff) {
    //   if (this.currentTab === this.TAB_RETRY_PAYMENT) {
    //     // disable validation
    //     this.$refs.staffPaymentComponent && this.$refs.staffPaymentComponent.setValidation(false)
    //     // go to next tab
    //     this.currentTab = this.TAB_STAFF_PAYMENT
    //     return
    //   }
    //   if (this.currentTab === this.TAB_STAFF_PAYMENT) {
    //     // enable validation
    //     this.$refs.staffPaymentComponent && this.$refs.staffPaymentComponent.setValidation(true)
    //     // if invalid then stop, else continue
    //     if (!this.isStaffPaymentValid) return
    //   }
    // }

    // navigate to the payment portal
    this.isLoadingPayment = true
    const { id, token, nrId, action } = this.pendingPayment

    // Save payment to session
    this.savePendingPaymentToSession(action, this.pendingPayment)

    const baseUrl = sessionStorage.getItem('BASE_URL')
    const returnUrl = encodeURIComponent(`${baseUrl}/nr/${nrId}/?paymentId=${id}`)
    this.navigateToPaymentPortal(token, returnUrl)
  }

  /** The first pending payment. */
  private get pendingPayment (): any {
    return this.payments.find(payment => (
      ![PaymentStatus.APPROVED, PaymentStatus.COMPLETED, PaymentStatus.CANCELLED, PaymentStatus.REFUND_REQUESTED]
        .includes(payment.statusCode)
    ))
  }

  @Watch('isVisible')
  onVisibleChanged (val: boolean) {
    if (val) {
      this.$nextTick(() => {
        if (this.$el?.querySelector instanceof Function) {
          // add classname to button text (for more detail in breadcrumbs)
          const retryContinueBtn = this.$el.querySelector('#retry-continue-btn > span')
          if (retryContinueBtn) retryContinueBtn.classList.add('retry-continue-btn')
          const retryNrBtn = this.$el.querySelector('#retry-submit-btn > span')
          if (retryNrBtn) retryNrBtn.classList.add('retry-submit-btn')
          const retryCancelBtn = this.$el.querySelector('#retry-cancel-btn > span')
          if (retryCancelBtn) retryCancelBtn.classList.add('retry-cancel-btn')
          const retryBackBtn = this.$el.querySelector('#retry-back-btn > span')
          if (retryBackBtn) retryBackBtn.classList.add('retry-back-btn')
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
// hide tabs bar
::v-deep .v-tabs > .v-tabs-bar {
  display: none;
}

// adjust top whitespace so 'X' button is not cropped
.v-tabs-items {
  padding-top: 0.5rem;
  margin-top: -0.5rem;
}
</style>
