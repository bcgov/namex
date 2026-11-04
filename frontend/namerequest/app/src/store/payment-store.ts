import { defineStore } from 'pinia'
import { FilingTypes, PaymentStatus } from '@/enums'

export const usePaymentStore = defineStore('payment', {
  state: () => ({
    // The payment reference
    references: [
      {
        id: '',
        receiptNumber: '',
        statusCode: ''
      }
    ],
    isConfirmNrVisible: false,
    isPaymentHistoryVisible: false,
    isRefundVisible: false,
    isCancelVisible: false,
    isUpgradeVisible: false,
    isResubmitVisible: false,
    isRetryVisible: false,
    isRenewVisible: false,
    isPaymentCompleteVisible: false,
    isProcessing: false,
    filingTypeCode: FilingTypes.NM606,
    entity_type_cd: null,
    filingDescription: '',
    waiveFees: false,
    priority: false,
    futureEffective: false,
    fees: {
      filingFees: 0.0,
      filingType: '',
      filingTypeCode: undefined,
      futureEffectiveFees: 0.0,
      priorityFees: 0.0,
      processingFees: 0.0,
      serviceFees: 0.0,
      tax: {} as any,
      total: 0.0
    },
    request: {} as any,
    payment: {} as any,
    sbcPayment: {
      paymentStatus: '' // should this be statusCode instead?
    } as any,
    payments: [],
    receipt: {
      id: undefined,
      receiptAmount: 0.00,
      receiptDate: '',
      receiptNumber: ''
    },
    receipts: []
  }),

  getters: {
    confirmNrModalIsVisible (): boolean {
      return this.isConfirmNrVisible
    },

    paymentHistoryModalIsVisible (): boolean {
      return this.isPaymentHistoryVisible
    },

    refundModalIsVisible (): boolean {
      return this.isRefundVisible
    },

    cancelModalIsVisible (): boolean {
      return this.isCancelVisible
    },

    upgradeModalIsVisible (): boolean {
      return this.isUpgradeVisible
    },

    resubmitModalIsVisible (): boolean {
      return this.isResubmitVisible
    },

    retryModalIsVisible (): boolean {
      return this.isRetryVisible
    },

    renewModalIsVisible (): boolean {
      return this.isRenewVisible
    },

    paymentCompleteModalIsVisible (): boolean {
      return this.isPaymentCompleteVisible
    },

    paymentIsInProgress (): boolean {
      return this.isProcessing
    },

    getSbcPayment (): any {
      return this.sbcPayment
    },

    getSbcPaymentStatus (): string {
      return this.sbcPayment
        ? this.sbcPayment.statusCode
        : undefined
    },

    getPayment (): any {
      return this.payment
    },

    getPaymentId (): number {
      return this.payment.id
    },

    getPaymentToken (): string {
      return this.payment.payment_token
    },

    getPaymentStatus (): PaymentStatus {
      return (
        this.sbcPayment.paymentStatus ||
        this.payment.payment_status_code
      )
    },

    getPaymentDate (): any {
      // FUTURE: should this return payment_completion_date instead?
      return this.payment.payment_status_code
    },

    getPaymentFees (): any {
      return this.fees
    },

    getPaymentDetails (): any {
      // FUTURE: delete these state properties if obsolete
      const {
        filingTypeCode,
        entity_type_cd,
        filingDescription,
        waiveFees,
        priority,
        futureEffective
      } = this

      return {
        filingTypeCode,
        entity_type_cd,
        filingDescription,
        waiveFees,
        priority,
        futureEffective
      }
    },

    getPaymentRequest (): any {
      let paymentRequestState
      if (
        (!this.request || Object.keys(this.request).length === 0) &&
        sessionStorage.getItem('paymentRequest')
      ) {
        paymentRequestState = JSON.parse(sessionStorage.getItem('paymentRequest'))
      } else {
        paymentRequestState = this.request
      }

      return paymentRequestState
    },

    getPaymentReceipt (): any {
      return this.receipt
    },

    getPayments (): any[] {
      return this.payments
    }
  },

  actions: {
    setPayment (payment: any) {
      this.payment = payment || {}
    },

    setPaymentFees (fees: any) {
      if (fees) {
        this.fees = fees
      }
    },

    setPaymentIsProcessing (isProcessing: boolean) {
      this.isProcessing = isProcessing || false
    },

    setPaymentReceipt (receipt: any) {
      this.receipt = receipt || {}
    },

    setPaymentRequest (req: any) {
      this.request = req || {}
      sessionStorage.setItem('paymentRequest', JSON.stringify(req))
    },

    setPayments (payments: any[]) {
      this.payments = payments || []
    },

    setSbcPayment (sbcPayment: any) {
      this.sbcPayment = sbcPayment || {}
    },

    toggleCancelModal (isVisible: boolean) {
      this.isCancelVisible = isVisible || false
    },

    toggleConfirmNrModal (isVisible: boolean) {
      this.isConfirmNrVisible = isVisible || false
    },

    togglePaymentHistoryModal (isVisible: boolean) {
      this.isPaymentHistoryVisible = isVisible || false
    },

    toggleReceiptModal (isVisible: boolean) {
      this.isPaymentCompleteVisible = isVisible || false
    },

    toggleRefundModal (isVisible: boolean) {
      this.isRefundVisible = isVisible || false
    },

    toggleRenewModal (isVisible: boolean) {
      this.isRenewVisible = isVisible || false
    },

    toggleResubmitModal (isVisible: boolean) {
      this.isResubmitVisible = isVisible || false
    },

    toggleRetryModal (isVisible: boolean) {
      this.isRetryVisible = isVisible || false
    },

    toggleUpgradeModal (isVisible: boolean) {
      this.isUpgradeVisible = isVisible || false
    }
  }
})
