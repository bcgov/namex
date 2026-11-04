<template>
  <v-dialog
    min-width="32rem"
    max-width="45rem"
    :value="isVisible"
    persistent
  >
    <v-card>
      <v-tabs id="upgrade-tabs">
        <v-tabs-items
          v-model="currentTab"
          touchless
        >
          <v-tab-item>
            <v-card-title class="d-flex justify-space-between">
              <div>Staff Payment for Priority Upgrade</div>
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
                id="upgrade-back-btn"
                class="button-blue px-10"
                :disabled="isLoadingPayment"
                @click="goBack()"
              >
                Back
              </v-btn>
              <v-btn
                id="upgrade-submit-btn"
                class="primary px-5"
                :loading="isLoadingPayment"
                @click="confirmPayment()"
              >
                Submit Priority Upgrade
              </v-btn>
            </v-card-actions>
          </v-tab-item>

          <v-tab-item>
            <v-card-title class="d-flex justify-space-between">
              <div>Upgrade Priority</div>
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
                If you need your name reviewed as quickly as possible, upgrade to a Priority
                request. Priority name requests are usually reviewed within {{ getPriorityWaitTime }} business days.
              </p>

              <FeeSummary
                :fees="[...paymentFees]"
              />
            </v-card-text>

            <v-card-actions class="pt-8 justify-center">
              <v-btn
                id="upgrade-cancel-btn"
                class="button button-blue px-5"
                @click="hideModal()"
              >
                Cancel
              </v-btn>
              <v-btn
                id="upgrade-continue-btn"
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
import { CreatePaymentParams, FetchFeesParams } from '@/interfaces'
import { FilingTypes } from '@/enums/filing-types'
import { Jurisdictions, PaymentAction } from '@/enums'
import { PaymentMixin, PaymentSessionMixin, DisplayedComponentMixin } from '@/mixins'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { PaymentRequiredError } from '@/errors'
import { Navigate } from '@/plugins'

@Component({
  components: {
    FeeSummary,
    StaffPayment
  }
})
export default class UpgradeDialog extends Mixins(
  PaymentMixin,
  PaymentSessionMixin,
  DisplayedComponentMixin
) {
  @Getter(useStore) getPriorityWaitTime!: string | number

  // the tab indices
  // NB: these are reversed to reverse the built-in slide transition
  readonly TAB_STAFF_PAYMENT = 0
  readonly TAB_UPGRADE_NAME_REQUEST = 1

  // Refs
  $refs!: {
    staffPaymentComponent: StaffPayment
  }

  @Getter(useStore) isRoleStaff!: boolean
  @Getter(usePaymentStore) upgradeModalIsVisible!: boolean

  @Action(usePaymentStore) toggleUpgradeModal!: ActionBindingIF

  /** Whether staff payment is valid. */
  private isStaffPaymentValid = false

  /** The current tab to display. */
  private currentTab = this.TAB_UPGRADE_NAME_REQUEST

  /** Whether payment redirection is in progress. */
  private isLoadingPayment = false

  /** Whether this dialog is visible. */
  private isVisible = false

  /** Whether this modal should be shown (per store property). */
  private get showModal (): boolean {
    return this.upgradeModalIsVisible
  }

  /** Clears store property to hide this modal. */
  async hideModal () {
    this.isLoadingPayment = false
    await this.toggleUpgradeModal(false)
  }

  /** Depending on value, fetches fees and makes this modal visible or hides it. */
  @Watch('showModal')
  async onShowModal (val: boolean): Promise<void> {
    if (val) {
      // reset tab id
      this.currentTab = this.TAB_UPGRADE_NAME_REQUEST

      const params: FetchFeesParams = {
        filingType: FilingTypes.NM606,
        jurisdiction: Jurisdictions.BC,
        priorityRequest: false // not needed in NM606
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
    this.currentTab = this.TAB_UPGRADE_NAME_REQUEST
  }

  /** Called when user clicks Continue/Upgrade button. */
  private async confirmPayment () {
    if (this.isRoleStaff) {
      if (this.currentTab === this.TAB_UPGRADE_NAME_REQUEST) {
        // disable validation
        this.$refs.staffPaymentComponent && this.$refs.staffPaymentComponent.setValidation(false)
        // go to next tab
        this.currentTab = this.TAB_STAFF_PAYMENT
        return
      }
      if (this.currentTab === this.TAB_STAFF_PAYMENT) {
        // enable validation
        this.$refs.staffPaymentComponent && this.$refs.staffPaymentComponent.setValidation(true)
        // if invalid then stop, else continue
        if (!this.isStaffPaymentValid) return
      }
    }

    this.isLoadingPayment = true

    const onSuccess = (paymentResponse) => {
      const { paymentId, paymentToken } = this

      // Save response to session
      this.savePaymentResponseToSession(PaymentAction.UPGRADE, paymentResponse)

      // See if pay is needed else navigate to Existing NR page
      const baseUrl = sessionStorage.getItem('BASE_URL')
      const returnUrl = encodeURIComponent(`${baseUrl}/nr/${this.getNrId}/?paymentId=${paymentId}`)
      if (paymentResponse.sbcPayment.isPaymentActionRequired) {
        this.navigateToPaymentPortal(paymentToken, returnUrl)
      } else {
        Navigate(returnUrl)
      }
    }

    try {
      await this.createPayment({
        action: PaymentAction.UPGRADE,
        nrId: this.getNrId,
        filingType: FilingTypes.NM606,
        priorityRequest: false // not needed in NM606
      } as CreatePaymentParams, onSuccess)
    } catch (error) {
      this.isLoadingPayment = false
      if (!(error instanceof PaymentRequiredError)) {
        // on generic error, close this modal so error modal is visible
        await this.hideModal()
      }
    }
  }

  @Watch('isVisible')
  onVisibleChanged (val: boolean) {
    if (val) {
      this.$nextTick(() => {
        if (this.$el?.querySelector instanceof Function) {
          // add classname to button text (for more detail in breadcrumbs)
          const upgradeContinueBtn = this.$el.querySelector('#upgrade-continue-btn > span')
          if (upgradeContinueBtn) upgradeContinueBtn.classList.add('upgrade-continue-btn')
          const upgradeSubmitBtn = this.$el.querySelector('#upgrade-submit-btn > span')
          if (upgradeSubmitBtn) upgradeSubmitBtn.classList.add('upgrade-submit-btn')
          const upgradeCancelBtn = this.$el.querySelector('#upgrade-cancel-btn > span')
          if (upgradeCancelBtn) upgradeCancelBtn.classList.add('upgrade-cancel-btn')
          const upgradeBackBtn = this.$el.querySelector('#upgrade-back-btn > span')
          if (upgradeBackBtn) upgradeBackBtn.classList.add('upgrade-back-btn')
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
