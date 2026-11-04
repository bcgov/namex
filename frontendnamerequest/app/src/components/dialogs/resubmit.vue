<template>
  <v-dialog
    min-width="32rem"
    max-width="45rem"
    :value="isVisible"
    persistent
  >
    <v-card>
      <v-tabs id="resubmit-tabs">
        <v-tabs-items
          v-model="currentTab"
          touchless
        >
          <v-tab-item>
            <v-card-title class="d-flex justify-space-between">
              <div>Staff Payment for Name Request Resubmission</div>
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
                id="resubmit-back-btn"
                class="button-blue px-10"
                :disabled="isLoadingPayment"
                @click="goBack()"
              >
                Back
              </v-btn>
              <v-btn
                id="resubmit-submit-btn"
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
              <div>Resubmit Name Request</div>
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
                If your Name Request has expired, you can resubmit the same name request, for a
                fee. This will generate a new Name Request Number. Resubmissions follow the same
                process for new submissions using the email and phone number on the Name Request.
              </p>

              <FeeSummary
                :fees="[...paymentFees]"
              />

              <v-tooltip
                top
                content-class="top-tooltip"
                transition="fade-transition"
                :disabled="isMobile || enablePriorityCheckbox"
              >
                <template #activator="{ on }">
                  <div
                    class="width-fit-content"
                    v-on="on"
                  >
                    <v-checkbox
                      v-model="isPriorityRequest"
                      hide-details
                      class="pre-wrap mt-8 pt-0 pl-2"
                      :disabled="!enablePriorityCheckbox"
                    >
                      <template #label>
                        Make this a Priority Request <b>($100)</b>
                      </template>
                    </v-checkbox>
                  </div>
                </template>
                <span>
                  Due to the on-going labour dispute between the government and its employees,
                  priority filings are temporarily disabled.
                </span>
              </v-tooltip>
            </v-card-text>

            <v-card-actions class="pt-8 justify-center">
              <v-btn
                id="resubmit-cancel-btn"
                class="button button-blue px-5"
                @click="hideModal()"
              >
                Cancel
              </v-btn>
              <v-btn
                id="resubmit-continue-btn"
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
import { Jurisdictions, NrAction, PaymentAction } from '@/enums'
import { PaymentMixin, PaymentSessionMixin, DisplayedComponentMixin } from '@/mixins'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import NamexServices from '@/services/namex-services'
import { PaymentRequiredError } from '@/errors'
import { GetFeatureFlag, Navigate } from '@/plugins'

@Component({
  components: {
    FeeSummary,
    StaffPayment
  }
})
export default class ResubmitDialog extends Mixins(
  PaymentMixin,
  PaymentSessionMixin,
  DisplayedComponentMixin
) {
  // the tab indices
  // NB: these are reversed to reverse the built-in slide transition
  readonly TAB_STAFF_PAYMENT = 0
  readonly TAB_RESUBMIT_NAME_REQUEST = 1

  // Refs
  $refs!: {
    staffPaymentComponent: StaffPayment
  }

  @Getter(useStore) isRoleStaff!: boolean
  @Getter(useStore) getNrNum!: string
  @Getter(useStore) isMobile!: boolean
  @Getter(usePaymentStore) resubmitModalIsVisible!: boolean

  @Action(usePaymentStore) toggleResubmitModal!: ActionBindingIF
  @Action(useStore) resubmit!: ActionBindingIF
  @Action(useStore) setPriorityRequest!: ActionBindingIF
  @Action(useStore) loadExistingNameRequest!: ActionBindingIF

  /** Whether staff payment is valid. */
  private isStaffPaymentValid = false

  /** The current tab to display. */
  private currentTab = this.TAB_RESUBMIT_NAME_REQUEST

  /** Whether payment redirection is in progress. */
  private isLoadingPayment = false

  /** Whether this dialog is visible. */
  private isVisible = false

  /**
   * Whether this NR is a priority request.
   * Initially false for resubmission.
   */
  private isPriorityRequest = false

  /** Whether priority checkbox should be enabled. */
  get enablePriorityCheckbox (): boolean {
    return GetFeatureFlag('enable-priority-checkbox')
  }

  /** Whether this modal should be shown (per store property). */
  get showModal (): boolean {
    return this.resubmitModalIsVisible
  }

  /** Clears store property to hide this modal. */
  async hideModal () {
    this.isLoadingPayment = false
    await this.toggleResubmitModal(false)
  }

  /** Depending on value, fetches fees and makes this modal visible or hides it. */
  @Watch('showModal')
  async onShowModal (val: boolean): Promise<void> {
    if (val) {
      // reset tab id
      this.currentTab = this.TAB_RESUBMIT_NAME_REQUEST

      // only make visible on success, otherwise hide it
      if (await this.onPriorityRequestChange()) {
        this.isVisible = true
      } else {
        await this.hideModal()
      }
    } else {
      this.isVisible = false
    }
  }

  @Watch('isPriorityRequest')
  async onPriorityRequestChange (): Promise<boolean> {
    // update new request model
    this.setPriorityRequest(this.isPriorityRequest)

    // fetch fees
    const params: FetchFeesParams = {
      filingType: FilingTypes.NM620,
      jurisdiction: Jurisdictions.BC,
      priorityRequest: this.isPriorityRequest
    }
    return this.fetchFees(params)
  }

  /** Called when staff clicks "Back" button. */
  goBack () {
    // disable validation
    this.$refs.staffPaymentComponent && this.$refs.staffPaymentComponent.setValidation(false)
    // go to previous tab
    this.currentTab = this.TAB_RESUBMIT_NAME_REQUEST
  }

  /** Called when user clicks Continue/Resubmit button. */
  private async confirmPayment () {
    if (this.isRoleStaff) {
      if (this.currentTab === this.TAB_RESUBMIT_NAME_REQUEST) {
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

    // save original NR number
    const nrNum = this.getNrNum

    // first resubmit the NR
    let success: boolean = await this.resubmit(null)

    const onSuccess = (paymentResponse) => {
      const { paymentId, paymentToken } = this

      // Save response to session
      this.savePaymentResponseToSession(PaymentAction.RESUBMIT, paymentResponse)

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
      // if resubmit succeeded then create the payment
      if (success) {
        await this.createPayment({
          action: PaymentAction.RESUBMIT,
          nrId: this.getNrId,
          filingType: FilingTypes.NM620,
          priorityRequest: this.isPriorityRequest
        } as CreatePaymentParams, onSuccess)
      }
    } catch (error) {
      this.isLoadingPayment = false
      if (!(error instanceof PaymentRequiredError)) {
        // close this modal so generic error modal is visible
        await this.hideModal()
      }

      // reset session data
      sessionStorage.setItem('BCREG-NRL', null)
      sessionStorage.setItem('BCREG-nrNum', nrNum)

      // try to delete the new (resubmitted) NR
      await NamexServices.patchNameRequestsByAction(this.getNrId, NrAction.CANCEL).catch(() => {})

      // try to reload the original NR
      const nrData = await NamexServices.getNameRequest(false)
      if (nrData) this.loadExistingNameRequest(nrData)
    }
  }

  @Watch('isVisible')
  onVisibleChanged (val: boolean) {
    if (val) {
      this.$nextTick(() => {
        if (this.$el?.querySelector instanceof Function) {
          // add classname to button text (for more detail in breadcrumbs)
          const resubmitContinueBtn = this.$el.querySelector('#resubmit-continue-btn > span')
          if (resubmitContinueBtn) resubmitContinueBtn.classList.add('resubmit-continue-btn')
          const resubmitSubmitBtn = this.$el.querySelector('#resubmit-submit-btn > span')
          if (resubmitSubmitBtn) resubmitSubmitBtn.classList.add('resubmit-submit-btn')
          const resubmitCancelBtn = this.$el.querySelector('#resubmit-cancel-btn > span')
          if (resubmitCancelBtn) resubmitCancelBtn.classList.add('resubmit-cancel-btn')
          const resubmitBackBtn = this.$el.querySelector('#resubmit-back-btn > span')
          if (resubmitBackBtn) resubmitBackBtn.classList.add('resubmit-back-btn')
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/theme";

.width-fit-content {
  width: fit-content;
}

// hide tabs bar
::v-deep .v-tabs > .v-tabs-bar {
  display: none;
}

// adjust top whitespace so 'X' button is not cropped
.v-tabs-items {
  padding-top: 0.5rem;
  margin-top: -0.5rem;
}

// disabled checkbox label
::v-deep .v-input--is-disabled label {
  color: $disabled-action !important;
}
</style>
