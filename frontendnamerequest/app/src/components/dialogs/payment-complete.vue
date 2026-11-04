<template>
  <div>
    <v-dialog
      max-width="45rem"
      :value="showModal"
      persistent
    >
      <v-card>
        <v-card-title class="d-flex justify-space-between mt-n3">
          <div>Payment Successful</div>
          <v-btn
            icon
            large
            class="dialog-close"
            @click="hideModal()"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="copy-normal pt-4">
          <PaymentConfirm
            :nrNum="getNrNum"
            :applicant="getApplicant"
            :nameChoices="getNameChoices"
            :name="getName"
            :summary="summary"
            :receipt="paymentReceipt"
          />
        </v-card-text>

        <v-card-actions class="pt-1 justify-center">
          <v-btn
            id="receipt-download-btn"
            class="primary px-4"
            :loading="loading"
            @click="downloadReceipt()"
          >
            <span>Download Receipt</span>
          </v-btn>
          <v-btn
            id="receipt-close-btn"
            class="button-blue px-4"
            @click="hideModal()"
          >
            <span>Done</span>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      :value="showCompleteAccount"
      max-width="45rem"
      persistent
    >
      <v-card>
        <v-card-title>Complete your BC Registries account</v-card-title>
        <v-card-text class="copy-normal pt-4">
          Your name request has been submitted for review. Would you like to complete your
          BC Registries account?
        </v-card-text>
        <v-card-actions class="pt-1 justify-center">
          <v-btn
            id="complete-account-dismiss-btn"
            class="button-blue px-4"
            @click="dismissAccountRegistration()"
          >
            <span>Not now</span>
          </v-btn>
          <v-btn
            id="complete-account-btn"
            class="primary px-4"
            @click="completeAccountRegistration()"
          >
            <span>Complete your Registries Account</span>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { Component, Mixins, Watch } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore, usePaymentStore } from '@/store'
import PaymentConfirm from '@/components/payment/payment-confirm.vue'
import { NrState, PaymentAction } from '@/enums'
import { CommonMixin, PaymentMixin, PaymentSessionMixin } from '@/mixins'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { NameChoicesIF } from '@/interfaces'
import NamexServices from '@/services/namex-services'
import { getBusinessHomeLoginUrl, isLoggedInWithoutRegistriesAccount, Navigate } from '@/plugins'

@Component({
  components: {
    PaymentConfirm
  }
})
export default class PaymentCompleteDialog extends Mixins(
  CommonMixin,
  PaymentMixin,
  PaymentSessionMixin
) {
  @Getter(useStore) getName!: string
  @Getter(useStore) getNrNum!: string
  @Getter(useStore) getNrState!: NrState
  @Getter(useStore) getNameChoices!: NameChoicesIF
  @Getter(usePaymentStore) paymentCompleteModalIsVisible!: boolean

  @Action(useStore) loadExistingNameRequest!: ActionBindingIF
  @Action(useStore) setEditMode!: ActionBindingIF
  @Action(usePaymentStore) toggleReceiptModal!: ActionBindingIF

  /** Used to show loading state on button. */
  loading = false
  incompletePaymentRetries = 5
  isRetrying = false

  /** Shown after a guest credit-card payment when the login has no Registries account. */
  showCompleteAccount = false

  /** Whether this modal should be shown (per store property). */
  get showModal (): boolean {
    return this.paymentCompleteModalIsVisible
  }

  async mounted () {
    const { sessionPaymentId, sessionPaymentAction } = this
    // Check for a payment ID in sessionStorage, if it has been set, we've been redirected away from the application,
    // and need to rehydrate the application using the payment ID (for now, it could be some other token too)!
    if (sessionPaymentId && sessionPaymentAction) {
      // Make sure edit mode is disabled or it will screw up the back button
      await this.setEditMode(false)
      // Load the NR and the payment
      await this.fetchData()
    }
  }

  async hideModal () {
    await this.fetchNr()
    await this.toggleReceiptModal(false)
  }

  async fetchNr (): Promise<void> {
    let nrData = await NamexServices.getNameRequest(true)
    if (nrData.state === NrState.PENDING_PAYMENT && this.incompletePaymentRetries > 0) {
      this.incompletePaymentRetries--
      this.isRetrying = true
      setTimeout(async () => {
        await this.fetchData()
      }, 2000)
      // Retry at least once before showing pending payment, this should cover most of the cases.
      if (this.incompletePaymentRetries === 4) {
        nrData = null
      }
    } else {
      this.isRetrying = false
    }
    if (nrData) {
      await this.loadExistingNameRequest(nrData)
    }
  }

  /**
   * NOTE: This method makes use of the PaymentSectionMixin class!
   */
  async fetchData () {
    const { sessionPaymentId, sessionNrId, sessionPaymentAction } = this
    await this.fetchNr()
    await this.fetchPaymentData(sessionPaymentId, +sessionNrId)
    if (!this.isRetrying) {
      this.cleanUpSessionStorage()
      this.offerAccountRegistration(sessionPaymentAction)
    }
  }

  /**
   * After the name request is submitted, offer account creation option.
   * Upgrade, renew, and resubmit payments are not the first submission.
   */
  offerAccountRegistration (action: string): void {
    if (action !== PaymentAction.CREATE) return
    if (this.getNrState === NrState.PENDING_PAYMENT) return
    if (!isLoggedInWithoutRegistriesAccount()) return
    this.showCompleteAccount = true
  }

  dismissAccountRegistration (): void {
    this.showCompleteAccount = false
  }

  /**
   * Sends the user to Business Home account creation.
   * On return, the name request is loaded
   * again with the guest lookup the app already uses.
   */
  completeAccountRegistration (): void {
    sessionStorage.setItem('PENDING_NR_AFFILIATION', 'true')
    Navigate(getBusinessHomeLoginUrl(window.location.href))
  }

  cleanUpSessionStorage () {
    ['payment', 'paymentInProgress', 'paymentId', 'paymentToken', 'nrId'].forEach(key => sessionStorage.removeItem(key))
  }

  async fetchPaymentData (paymentId: number, nameReqId: number) {
    if (nameReqId && paymentId) {
      await this.fetchNrPayment(nameReqId, paymentId)
    }
  }

  get summary () {
    return {
      completionDate: this.paymentDate,
      statusCode: this.toTitleCase(this.sbcPaymentStatus)
    }
  }

  async downloadReceipt () {
    const { paymentId } = this
    this.loading = true
    await this.downloadReceiptPdf(paymentId)
    this.loading = false
  }

  @Watch('showModal')
  onVisibleChanged (val: boolean) {
    if (val) {
      this.$nextTick(() => {
        if (this.$el?.querySelector instanceof Function) {
          // add classname to button text (for more detail in breadcrumbs)
          const paymentSuccessfulDoneBtn = this.$el.querySelector('#receipt-close-btn > span')
          if (paymentSuccessfulDoneBtn) {
            paymentSuccessfulDoneBtn.classList
              .add('payment-successful-done-btn')
          }
          const paymentSuccessfulDownloadBtn = this.$el.querySelector('#receipt-download-btn > span')
          if (paymentSuccessfulDownloadBtn) {
            paymentSuccessfulDownloadBtn.classList
              .add('payment-successful-download-btn')
          }
        }
      })
    }
  }
}
</script>
