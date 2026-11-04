import {
  AnalysisJSONI, ApplicantI, ConversionTypesI, ExistingRequestSearchI, NameRequestI, RequestActionsI,
  RequestNameI, SelectOptionsI, StatsI, SubmissionTypeT, WaitingAddressSearchI
} from '@/interfaces/models'
import { BusinessSearchIF, NameChoicesIF, NrDataIF, RequestOrConsentIF } from '@/interfaces'
import { CompanyTypes, EntityTypes, Location, NrAffiliationErrors, NrRequestActionCodes, NrRequestTypeCodes }
  from '@/enums'

type RequestNameMapI = RequestNameI

export interface NewRequestIF {
  actingOnOwnBehalf: boolean
  addressSuggestions: any[]
  affiliationErrorModalValue: NrAffiliationErrors
  allowAutoApprove: boolean
  analysisJSON: AnalysisJSONI
  applicant: ApplicantI
  assumedNameOriginal: string
  conditionsModalVisible: boolean
  conflictId: string
  conversionType: NrRequestTypeCodes
  conversionTypeAddToSelect: ConversionTypesI
  corpNum: string
  corpSearch: string
  designationIssueTypes: string[]
  displayedComponent: string
  doNotAnalyzeEntities: EntityTypes[]
  editMode: boolean
  entity_type_cd: EntityTypes
  entityTypeAddToSelect: SelectOptionsI
  errorAmalgamateNow: boolean,
  errorContinuationIn: boolean,
  errorIncorporateNow: boolean,
  errors: string[]
  exitIncompletePaymentVisible: boolean
  exitModalVisible: boolean
  existingRequestSearch: ExistingRequestSearchI
  extendedRequestType: SelectOptionsI
  folioNumber?: string
  getNameReservationFailed: boolean
  helpMeChooseModalVisible: boolean
  isLearBusiness: boolean
  isLoadingSubmission: boolean
  isPersonsName: boolean
  issueIndex: number
  location: Location
  mrasSearchInfoModalVisible: boolean
  mrasSearchResultCode: number
  name: string
  nameAnalysisTimedOut: boolean
  nameChoices: NameChoicesIF
  nameIsEnglish: boolean
  nameOriginal: string
  noCorpNum: boolean
  nr: Partial<NameRequestI>
  nrData: NrDataIF
  nrOriginal: Partial<NameRequestI>
  nrRequestNameMap: RequestNameMapI[]
  nrRequiredModalVisible: boolean
  numberedCompanyHelpModalVisible: boolean
  origin_entity_type_cd: EntityTypes
  pickEntityModalVisible: boolean
  priorityRequest: boolean
  quickSearchNames: any[]
  request_action_cd: NrRequestActionCodes
  request_jurisdiction_cd: string
  requestExaminationOrProvideConsent: RequestOrConsentIF
  search: {
    business: BusinessSearchIF
    companyType: CompanyTypes
    jurisdiction: any
    request: RequestActionsI
  }
  showActualInput: boolean
  societiesModalVisible: boolean
  stats: StatsI
  submissionTabNumber: number
  submissionType: SubmissionTypeT
  tabNumber: number
  userCancelledAnalysis: boolean
  waitingAddressSearch: WaitingAddressSearchI
  businessAccountId: string
}
