<template>
  <v-dialog
    min-width="32rem"
    max-width="45rem"
    :value="isVisible"
    persistent
  >
    <v-card>
      <v-tabs id="confirm-nr-tabs">
        <v-tabs-items
          v-model="currentTab"
          touchless
        >
          <v-tab-item>
            <v-card-title class="d-flex justify-space-between">
              <div>Staff Payment</div>
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
                id="confirm-nr-back-btn"
                class="button-blue px-10"
                :disabled="isLoadingPayment"
                @click="goBack()"
              >
                Back
              </v-btn>
              <v-btn
                id="confirm-nr-submit-btn"
                class="primary px-5"
                :loading="isLoadingPayment"
                @click="confirmPayment()"
              >
                Submit Name Request
              </v-btn>
            </v-card-actions>
          </v-tab-item>

          <v-tab-item>
            <v-card-title>
              <v-row no-gutters>
                <v-col cols="8">
                  <span>Confirm Name Request</span>
                </v-col>
                <v-col>
                  <v-btn
                    icon
                    large
                    class="dialog-close"
                    @click="hideModal()"
                  >
                    <v-icon>mdi-close</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-title>

            <v-card-text class="copy-normal pt-5">
              <RequestDetails
                :applicant="getApplicant"
                :name="getName"
                :nameChoices="getNameChoices"
              />
              <FeeSummary
                class="mt-2"
                :fees="[...paymentFees]"
              />
            </v-card-text>

            <v-card-actions class="pt-8">
              <v-row no-gutters>
                <v-col
                  cols="12"
                  md="6"
                  lg="6"
                  :class="{ 'col-align-center': isMobile}"
                >
                  <v-btn
                    v-if="allowCancel"
                    id="confirm-nr-cancel-btn"
                    class="button-red"
                    :class="{ 'mobile-btn' : isMobile }"
                    :disabled="isLoadingPayment"
                    @click="cancelPayment()"
                  >
                    Cancel Name Request
                  </v-btn>
                </v-col>
                <v-col
                  cols="12"
                  md="2"
                  lg="2"
                  :class="[isMobile ? 'col-align-center' : 'col-align-end']"
                >
                  <v-btn
                    id="confirm-nr-close-btn"
                    class="button-blue"
                    :class="[isMobile ? 'mobile-btn' : 'mr-n6']"
                    :disabled="isLoadingPayment"
                    @click="hideModal()"
                  >
                    Close
                  </v-btn>
                </v-col>
                <v-col
                  cols="12"
                  md="4"
                  lg="4"
                  :class="[isMobile ? 'col-align-center' : 'col-align-end']"
                >
                  <v-btn
                    id="confirm-nr-continue-btn"
                    class="primary"
                    :class="{ 'mobile-btn' : isMobile }"
                    :loading="isLoadingPayment"
                    @click="confirmPayment()"
                  >
                    Continue to Payment
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-actions>
          </v-tab-item>
        </v-tabs-items>
      </v-tabs>
    </v-card>
  </v-dialog>
</template>

<script lang='ts'>
import { Component, Mixins, Prop, Watch } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore, usePaymentStore } from '@/store'
import FeeSummary from '@/components/payment/fee-summary.vue'
import RequestDetails from '@/components/common/request-details.vue'
import StaffPayment from '@/components/payment/staff-payment.vue'
import { FilingTypes } from '@/enums/filing-types'
import { Jurisdictions, PaymentAction } from '@/enums'
import { PaymentMixin, PaymentSessionMixin, DisplayedComponentMixin } from '@/mixins'
import { NameChoicesIF, CreatePaymentParams, FetchFeesParams } from '@/interfaces'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { PaymentRequiredError } from '@/errors'
import { Navigate } from '@/plugins'

@Component({
  components: {
    RequestDetails,
    FeeSummary,
    StaffPayment
  }
})
export default class ConfirmNrDialog extends Mixins(
  PaymentMixin,
  PaymentSessionMixin,
  DisplayedComponentMixin
) {
  // the tab indices
  // NB: these are reversed to reverse the built-in slide transition
  readonly TAB_STAFF_PAYMENT = 0
  readonly TAB_CONFIRM_NAME_REQUEST = 1

  // Refs
  $refs!: {
    staffPaymentComponent: StaffPayment
  }

  @Prop({ default: async () => {} }) readonly onCancel: () => void

  @Getter(useStore) getName!: string
  @Getter(useStore) getNameChoices!: NameChoicesIF
  @Getter(useStore) getPriorityRequest!: boolean
  @Getter(useStore) getBusinessAccount : any
  @Getter(useStore) isMobile!: boolean
  @Getter(useStore) isRoleStaff!: boolean
  @Getter(usePaymentStore) confirmNrModalIsVisible!: boolean

  @Action(usePaymentStore) toggleConfirmNrModal!: ActionBindingIF

  /** Whether staff payment is valid. */
  private isStaffPaymentValid = false

  /** The current tab to display. */
  private currentTab = this.TAB_CONFIRM_NAME_REQUEST

  /** Whether payment redirection is in progress. */
  private isLoadingPayment = false

  /** Whether this dialog is visible. */
  private isVisible = false

  /** Whether to show Cancel button. */
  private get allowCancel (): boolean {
    return (typeof this.$props.onCancel === 'function')
  }

  /** Whether this modal should be shown (per store property). */
  private get showModal (): boolean {
    return this.confirmNrModalIsVisible
  }

  /** Clears store property to hide this modal. */
  async hideModal () {
    this.isLoadingPayment = false
    await this.toggleConfirmNrModal(false)
  }

  /** Depending on value, fetches fees and makes this modal visible or hides it. */
  @Watch('showModal')
  async onShowModal (val: boolean): Promise<void> {
    if (val) {
      // reset tab id
      this.currentTab = this.TAB_CONFIRM_NAME_REQUEST

      const params: FetchFeesParams = {
        filingType: FilingTypes.NM620,
        jurisdiction: Jurisdictions.BC,
        priorityRequest: this.getPriorityRequest
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
    this.currentTab = this.TAB_CONFIRM_NAME_REQUEST
  }

  /** Called when user clicks Continue/Submit button. */
  async confirmPayment () {
    if (this.isRoleStaff) {
      if (this.currentTab === this.TAB_CONFIRM_NAME_REQUEST) {
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
      this.savePaymentResponseToSession(PaymentAction.CREATE, paymentResponse)

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
        action: PaymentAction.CREATE,
        nrId: this.getNrId,
        filingType: FilingTypes.NM620,
        priorityRequest: this.getPriorityRequest,
        businessAccountId: this.getBusinessAccount?.id
      } as CreatePaymentParams, onSuccess)
    } catch (error) {
      this.isLoadingPayment = false
      if (!(error instanceof PaymentRequiredError)) {
        // on generic error, close this modal so error modal is visible
        await this.hideModal()
      }
    }
  }

  /** Called when user clicks "Cancel Name Request" button. */
  async cancelPayment () {
    // rollback the NR
    this.$props.onCancel()
    // close this modal
    await this.hideModal()
  }

  @Watch('isVisible')
  onVisibleChanged (val: boolean) {
    if (val) {
      this.$nextTick(() => {
        if (this.$el?.querySelector instanceof Function) {
          // add classname to button text (for more detail in breadcrumbs)
          const confirmNrCancelBtn = this.$el.querySelector('#confirm-nr-cancel-btn > span')
          if (confirmNrCancelBtn) confirmNrCancelBtn.classList.add('confirm-nr-cancel-btn')
          const confirmNrContinueBtn = this.$el.querySelector('#confirm-nr-continue-btn > span')
          if (confirmNrContinueBtn) confirmNrContinueBtn.classList.add('confirm-nr-continue-btn')
          const confirmNrSubmitBtn = this.$el.querySelector('#confirm-nr-submit-btn > span')
          if (confirmNrSubmitBtn) confirmNrSubmitBtn.classList.add('confirm-nr-submit-btn')
          const confirmNrCloseBtn = this.$el.querySelector('#confirm-nr-close-btn > span')
          if (confirmNrCloseBtn) confirmNrCloseBtn.classList.add('confirm-nr-close-btn')
          const confirmNrBackBtn = this.$el.querySelector('#confirm-nr-back-btn > span')
          if (confirmNrBackBtn) confirmNrBackBtn.classList.add('confirm-nr-back-btn')
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

.col-align-center {
  text-align: center;
}

.col-align-end {
  text-align: end;
}

.mobile-btn {
  width: 16rem !important;
  margin: .5rem 0;
}
</style>
