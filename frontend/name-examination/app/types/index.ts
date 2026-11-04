import type {
  ClassTypeCode,
  ConsentFlag,
  EntityTypeCode,
  PaymentMethod,
  RefundStatus,
  RequestActionCode,
  RequestTypeCode,
} from '~/enums/codes'
import type { Status } from '~/enums/nr-status'

export interface NameChoice {
  choice: number
  name: string | null
  state: Status
  decision_text: string | null
  conflict1: string | null
  conflict2: string | null
  conflict3: string | null
  consumptionDate: string | null
  corpNum: string | null
  conflict1_num: string | null
  conflict2_num: string | null
  conflict3_num: string | null
  comment: string | null
}

export interface Comment {
  comment: string
  examiner: string
  timestamp: string
}

export type ConflictData = NameRequest | Corporation

export interface Corporation {
  'identifier': string
  directors: string[]
  'nature of business': string
  jurisdiction: string
}

export interface BCCorporation extends Corporation {
  'records office delivery address': string[]
  'registered office delivery address': string[]
}

export interface XproCorporation extends Corporation {
  'attorney names': string[]
  'head office': string[]
}

export interface HistoryEntry {
  name: string
  jurisdiction: string
  nr_num: string
  start_date: string
  name_state_type_cd: string
  score: number
  submit_count: number
}

export interface Histories {
  names: Array<HistoryEntry>
  highlighting: string
  response: {
    maxScore: number
    name: string
    numFound: number
    /** string representing number of rows */
    rows: string
    start: number
  }
}

export enum ConflictSource {
  Corp = 'CORP',
  NameRequest = 'NAMEREQUEST',
  NRO = 'NRO',
}

export interface ConflictListItem {
  text: string
  highlightedText: string
  jurisdiction: string | undefined
  nrNumber: string
  startDate: string
  source: ConflictSource
  /** Properties related to how this object is presented in the UI */
  ui: {
    focused: boolean
    open: boolean
  }
}

export interface ConflictList {
  text: string
  highlightedText: string
  meta: string | undefined
  children: Array<ConflictListItem>
  /** Properties related to how this object is presented in the UI */
  ui: {
    focused: boolean
    open: boolean
  }
}

export interface Condition {
  id: number
  phrase: string
  text: string
  allow_use: 'Y' | 'N'
  consent_required: 'Y' | 'N'
  instructions: string
}

export interface ConditionsList {
  restricted_words_conditions: Array<{
    cnd_info: Array<{
      allow_use: 'Y' | 'N'
      consent_required: 'Y' | 'N'
      consenting_body: string
      id: number
      instructions: string
      text: string
    }>
    word_info: {
      id: number
      phrase: string
    }
  }>
}

export interface Macro {
  id: number
  name: string
  reason: string
}

export interface Trademark {
  application_number: string
  description: string
  name: string
  score: number
  status: string
}

export interface TrademarksObject {
  names: Array<Trademark>
  highlighting: {
    [key: string]: {
      name?: Array<string>
    }
  }
  response: {
    maxScore: number
    name: string
    numFound: number
    /** string representing number of rows */
    rows: string
    start: number
  }
}

export interface RequestType {
  value: RequestTypeCode
  text: string
  short_desc: string
  class_type_cd: ClassTypeCode
  legacy_cd: string
  additional_info: string
  source_application: 'COLIN' | ''
  entity_type_cd: EntityTypeCode
  request_action_cd: RequestActionCode
}

export interface RequestTypeRule {
  request_type: string
  jurisdiction_required: boolean
  prev_nr_required: boolean
  corp_num_required: boolean
  additional_info_template: string
  is_lp_nwpta_type: boolean
  is_cp_nwpta_type: boolean
}

export interface Jurisdiction {
  /** two letter code */
  value: string
  short_desc: string
  text: string
}

export interface Transactions {
  response: {
    count: number
  }
  transactions: Array<TransactionEntry>
}

export interface TransactionEntry {
  id: string
  additionalInfo: string
  consentFlag: ConsentFlag
  /** consent date */
  consent_dt: string | null
  corpNum: string | null
  eventDate: string
  expirationDate: string | null
  furnished: 'Y' | 'N'
  names: Array<NameChoice>
  priorityCd: 'Y' | 'N'
  requestTypeCd: RequestTypeCode
  request_action_cd: RequestActionCode
  stateCd: Status
  user_action: string
  user_name: string
  comment?: string
  option?: string
  email?: Email
  resend_date?: string
}

export interface Email {
  recipients: string
  content: {
    subject: string
    body: string
    attachments?: Array<EmailAttachment>
  }
}

export interface EmailAttachment {
  fileName: string
  attachOrder: string
  fileUrl: string
  fileBytes: string
}

export interface Action {
  URL: string
  entitiesFilingName: string
  filingName: string
  learTemplate?: string
}

export interface Applicant {
  addrLine1: string
  addrLine2: string | null
  addrLine3: string | null
  city: string
  clientFirstName: string | null
  clientLastName: string | null
  contact: string
  countryTypeCd: string
  declineNotificationInd: any
  emailAddress: string
  faxNumber: string | null
  firstName: string
  lastName: string
  middleName: string | null
  partyId: number
  phoneNumber: string
  postalCd: string
  stateProvinceCd: string
}

export interface NameRequest {
  actions: Array<Action>
  additionalInfo: string | null
  applicants: Applicant
  checkedOutBy: string | null
  checkedOutDt: string | null
  comments: Array<Comment>
  consentFlag: ConsentFlag | null
  consent_dt: string | null
  corpNum: string | null
  entity_type_cd: EntityTypeCode
  expirationDate: string | null
  furnished: 'Y' | 'N'
  hasBeenReset: boolean
  homeJurisNum: string | null
  details: unknown | null
  id: number
  lastUpdate: string
  legalType: string
  names: Array<NameChoice>
  natureBusinessInfo: string | null
  notifiedBeforeExpiry: boolean
  notifiedExpiry: boolean
  nrNum: string
  nwpta: Array<unknown>
  previousNr: string | null
  previousRequestId: string | null
  previousStateCd: Status | null
  priorityCd: 'Y' | 'N'
  priorityDate: string
  requestTypeCd: RequestTypeCode
  request_action_cd: RequestActionCode
  source: string | null
  state: Status
  stateCd: Status
  submitCount: number
  submittedDate: string
  submitter_userid: string
  target: string
  tradeMark: string | null
  userId: string
  xproJurisdiction: string | null
}

export interface Payment {
  sbcPayment: {
    paid: number
    refund: number
    statusCode: RefundStatus
    paymentMethod: PaymentMethod
  }
  refund: number
}
