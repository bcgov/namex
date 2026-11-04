export class PaymentRequiredError extends Error {
  constructor (errorResponse) {
    super()
    this.errorResponse = errorResponse
  }
  errorResponse: any
}
