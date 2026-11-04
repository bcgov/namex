import { FilingTypes, Jurisdictions, PaymentAction } from '@/enums'
import { ErrorI } from '@/interfaces'

export interface NameRequestPaymentResponse {
  action: PaymentAction
  id: number
  nrId: string
  nrNum: string
  token: number
  statusCode: string
  completionDate: string
  payment: any
  sbcPayment: any
}

export interface NameRequestPayment {
  payment?: any
  paymentSuccess: boolean
  paymentErrors?: ErrorI[]
  statusCode?: string
  httpStatusCode?: string
}

export interface NameRequestReceipt {
  id?: any
  receiptAmount?: number
  receiptDate?: string
  receiptNumber?: string
}

export interface CreatePaymentParams {
  action: string // FUTURE: use type 'NrAction' or 'NrRequestActionCodes' ?
  nrId: number
  filingType: string // FUTURE: use type 'FilingTypes' ?
  priorityRequest: boolean,
  businessAccountId: string
}

export interface FetchFeesParams {
  filingType: FilingTypes
  jurisdiction: Jurisdictions
  priorityRequest: boolean
}
