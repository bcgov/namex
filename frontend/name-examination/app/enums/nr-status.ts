export enum Status {
  /** A name approval was halted for some reason */
  Hold = 'HOLD',
  /** An examiner is working on this request */
  InProgress = 'INPROGRESS',
  /** Unexamined name, submitted by a client */
  Draft = 'DRAFT',
  /** LEGACY state for expired NRs from NRO */
  Expired = 'EXPIRED',
  /** Historical */
  Historical = 'HISTORICAL',
  /** The request is cancelled and cannot be changed */
  Cancelled = 'CANCELLED',
  /** Approved request, this is a final state */
  Approved = 'APPROVED',
  /** Approved, but with conditions to be met */
  Conditional = 'CONDITIONAL',
  /** Temporary reserved state with consent required */
  ConditionalReserved = 'COND_RESERVE',
  /** Approved, with conditions met. This is a final state */
  Condition = 'CONDITION',
  /** CONSUMED by a corp" */
  Consumed = 'CONSUMED',
  /** Rejected request, this is a final state */
  Rejected = 'REJECTED',
  /** COMPLETED - LEGACY state for completed NRs from NRO */
  Completed = 'COMPLETED',
  /** New name not yet examined */
  NotExamined = 'NE',
  /** The request is cancelled and a refund for all payments has been requested */
  RefundRequested = 'REFUND_REQUESTED',
  Reserved = 'RESERVED',
  /** Internal state used when updating records from NRO" */
  NROUpdating = 'NRO_UPDATING',
  /** NR is in a pending deletion state */
  PendingDeletion = 'PENDING_DELETION',
  /** NR has been created, but payment is not completed yet */
  PendingPayment = 'PENDING_PAYMENT',
}
