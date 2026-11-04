import { PaymentMethod, RefundMessage, RefundStatus } from '~/enums/codes'
import { type Payment } from '~/types'
import { emitter } from '~/util/emitter'
import { getPayments } from '~/util/namex-api'

export const usePayments = defineStore('payments', () => {
  const payments = ref<Array<Payment>>([])

  const isNoFeePayment = computed(() => {
    if (payments.value.length === 0) {
      return true
    } else if (payments.value.length === 1) {
      return payments.value[0].sbcPayment.paid === 0
    } else {
      const total = payments.value.reduce((a, b) => a + b.sbcPayment.paid, 0)
      return total === 0
    }
  })

  const isNoRefund = computed(() => {
    if (payments.value.length === 0) {
      return true
    } else if (payments.value.length === 1) {
      return payments.value[0].refund === 0
    } else {
      const total = payments.value.reduce((a, b) => a + b.sbcPayment.refund, 0)
      return total === 0
    }
  })

  const isDifferentPaymentStatus = computed(() => {
    if (payments.value.length > 1) {
      return payments.value
        .map((payment) => payment.sbcPayment.statusCode)
        .some((method) => method !== payments.value[0].sbcPayment.statusCode)
    }
    return false
  })

  const refundState = computed(() => {
    const paymentMethod = payments.value[0].sbcPayment.paymentMethod
    const paymentStatus = payments.value[0].sbcPayment.statusCode
    if (paymentStatus === RefundStatus.Refunded) {
      return RefundMessage.Completed
    } else if (paymentStatus === RefundStatus.Credited) {
      return RefundMessage.Credited
    } else if (paymentStatus === RefundStatus.Cancelled) {
      return RefundMessage.Cancelled
    } else {
      // REFUND_REQUESTED or other status
      if (paymentMethod === PaymentMethod.Pad) {
        // Premium Account
        if (!isNoRefund.value) {
          return RefundMessage.Requested
        } else {
          return RefundMessage.NotProcessed
        }
      } else if (paymentMethod === PaymentMethod.Internal) {
        // INTERNAL is a Staff payment. It can be 'Routing Slip' or 'No Fee' payments.
        return RefundMessage.NotProcessed
      } else if (
        [PaymentMethod.DirectPay, PaymentMethod.DrawDown].includes(
          paymentMethod
        )
      ) {
        // Credit Card or BCOL
        if (!isNoFeePayment.value) {
          return RefundMessage.Processed
        } else {
          return RefundMessage.Completed
        }
      }
    }
  })

  const refundPaymentState = computed(() => {
    if (payments.value.length > 0) {
      if (payments.value.length === 1) {
        return refundState.value
      } else {
        // More than 1 payment. (e.g. paid priority service)
        if (!isDifferentPaymentStatus.value) {
          // all payments have the same status
          return refundState.value
        } else {
          // the payments have the different status (e.g one REFUNDED and another one REFUND_REQUESTED)
          if (!isNoRefund.value) {
            // Multi-transaction scenario returns success
            return RefundMessage.Processed
          } else {
            // This should not happen
            return RefundMessage.NotProcessed
          }
        }
      }
    }
  })

  async function initialize(id: number) {
    const response = await getPayments(id)
    if (!response.ok) {
      emitter.emit('error', {
        title: 'Payments Error',
        message: 'Failed to get payment data.',
      })
      return
    }
    payments.value = await response.json()
  }

  return { initialize, refundPaymentState }
})
