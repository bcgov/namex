import { Component, Mixins } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useErrorStore, usePaymentStore, useStore } from '@/store'
import { AxiosRequestConfig } from 'axios'
import { ACCEPTED, CREATED, NO_CONTENT, OK, PAYMENT_REQUIRED } from 'http-status-codes'
import { SessionStorageKeys } from 'sbc-common-components/src/util/constants'
import { PaymentStatus, StaffPaymentOptions, NrState, PaymentMethod, SbcPaymentStatus, PaymentAction } from '@/enums'
import { ActionMixin } from '@/mixins'
import { StaffPaymentIF, RefundParamsIF, NameRequestI, ErrorI, CreatePaymentParams, FetchFeesParams,
  NameRequestPaymentResponse } from '@/interfaces'
import NamexServices from '@/services/namex-services'
import { PaymentRequiredError } from '@/errors'
import { isLoggedInWithoutRegistriesAccount, Navigate } from '@/plugins'

const namexApiUrl = sessionStorage.getItem('NAMEX_API_URL')

@Component({})
export class PaymentMixin extends Mixins(ActionMixin) {
  @Action(usePaymentStore) setPayment!: (payment: any) => void
  @Action(usePaymentStore) setPayments!: (payments: any[]) => void
  @Action(usePaymentStore) setPaymentFees!: (fees: any) => void
  @Action(usePaymentStore) setPaymentReceipt!: (receipt: any) => void
  @Action(usePaymentStore) setPaymentRequest!: (req: any) => void
  @Action(usePaymentStore) setSbcPayment!: (payment: any) => void
  @Action(useStore) setFolioNumber!: (folioNumber: string) => void
  @Action(useStore) setRefundParams!: (refundParams: RefundParamsIF) => void
  @Action(useErrorStore) setAppError!: (err: ErrorI) => void

  @Getter(useStore) getCurrentJsDate!: Date
  @Getter(useStore) getStaffPayment!: StaffPaymentIF
  @Getter(useStore) getFolioNumber!: string
  @Getter(useStore) getNr!: Partial<NameRequestI>
  @Getter(useStore) getRefundParams!: RefundParamsIF
  @Getter(usePaymentStore) getSbcPayment!: any
  @Getter(usePaymentStore) getSbcPaymentStatus!: any
  @Getter(usePaymentStore) getPayment!: any
  @Getter(usePaymentStore) getPaymentId!: number
  @Getter(usePaymentStore) getPaymentToken!: any
  @Getter(usePaymentStore) getPaymentStatus!: PaymentStatus
  @Getter(usePaymentStore) getPaymentDate!: any
  @Getter(usePaymentStore) getPaymentRequest!: any
  @Getter(usePaymentStore) getPaymentReceipt!: any
  @Getter(usePaymentStore) getPaymentFees!: any
  @Getter(usePaymentStore) getPayments!: any

  get sbcPayment () {
    return this.getSbcPayment
  }

  get sbcPaymentStatus () {
    return this.getSbcPaymentStatus
  }

  get payment () {
    return this.getPayment
  }

  get paymentId () {
    return this.getPaymentId
  }

  get paymentToken () {
    return this.getPaymentToken
  }

  get paymentStatus (): PaymentStatus {
    return this.getPaymentStatus
  }

  get paymentDate () {
    return this.getPaymentDate
  }

  get paymentRequest () {
    return this.getPaymentRequest
  }

  get paymentReceipt () {
    return this.getPaymentReceipt
  }

  get paymentFees (): any[] {
    const fees = this.getPaymentFees
    return [fees]
  }

  get payments () {
    return this.getPayments
  }

  get paymentSummaries () {
    const payments = this.getPayments
    const summaries = payments?.map(payment => {
      const { id, sbcPayment } = payment
      let receipt
      if (sbcPayment &&
        sbcPayment.receipts instanceof Array &&
        sbcPayment.receipts.length > 0) {
        receipt = sbcPayment.receipts[0]
      }

      return {
        id,
        payment,
        receipt
      }
    })
    return summaries
  }

  /** Check if there is more than one payment. */
  get isThereMoreThanOnePayment (): boolean {
    if (Array.isArray(this.payments) && this.payments.length > 1) {
      return true
    }
    return false
  }

  /** Check if there is more than one payment with different status. */
  get isDifferentPaymentStatus (): boolean {
    if (Array.isArray(this.payments) && this.payments.length > 1) {
      const paymentStatus = this.payments.map(payment => payment.sbcPayment.statusCode)
      return paymentStatus.some(method => method !== paymentStatus[0])
    }
    return false
  }

  /** Check if the user has been waived of all fees for the NR. */
  get isNoFeePayment (): boolean {
    if (Array.isArray(this.payments) && this.payments.length) {
      // Payments might not have been processed yet, e.g., PAD
      if (this.payments.length > 1) {
        return this.payments.reduce((paymentA, paymentB) => paymentA.sbcPayment.paid + paymentB.sbcPayment.paid) === 0
      } else {
        return this.payments[0].sbcPayment.paid === 0
      }
    }
    return true
  }

  /**
   * Check if there is any amount that will be refunded.
   * Some payments are not refundable or some problem may be happened to the refund request.
   */
  get isNoRefund (): boolean {
    if (Array.isArray(this.payments) && this.payments.length) {
      // Payments might not have been processed yet, e.g., PAD
      if (this.payments.length > 1) {
        return this.payments.reduce(
          (paymentA, paymentB) => paymentA.sbcPayment.refund + paymentB.sbcPayment.refund
        ) === 0
      } else {
        return this.payments[0].refund === 0
      }
    }
    return true
  }

  async fetchFees (params: FetchFeesParams): Promise<boolean> {
    const { filingType, jurisdiction, priorityRequest } = params
    try {
      // NB: params uses snake_case
      const data: any = {
        'filing_type_code': filingType,
        'jurisdiction': jurisdiction,
        'date': this.getCurrentJsDate.toISOString(), // "now" in UTC
        'priority': priorityRequest,
        headers: this.buildHeaders(false)
      }

      const response = await this._getPaymentFees(data)
      this.setPaymentFees(response)
      return true
    } catch (err) {
      // don't console.error - _getPaymentFees() already did that
      this.setAppError(
        { id: 'fetch-fees-error', error: 'Could not fetch fees' } as ErrorI
      )
      return false
    }
  }

  /**
   * Check if NR State is 'REFUND_REQUESTED'
   * If so, call buildRefundParams method.
  */
  get isRefundRequested (): boolean {
    if (this.getNr.state === NrState.REFUND_REQUESTED) {
      this.buildRefundParams()
      return true
    }
    return false
  }

  get isIncompletePayment (): boolean {
    return (this.getNr.state === NrState.PENDING_PAYMENT)
  }

  setRefundParamsByStatus (paymentMethod, paymentStatus) {
    if (paymentStatus === PaymentStatus.REFUNDED) {
      const refundParams = {
        refundLabel: 'Refund process is completed',
        refundMessageText1: 'Your Name Request has been cancelled and the payment has been refunded.',
        showStaffContact: false,
        showAlertIcon: false
      }
      this.setRefundParams(refundParams)
    } else if (paymentStatus === PaymentStatus.CREDITED) {
      const refundParams = {
        refundLabel: 'Funds have been credited',
        refundMessageText1: 'Your Name Request has been cancelled and ' +
        'the payment has been credited back your BC Registries payment account.',
        showStaffContact: false,
        showAlertIcon: false
      }
      this.setRefundParams(refundParams)
    } else if (paymentStatus === PaymentStatus.CANCELLED) {
      const refundParams = {
        refundLabel: 'Payment Cancelled',
        refundMessageText1: 'Your Name Request has been cancelled and your account has not been charged.',
        showStaffContact: false,
        showAlertIcon: false
      }
      this.setRefundParams(refundParams)
    } else {
      // REFUND_REQUESTED or other status
      if (paymentMethod === PaymentMethod.PAD) {
        // Premium Account
        if (!this.isNoRefund) {
          const refundParams = {
            refundLabel: 'Refund has been requested',
            refundMessageText1:
            'Your Name Request has been cancelled and a refund request is being processed.',
            refundMessageText2:
            'A credit will be applied to your BC Registries account.<br/>There may be a one day delay before the ' +
            'credit will show on your transactions / statetements.',
            showStaffContact: false,
            showAlertIcon: false
          }
          this.setRefundParams(refundParams)
        } else {
          // May happen when a PAD is not processed yet.
          // It usually takes a day to be processed.
          const refundParams = {
            refundLabel: 'Refund Not Processed',
            refundMessageText1:
            'Your Name Request has been cancelled.',
            refundMessageText2:
            'Pre-authorized debit transactions are handled at the end of each day, therefore, your bank will ' +
            'not be charged the initial payment amount.',
            showStaffContact: false,
            showAlertIcon: true
          }
          this.setRefundParams(refundParams)
        }
      } else if (paymentMethod === PaymentMethod.INTERNAL) {
        // INTERNAL is a Staff payment. It can be 'Routing Slip' or 'No Fee' payments.
        if (this.isNoFeePayment) {
          // No Fee payment
          const refundParams = {
            refundLabel: 'Refund Not Processed',
            refundMessageText1:
            'Your Name Request has been cancelled.',
            refundMessageText2:
            'Since there was no charge for this transaction, a refund will not be issued. Please contact BC ' +
            'Registries if you require further assistance.',
            showStaffContact: true,
            showAlertIcon: true
          }
          this.setRefundParams(refundParams)
        } else {
          // Routing Slip
          const refundParams = {
            refundLabel: 'Refund Not Processed',
            refundMessageText1:
            'Your Name Request has been cancelled, but you will not receive an automatic refund. ' +
            'Please contact BC Registries in order to request a refund.',
            refundMessageText2: '',
            showStaffContact: true,
            showAlertIcon: true
          }
          this.setRefundParams(refundParams)
        }
      } else if ([PaymentMethod.DIRECT_PAY, PaymentMethod.DRAWDOWN].includes(paymentMethod)) {
        // Credit Card or BCOL
        if (!this.isNoFeePayment) {
          const refundParams = {
            refundLabel: 'Refund Request Processed',
            refundMessageText1:
            'Your Name Request has been cancelled and a refund request has been submitted.',
            refundMessageText2:
            'The refund will be applied to your original payment method and the requested name will not be ' +
            'examined for use. An email confirming the cancellation and refund of this Name Request will be ' +
            `sent to ${this.getNr.applicants.emailAddress}.`,
            showStaffContact: false,
            showAlertIcon: false
          }
          this.setRefundParams(refundParams)
        } else {
          const refundParams = {
            refundLabel: 'Refund process is completed',
            refundMessageText1: 'Your Name Request has been cancelled and the payment has been refunded.',
            showStaffContact: false,
            showAlertIcon: false
          }
          this.setRefundParams(refundParams)
        }
      }
    }
  }

  /**
   * Build refund params to be used to display information about the refund request.
  */
  buildRefundParams () {
    if (this.getNr.state === NrState.REFUND_REQUESTED) {
      if (!this.isThereMoreThanOnePayment) {
        // Only 1 payment record
        const paymentMethod = this.payments[0]?.sbcPayment?.paymentMethod
        const paymentStatus = this.payments[0]?.sbcPayment?.statusCode
        this.setRefundParamsByStatus(paymentMethod, paymentStatus)
      } else {
        // More than 1 payment. (e.g. paid priority service)
        if (!this.isDifferentPaymentStatus) {
          // all payments have the same status
          const paymentMethod = this.payments[0]?.sbcPayment?.paymentMethod
          const paymentStatus = this.payments[0]?.sbcPayment?.statusCode
          this.setRefundParamsByStatus(paymentMethod, paymentStatus)
        } else {
          // the payments have the different status (.e.g one REFUNDED and another one REFUND_REQUESTED)
          if (!this.isNoRefund) {
            // Multi-transaction scenario returns success
            const refundParams = {
              refundLabel: 'Refund Request Processed',
              refundMessageText1:
              'Your Name Request has been cancelled and the refund request has been submitted.<br/><br/>' +
              'The refund will be applied to your original payment method and the requested name will not be ' +
              'examined for use. An email confirming the cancellation and refund of this Name Request will be ' +
              `sent to ${this.getNr.applicants.emailAddress}.`,
              showStaffContact: false,
              showAlertIcon: false
            }
            this.setRefundParams(refundParams)
          } else {
            // This should not happen
            const refundParams = {
              refundLabel: 'Refund Not Processed',
              refundMessageText1:
              'Your Name Request has been cancelled, but we were unable to process ' +
              'your full refund. Please contact BC Registries.',
              showStaffContact: true,
              showAlertIcon: true
            }
            this.setRefundParams(refundParams)
          }
        }
      }
    }
  }

  async createPayment (params: CreatePaymentParams, onSuccess: (paymentResponse) => void): Promise<boolean> {
    const { nrId, filingType, priorityRequest, action, businessAccountId } = params
    // Comment this out to use direct pay:
    // const methodOfPayment = 'CC' // We may need to handle more than one type at some point?

    if (!nrId) {
      // eslint-disable-next-line no-console
      console.warn('NR ID is not present in params, cannot continue!')
      throw new Error('NR ID is not present in params, cannot continue!')
    }

    // This is the minimum required to make a payment!
    // Any additional data supplied here, eg. supplying
    // a businessInfo object, will override values found
    // in the corresponding Name Request
    const data: any = {
      // Comment this out to use direct pay:
      // paymentInfo: {
      //   methodOfPayment: methodOfPayment
      // },
      businessAccountId: businessAccountId,
      filingInfo: {
        filingTypes: [
          {
            filingTypeCode: filingType,
            priority: priorityRequest || false
          }
        ]
      },
      headers: this.buildHeaders()
    }

    try {
      const paymentResponse = await this.createPaymentRequest(nrId, action, data)
      // set nr in session storage before redirecting to pay (this is how we find our way back afterwards)
      if (paymentResponse.nrNum?.includes('NR L')) {
        sessionStorage.setItem('BCREG-NRL', paymentResponse.nrNum)
        sessionStorage.setItem('BCREG-nrNum', null)
      } else if (paymentResponse.nrNum) {
        sessionStorage.setItem('BCREG-NRL', null)
        sessionStorage.setItem('BCREG-nrNum', paymentResponse.nrNum)
      }

      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { payment, sbcPayment = { receipts: [] } } = paymentResponse

      this.setPayment(payment)
      // this.setPaymentReceipt(sbcPayment.receipts[0]) // FUTURE: verify that new code === old code
      this.setPaymentRequest(data)

      // delete previous incomplete payments after the new payment record created
      const allPayments = await this.getNameRequestPayments(nrId, {})
      if (allPayments) {
        for (let i = 0; i < allPayments.length; i++) {
          if (
            allPayments[i].payment?.id !== payment.id &&
            allPayments[i].payment?.payment_action === action &&
            allPayments[i].sbcPayment?.statusCode === SbcPaymentStatus.CREATED
          ) {
            await NamexServices.cancelPayment(nrId, allPayments[i].sbcPayment.id)
          }
        }
      }

      if (onSuccess) {
        // Execute callback
        onSuccess(paymentResponse)
      }
      return true
    } catch (err) {
      if (err instanceof PaymentRequiredError) {
        this.$root.$emit('save-error-event', err.errorResponse)
        if (err.errorResponse.response.data.businessInfo?.businessIdentifier) {
          sessionStorage.setItem('BCREG-nrNum', err.errorResponse.response.data.businessInfo.businessIdentifier)
        }
        this.setAppError(
          { id: 'payment-required-error', error: 'Payment Required' } as ErrorI
        )
        throw err
      }
      // don't console.error - createPaymentRequest() already did that
      this.setAppError(
        { id: 'create-payment-error', error: 'Could not create payment' } as ErrorI
      )
      throw err
    }
  }

  /**
   * Returns header object with auth, content and account properties,
   * and optionally staff payment properties.
   */
  private buildHeaders (populateStaffPayment = true) {
    const headers = {}

    if (populateStaffPayment) {
      // Populate Staff Payment according to payment option
      switch (this.getStaffPayment.option) {
        case StaffPaymentOptions.FAS:
          headers['routingSlipNumber'] = this.getStaffPayment.routingSlipNumber
          break

        case StaffPaymentOptions.BCOL:
          headers['bcolAccountNumber'] = this.getStaffPayment.bcolAccountNumber
          headers['datNumber'] = this.getStaffPayment.datNumber
          headers['folioNumber'] = this.getStaffPayment.folioNumber // this overrides original folio number
          break

        case StaffPaymentOptions.NO_FEE:
          headers['waiveFees'] = true
          break

        case StaffPaymentOptions.NONE: // It is not a StaffPayment
          headers['folioNumber'] = this.getFolioNumber
          break
      }
    }

    const keycloakToken = sessionStorage.getItem(SessionStorageKeys.KeyCloakToken)
    // A BCSC or BCeID login with no Registries account pays by credit card as a guest.
    // Sending the token without Account-Id is what makes that payment fail.
    if (keycloakToken && !isLoggedInWithoutRegistriesAccount()) {
      headers['Authorization'] = `Bearer ${keycloakToken}`
      headers['Content-Type'] = 'application/json'
    }

    const currentAccount = sessionStorage.getItem(SessionStorageKeys.CurrentAccount)
    if (currentAccount) {
      try {
        const accountId = JSON.parse(currentAccount)?.id
        if (accountId) headers['Account-Id'] = accountId
      } catch {
        // Header stores "" or "undefined" when the login has no Registries account.
      }
    }

    return headers
  }

  /**
   * Navigate to the Service BC Payment Portal.
   * The return URL should specify payment ID so we can
   * grab the payment when we're directed back to this app!
   * @param paymentToken
   * @param returnUrl
   */
  navigateToPaymentPortal (paymentToken: string, returnUrl: string) {
    const paymentPortalUrl = sessionStorage.getItem('PAYMENT_PORTAL_URL')
    const url = `${paymentPortalUrl}${paymentToken}/${returnUrl}`
    Navigate(url)
  }

  /**
   * Grab the receipt PDF and download / display it for the user...
   * @param paymentId
   */
  async downloadReceiptPdf (paymentId) {
    try {
      const response = await this.generateReceiptRequest(paymentId)
      const url = window.URL.createObjectURL(new Blob([response], { type: 'application/pdf' }))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `payment-receipt-${paymentId}.pdf`)
      document.body.appendChild(link)
      link.click()
    } catch (err) {
      // don't console.error - generateReceiptRequest() already did that
      this.setAppError(
        { id: 'download-receipt-pdf-error', error: 'Could not download receipt PDF' } as ErrorI
      )
    }
  }

  /**
   * Fetches the specified NR payment.
   * @param nrId the NR id
   * @param paymentId the payment id
   * @returns True if successful, otherwise False
   */
  async fetchNrPayment (nrId: number, paymentId: number): Promise<boolean> {
    try {
      const token = sessionStorage.getItem(SessionStorageKeys.KeyCloakToken)
      const accountInfo = sessionStorage.getItem(SessionStorageKeys.CurrentAccount)
      let headers = {}
      if (token && accountInfo) {
        const parsedAccountInfo = JSON.parse(accountInfo)
        headers = {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
          'Account-Id': parsedAccountInfo.id
        }
      }
      const paymentResponse = await this.getNameRequestPayment(nrId, paymentId, headers)
      if (!paymentResponse) throw new Error('Got error from getNameRequestPayment()')

      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      // Note this is broken the true response should be paymentResponse[0]
      // but this is called by many different pathways will need to fix in the future.
      const { payment, sbcPayment = { receipts: [], status_code: '' } } = paymentResponse

      this.setPayment(payment)
      this.setSbcPayment(sbcPayment)
      if (
        sbcPayment &&
        sbcPayment.receipts instanceof Array &&
        sbcPayment.receipts.length > 0
      ) {
        const receipt = sbcPayment.receipts[0]
        this.setPaymentReceipt(receipt)
      }
      return true
    } catch (err) {
      // don't console.error - getNameRequestPayment() already did that
      this.setAppError(
        { id: 'fetch-nr-payment-error', error: 'Could not fetch NR payment' }
      )
      return false
    }
  }

  /**
   * Fetches all payments for the specified NR.
   * @param nrId the NR id
   * @returns True if successful, otherwise False
   */
  async fetchNrPayments (nrId: number): Promise<boolean> {
    try {
      const paymentsResponse = await this.getNameRequestPayments(nrId, {})
      if (!paymentsResponse) throw new Error('Got error from getNameRequestPayments()')

      this.setPayments(paymentsResponse)

      // find the first payment in the returned array that has action = CREATE and has sbcPayment.folioNumber set
      const paymentWithFolio = paymentsResponse?.find(
        payment =>
          payment?.action === PaymentAction.CREATE &&
          payment?.sbcPayment?.folioNumber
      )
      if (paymentWithFolio?.sbcPayment?.folioNumber) {
        this.setFolioNumber(paymentWithFolio.sbcPayment.folioNumber)
      }

      return true
    } catch (err) {
      // don't console.error - getNameRequestPayments() already did that
      this.setAppError(
        { id: 'fetch-nr-payments-error', error: 'Could not fetch NR payments' }
      )
      return false
    }
  }

  // FUTURE: move to NamexServices
  async createPaymentRequest (nrId, action, data: any): Promise<NameRequestPaymentResponse> {
    const url = `${namexApiUrl}/payments/${nrId}/${action}`
    try {
      const response = await NamexServices.axios.post(url, data)
      if (response?.data && [OK, CREATED, ACCEPTED, NO_CONTENT].includes(response?.status)) {
        return response.data
      }
      throw new Error(`Invalid response = ${response}`)
    } catch (error) {
      const err = error as any
      if (err?.response?.status === PAYMENT_REQUIRED) {
        throw new PaymentRequiredError(err)
      }
      console.error('createPaymentRequest() =', err) // eslint-disable-line no-console
      const msg = await this.handleApiError(err, 'Could not create payment request')
      // console.error('createPaymentRequest() =', msg) // eslint-disable-line no-console
      throw new Error(msg)
    }
  }

  // FUTURE: move to NamexServices
  async getNameRequestPayment (nrId, paymentId, data: any): Promise<NameRequestPaymentResponse> {
    const url = `${namexApiUrl}/payments/${nrId}/payment/${paymentId}`
    try {
      const response = await NamexServices.axios.get(url, data)
      // FUTURE: check response status and data - make sure error handling is not changed
      return response.data
    } catch (err) {
      const msg = await this.handleApiError(err, 'Could not get name request payment')
      console.error('getNameRequestPayment() =', msg) // eslint-disable-line no-console
      throw new Error(msg)
    }
  }

  // FUTURE: move to NamexServices
  async getNameRequestPayments (nrId, data: any): Promise<NameRequestPaymentResponse[]> {
    const url = `${namexApiUrl}/payments/${nrId}`
    try {
      const response = await NamexServices.axios.get(url, data)
      // FUTURE: check response status and data - make sure error handling is not changed
      return response.data
    } catch (err) {
      const msg = await this.handleApiError(err, 'Could not get name request payments')
      console.error('getNameRequestPayments() =', msg) // eslint-disable-line no-console
      throw new Error(msg)
    }
  }

  // FUTURE: move to NamexServices
  async _getPaymentFees (data: any): Promise<any> {
    const url = `${namexApiUrl}/payments/fees`
    try {
      // FUTURE: check response status and data - make sure error handling is not changed
      const response = await NamexServices.axios.post(url, data)
      return response.data
    } catch (err) {
      const msg = await this.handleApiError(err, 'Could not get payment fees')
      console.error('_getPaymentFees() =', msg) // eslint-disable-line no-console
      throw new Error(msg)
    }
  }

  // FUTURE: move to NamexServices
  async generateReceiptRequest (paymentId): Promise<any> {
    const params = { responseType: 'arraybuffer' } as AxiosRequestConfig
    const url = `${namexApiUrl}/payments/${paymentId}/receipt`
    try {
      const response = await NamexServices.axios.post(url, {}, params)
      // FUTURE: check response status and data - make sure error handling is not changed
      return response.data
    } catch (err) {
      const msg = await this.handleApiError(err, 'Could not generate payment receipt')
      console.error('generateReceiptRequest() =', msg) // eslint-disable-line no-console
      throw new Error(msg)
    }
  }
}
