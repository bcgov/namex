import { Component, Vue } from 'vue-property-decorator'
import { NameRequestPaymentResponse } from '@/interfaces'
import { PaymentAction } from '@/enums'

@Component({})
export class PaymentSessionMixin extends Vue {
  get paymentInProgress (): boolean {
    return (sessionStorage.getItem('paymentInProgress') === 'true')
  }

  get sessionPaymentId () {
    return (this.paymentInProgress && sessionStorage.getItem('paymentId'))
      ? parseInt(sessionStorage.getItem('paymentId'))
      : undefined
  }

  get sessionPaymentAction () {
    return (this.paymentInProgress && sessionStorage.getItem('paymentAction'))
      ? sessionStorage.getItem('paymentAction')
      : undefined
  }

  get sessionPaymentToken () {
    return (this.paymentInProgress && sessionStorage.getItem('paymentToken'))
      ? sessionStorage.getItem('paymentToken')
      : undefined
  }

  get sessionNrId () {
    return (this.paymentInProgress && sessionStorage.getItem('nrId'))
      ? sessionStorage.getItem('nrId')
      : undefined
  }

  get sessionId () {
    return (this.paymentInProgress && sessionStorage.getItem('nrId'))
      ? sessionStorage.getItem('nrId')
      : undefined
  }

  /**
   * @param paymentAction A PaymentAction - one of [CREATE, REAPPLY, RESUBMIT, UPGRADE]
   * @param paymentResponse
   */
  savePaymentResponseToSession (paymentAction: PaymentAction, paymentResponse: NameRequestPaymentResponse) {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { id, nrId, payment, sbcPayment = { receipts: [] }, token, statusCode, completionDate } = paymentResponse

    // FUTURE: Remove this one, we don't want to set the payment to session once we're done!
    // FUTURE: Or... we could add a debug payments mode?
    sessionStorage.setItem('payment', `${JSON.stringify(payment)}`)
    sessionStorage.setItem('paymentAction', `${paymentAction}`)
    // Store the payment ID to sessionStorage, that way we can start the user back where we left off
    sessionStorage.setItem('paymentInProgress', 'true')
    sessionStorage.setItem('paymentId', `${id}`)
    sessionStorage.setItem('paymentToken', `${token}`)
    sessionStorage.setItem('nrId', `${nrId}`)
  }

  /**
   * @param paymentAction A PaymentAction - same as in original payment response
   * @param pendingPayment
   */
  savePendingPaymentToSession (paymentAction: PaymentAction, pendingPayment: any) {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { id, token, nrId, action } = pendingPayment

    // FUTURE: Remove this one, we don't want to set the payment to session once we're done!
    // FUTURE: Or... we could add a debug payments mode?
    sessionStorage.setItem('paymentInProgress', 'true')
    sessionStorage.setItem('paymentId', id)
    sessionStorage.setItem('paymentToken', token)
    sessionStorage.setItem('nrId', nrId)
    sessionStorage.setItem('paymentAction', paymentAction)
  }
}
