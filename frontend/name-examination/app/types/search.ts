import {
  ClientNotification,
  ConsentRequired,
  LastUpdate,
  Priority,
  Submitted,
} from '~/enums/filter-dropdowns'

import type { SearchColumns } from '~/enums/search-columns'

export type Filters = {
  [SearchColumns.Status]: StatusSearchFilter
  [SearchColumns.LastModifiedBy]: string
  [SearchColumns.NameRequestNumber]: string
  [SearchColumns.Names]: string
  [SearchColumns.ApplicantFirstName]: string
  [SearchColumns.ApplicantLastName]: string
  [SearchColumns.ConsentRequired]: ConsentRequired
  [SearchColumns.Priority]: Priority
  [SearchColumns.ClientNotification]: ClientNotification
  [SearchColumns.Submitted]: Submitted
  [SearchColumns.LastUpdate]: LastUpdate
}

export enum StatusSearchFilter {
  All = 'ALL',
  Hold = 'HOLD',
  InProgress = 'INPROGRESS',
  Draft = 'DRAFT',
  Expired = 'EXPIRED',
  Cancelled = 'CANCELLED',
  Approved = 'APPROVED',
  Conditional = 'CONDITIONAL',
  Consumed = 'CONSUMED',
  Rejected = 'REJECTED',
  Completed = 'COMPLETED',
}

export type Row = {
  [column in SearchColumns]: string
}

export type FilterKey = keyof Filters
