/** Enum for NR Action codes. Not to be confused with Request Code. */
export enum NrAction {
  CANCEL = 'CANCEL',
  EDIT = 'EDIT',
  RENEW = 'REAPPLY', // REAPPLY in API is RENEW in UI
  RECEIPTS = 'RECEIPT',
  REQUEST_REFUND = 'REQUEST_REFUND',
  RESEND = 'RESEND', // FUTURE: will be removed
  RESUBMIT = 'RESUBMIT',
  RESULT = 'RESULT',
  UPGRADE = 'UPGRADE',
  RETRY_PAYMENT = 'RETRY_PAYMENT',
  INCORPORATE = 'INCORPORATE'
}
