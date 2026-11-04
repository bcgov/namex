import Vue from 'vue'
import {
  AnalysisJSONI,
  BusinessSearchIF,
  ConditionalInstructionI,
  ConversionTypesI,
  NameRequestI,
  RefundParamsIF,
  RequestActionsI,
  SelectOptionsI,
  StaffPaymentIF,
  StateIF,
  StatsI,
  SubmissionTypeT,
  WaitingAddressSearchI
} from '@/interfaces'
import {
  AuthorizedActions,
  CompanyTypes,
  EntityTypes,
  Location,
  NameCheckErrorType,
  NrAffiliationErrors,
  NrRequestActionCodes,
  NrRequestTypeCodes,
  PriorityCode
} from '@/enums'

export const clearErrors = (state: StateIF) => {
  state.newRequestModel.errors = []
}

export const mutateActingOnOwnBehalf = (state: StateIF, actingOnOwnBehalf: boolean) => {
  state.newRequestModel.actingOnOwnBehalf = actingOnOwnBehalf
}

export const mutateAddressSuggestions = (state: StateIF, addressSuggestions: any[]) => {
  if (!addressSuggestions) {
    state.newRequestModel.addressSuggestions = null
  } else {
    state.newRequestModel.addressSuggestions = Object.assign([], addressSuggestions)
  }
}

export const mutateAnalysisJSON = (state: StateIF, analysisJSON: AnalysisJSONI) => {
  state.newRequestModel.analysisJSON = analysisJSON
}

export const mutateApplicant = (state: StateIF, appKV: any) => {
  if (Array.isArray(appKV)) {
    for (const element of appKV) {
      state.newRequestModel.applicant[element.name] = element.value
    }
  }
  if (appKV.key === 'postalCd') {
    appKV.value = appKV.value.toUpperCase()
  }
  state.newRequestModel.applicant[appKV.key] = appKV.value
  // sessionStorage.setItem('BCREG-emailAddress', state.newRequestModel.applicant?.emailAddress)
  // sessionStorage.setItem('BCREG-phoneNumber', state.newRequestModel.applicant?.phoneNumber)
}

export const mutateConflictId = (state: StateIF, conflictId: string) => {
  state.newRequestModel.conflictId = conflictId
}

export const mutateConversionType = (state: StateIF, conversionType: NrRequestTypeCodes) => {
  state.newRequestModel.conversionType = conversionType
}

export const mutateConversionTypeAddToSelect = (state: StateIF, conversionTypeAddToSelect: ConversionTypesI) => {
  state.newRequestModel.conversionTypeAddToSelect = conversionTypeAddToSelect
}

export const mutateCorpNum = (state: StateIF, corpNum: string) => {
  state.newRequestModel.corpNum = corpNum
}

export const mutateCorpSearch = (state: StateIF, corpNum: string) => {
  state.newRequestModel.corpSearch = corpNum
}

export const mutateDisplayedComponent = (state: StateIF, componentName: string) => {
  state.newRequestModel.displayedComponent = componentName
}

export const mutateEditMode = (state: StateIF, editMode: boolean) => {
  state.newRequestModel.editMode = editMode
}

export const mutateEntityType = (state: StateIF, entity_type_cd: EntityTypes) => {
  state.newRequestModel.entity_type_cd = entity_type_cd
}

export const mutateOriginEntityType = (state: StateIF, origin_entity_type_cd: EntityTypes) => {
  state.newRequestModel.origin_entity_type_cd = origin_entity_type_cd
}

export const mutateEntityTypeAddToSelect = (state: StateIF, entityTypeAddToSelect: SelectOptionsI) => {
  state.newRequestModel.entityTypeAddToSelect = entityTypeAddToSelect
}

export const resetEntityTypeAddToSelect = (state: StateIF) => {
  state.newRequestModel.entityTypeAddToSelect = null
}

export const mutateExistingRequestSearch = (state: StateIF, { key, value }) => {
  state.newRequestModel.existingRequestSearch[key] = value
}

export const mutateExistingRequestSearchToInitialState = (state: StateIF) => {
  state.newRequestModel.existingRequestSearch = {
    emailAddress: '',
    nrNum: '',
    phoneNumber: ''
  }
}

export const mutateExtendedRequestType = (state: StateIF, extendedRequestType: SelectOptionsI) => {
  state.newRequestModel.extendedRequestType = extendedRequestType
}

export const mutateGetNameReservationFailed = (state: StateIF, getNameReservationFailed: boolean) => {
  state.newRequestModel.getNameReservationFailed = getNameReservationFailed
}

export const mutateHelpMeChooseModalVisible = (state: StateIF, helpMeChooseModalVisible: boolean) => {
  state.newRequestModel.helpMeChooseModalVisible = helpMeChooseModalVisible
}

export const mutateAffiliationErrorModalValue = (state: StateIF, affiliationErrorModalValue: NrAffiliationErrors) => {
  state.newRequestModel.affiliationErrorModalValue = affiliationErrorModalValue
}

export const mutateIsLearBusiness = (state: StateIF, isLearBusiness: boolean) => {
  state.newRequestModel.isLearBusiness = isLearBusiness
}

export const mutateIsPersonsName = (state: StateIF, isPersonsName: boolean) => {
  state.newRequestModel.isPersonsName = isPersonsName
}

export const mutateLocation = (state: StateIF, location: Location) => {
  // don't reset location if it hasn't changed
  if (location === state.newRequestModel.location) {
    return
  }

  // reset entity type on location changes (options depend on location)
  // except amalgamation since entity type was set before location
  if (state.newRequestModel.request_action_cd !== NrRequestActionCodes.AMALGAMATE) {
    state.newRequestModel.entity_type_cd = null
  }

  if (
    state.newRequestModel.location === Location.CA ||
    state.newRequestModel.location === Location.IN
  ) {
    if (location === Location.CA || location === Location.IN) {
      state.newRequestModel.location = location
      return
    }
  }

  // reset recently-used entry on location changes
  // except amalgamation since recently-used entry was set before location
  if (state.newRequestModel.request_action_cd !== NrRequestActionCodes.AMALGAMATE) {
    state.newRequestModel.entityTypeAddToSelect = null
  }

  // finally, set location
  state.newRequestModel.location = location
}

export const mutateMrasSearchResult = (state: StateIF, mrasSearchResultCode: number) => {
  state.newRequestModel.mrasSearchResultCode = mrasSearchResultCode
}

export const mutateMrasSearchInfoModalVisible = (state: StateIF, mrasSearchInfoModalVisible: boolean) => {
  state.newRequestModel.mrasSearchInfoModalVisible = mrasSearchInfoModalVisible
}

export const mutateJurisdictionCd = (state: StateIF, request_jurisdiction_cd: string) => {
  state.newRequestModel.request_jurisdiction_cd = request_jurisdiction_cd
}

export const mutateCurrentJsDate = (state: StateIF, date: Date) => {
  state.common.currentJsDate = date
}

export const mutateName = (state: StateIF, name: string) => {
  state.newRequestModel.name = name
}

export const mutateNameOriginal = (state: StateIF, nameOriginal: string) => {
  state.newRequestModel.nameOriginal = nameOriginal
}

export const mutateNoCorpNum = (state: StateIF, noCorpNum: boolean) => {
  state.newRequestModel.noCorpNum = noCorpNum
}

export const mutateNROriginal = (state: StateIF, nrOriginal: NameRequestI) => {
  state.newRequestModel.nrOriginal = nrOriginal
}

export const mutateNameChoices = (state: StateIF, choiceObj: any) => {
  state.newRequestModel.nameChoices[choiceObj.key] = choiceObj.value
}

export const mutateNameChoicesToInitialState = (state: StateIF) => {
  state.newRequestModel.nameChoices = {
    name1: '',
    designation1: '',
    name2: '',
    designation2: '',
    name3: '',
    designation3: ''
  }
}

export const mutateNameIsEnglish = (state: StateIF, nameIsEnglish: boolean) => {
  state.newRequestModel.nameIsEnglish = nameIsEnglish
}

export const mutateIsLoadingSubmission = (state: StateIF, isLoadingSubmission: boolean) => {
  state.newRequestModel.isLoadingSubmission = isLoadingSubmission
}

export const mutateNameRequest = (state: StateIF, nr: NameRequestI) => {
  // store NR data
  state.newRequestModel.nr = nr

  // store Priority Code
  mutatePriorityRequest(state, (nr?.priorityCd === PriorityCode.YES))

  // FUTURE: have 1 mutation for nr / applicant info and put these there
  const nrNum = state.newRequestModel.nr?.nrNum
  if (nrNum?.includes('NR L')) {
    sessionStorage.setItem('BCREG-NRL', nrNum)
    sessionStorage.setItem('BCREG-nrNum', null)
  } else if (nrNum) {
    sessionStorage.setItem('BCREG-NRL', null)
    sessionStorage.setItem('BCREG-nrNum', nrNum)
  }
}

export const mutateNameRequestByKey = (state: StateIF, kv: any) => {
  Vue.set(
    state.newRequestModel.nr,
    kv.key,
    kv.value
  )
  // FUTURE: have 1 mutation for nr / applicant info and put these there
  const nrNum = state.newRequestModel.nr?.nrNum
  if (nrNum?.includes('NR L')) {
    sessionStorage.setItem('BCREG-NRL', nrNum)
    sessionStorage.setItem('BCREG-nrNum', null)
  } else if (nrNum) {
    sessionStorage.setItem('BCREG-NRL', null)
    sessionStorage.setItem('BCREG-nrNum', nrNum)
  }
}

export const mutateNRData = (state: StateIF, { key, value }) => {
  state.newRequestModel.nrData[key] = value
}

export const mutateXproJurisdiction = (state: StateIF, val: string) => {
  state.newRequestModel.nrData.xproJurisdiction = val
}

export const mutateHomeJurisNum = (state: StateIF, val: string) => {
  state.newRequestModel.nrData.homeJurisNum = val
}

export const mutateNrRequiredModalVisible = (state: StateIF, nrRequiredModalVisible: boolean) => {
  state.newRequestModel.nrRequiredModalVisible = nrRequiredModalVisible
}

export const mutateNumberedCompanyHelpModalVisible = (state: StateIF, numberedCompanyHelpModalVisible: boolean) => {
  state.newRequestModel.numberedCompanyHelpModalVisible = numberedCompanyHelpModalVisible
}

export const mutatePickEntityModalVisible = (state: StateIF, pickEntityModalVisible: boolean) => {
  state.newRequestModel.pickEntityModalVisible = pickEntityModalVisible
}

export const mutatePriorityRequest = (state: StateIF, priorityRequest: boolean) => {
  state.newRequestModel.priorityRequest = priorityRequest
}

export const mutateRequestAction = (state: StateIF, requestCd: NrRequestActionCodes) => {
  state.newRequestModel.conversionType = null
  state.newRequestModel.request_action_cd = requestCd
}

export const mutateRequestExaminationOrProvideConsent = (state: StateIF, { index, type, value }) => {
  state.newRequestModel.requestExaminationOrProvideConsent[index][type] = value
}

export const mutateShowActualInput = (state: StateIF, showActualInput: boolean) => {
  state.newRequestModel.showActualInput = showActualInput
}

export const mutateStats = (state: StateIF, stats: StatsI) => {
  state.newRequestModel.stats = stats
}

export const mutateSubmissionTabComponent = (state: StateIF, component: string) => {
  enum Components {
    EntityNotAutoAnalyzed,
    NamesCapture,
    ApplicantInfo1,
    ApplicantInfo2
  }
  const tab = parseInt(Components[component])
  state.newRequestModel.submissionTabNumber = tab
}

export const mutateSubmissionTabNumber = (state: StateIF, submissionTabNumber: number) => {
  state.newRequestModel.submissionTabNumber = submissionTabNumber
}

export const mutateSubmissionType = (state: StateIF, submissionType: SubmissionTypeT) => {
  state.newRequestModel.submissionType = submissionType
}

export const mutateTabNumber = (state: StateIF, tabNumber: number) => {
  state.newRequestModel.tabNumber = tabNumber
}

export const mutateWaitingAddressSearch = (state: StateIF, appKV: WaitingAddressSearchI) => {
  state.newRequestModel.waitingAddressSearch = appKV
}

export const populateApplicantData = (state: StateIF) => {
  for (const key in state.newRequestModel.nr.applicants) {
    Vue.set(
      state.newRequestModel.applicant,
      key,
      state.newRequestModel.nr.applicants[key]
    )
  }
  // FUTURE: have 1 mutation for nr / applicant info and put these there
  sessionStorage.setItem('BCREG-emailAddress', state.newRequestModel.applicant?.emailAddress)
  // Do not persist phone number in browser storage (sensitive PII).
  sessionStorage.removeItem('BCREG-phoneNumber')
}

export const populateNrData = (state: StateIF) => {
  for (const key in state.newRequestModel.nrData) {
    if (state.newRequestModel.nr[key]) {
      Vue.set(
        state.newRequestModel.nrData,
        key,
        state.newRequestModel.nr[key]
      )
    }
  }
  state.newRequestModel.entity_type_cd = state.newRequestModel.nr.entity_type_cd
}

export const resetEditFormValues = (state: StateIF) => {
  state.newRequestModel.nr = state.newRequestModel.nrOriginal
}

export const resetApplicantDetails = (state: StateIF) => {
  for (const key in state.newRequestModel.applicant) {
    if (key === 'countryTypeCd') {
      state.newRequestModel.applicant[key] = Location.CA
      continue
    }
    state.newRequestModel.applicant[key] = ''
  }
}

export const resetNrData = (state: StateIF) => {
  for (const key in state.newRequestModel.nrData) {
    Vue.set(
      state.newRequestModel.nrData,
      key,
      ''
    )
  }
}

export const resetRequestExaminationOrProvideConsent = (state: StateIF) => {
  for (const n of [0, 1, 2]) {
    for (const type of ['send_to_examiner', 'obtain_consent', 'conflict_self_consent']) {
      state.newRequestModel.requestExaminationOrProvideConsent[n][type] = false
    }
  }
}

export const setErrors = (state: StateIF, errors: string) => {
  if (Array.isArray(state.newRequestModel.errors) && state.newRequestModel.errors.length > 0) {
    state.newRequestModel.errors = state.newRequestModel.errors.concat(errors)
    return
  }
  state.newRequestModel.errors = [errors]
}

export const setNrResponse = (state: StateIF, nr: NameRequestI) => {
  try {
    // set NR data
    mutateNameRequest(state, nr)

    // set Applicants
    const applicants = state.newRequestModel.nr?.applicants || []
    if (applicants instanceof Array) {
      state.newRequestModel.applicant = { ...applicants[0] }
    } else if (applicants) {
      state.newRequestModel.applicant = { ...applicants }
    } else {
      // applicants is null/undefined
    }

    // populate Applicants
    populateApplicantData(state)
  } catch (err) {
    console.error('setNrResponse() =', err) // eslint-disable-line no-console
  }
}

export const updateReservationNames = (state: StateIF, nrNames: [] = []) => {
  nrNames.forEach(({ choice = 1, name = '', designation = '' }) => {
    state.newRequestModel.nameChoices[`name${choice}`] = name
    state.newRequestModel.nameChoices[`designation${choice}`] = designation
  })
}

export const mutateAssumedNameOriginal = (state: StateIF) => {
  state.newRequestModel.assumedNameOriginal = state.newRequestModel.name
}

export const resetNameChoices = (state: StateIF) => {
  for (const key in state.newRequestModel.nameChoices) {
    Vue.set(
      state.newRequestModel.nameChoices,
      key,
      ''
    )
  }
}

export const mutateConditionsModalVisible = (state: StateIF, conditionsModalVisible: boolean) => {
  state.newRequestModel.conditionsModalVisible = conditionsModalVisible
}

export const mutateSocietiesModalVisible = (state: StateIF, societiesModalVisible: boolean) => {
  state.newRequestModel.societiesModalVisible = societiesModalVisible
}

export const mutateExitModalVisible = (state: StateIF, exitModalVisible: boolean) => {
  state.newRequestModel.exitModalVisible = exitModalVisible
}

export const mutateExitIncompletePaymentVisible = (state: StateIF, exitIncompletePaymentVisible: boolean) => {
  state.newRequestModel.exitIncompletePaymentVisible = exitIncompletePaymentVisible
}

export const clearAssumedNameOriginal = (state: StateIF) => {
  state.newRequestModel.assumedNameOriginal = ''
}

export const mutateUserCancelledAnalysis = (state: StateIF, userCancelledAnalysis: boolean) => {
  state.newRequestModel.userCancelledAnalysis = userCancelledAnalysis
}

export const mutateKeycloakRoles = (state: StateIF, keyCloakRoles: Array<string>) => {
  state.common.keycloakRoles = keyCloakRoles
}

export const mutateAuthorizedActions = (state: StateIF, authorizedActions: Array<AuthorizedActions>) => {
  state.common.authorizedActions = authorizedActions
}

export const mutateStaffPayment = (state: StateIF, staffPayment: StaffPaymentIF) => {
  state.staffPayment = staffPayment
}

/** Mutations for Name Check */

export const mutateAnalyzeDesignationPending = (state: StateIF, pending: boolean) => {
  state.nameCheckModel.analyzeDesignationPending = pending
}

export const mutateAnalyzeStructurePending = (state: StateIF, pending: boolean) => {
  state.nameCheckModel.analyzeStructurePending = pending
}

export const mutateAnalyzeConflictsPending = (state: StateIF, pending: boolean) => {
  state.nameCheckModel.analyzeConflictsPending = pending
}

export const mutateConflictsConditional = (state: StateIF, value: Array<string>) => {
  state.nameCheckModel.conflictsConditional = value
}

export const mutateConflictsConditionalInstructions = (state: StateIF, value: Array<ConditionalInstructionI>) => {
  state.nameCheckModel.conflictsConditionalInstructions = value
}

export const mutateConflictsExact = (state: StateIF, value: Array<string>) => {
  state.nameCheckModel.conflictsExact = value
}

export const mutateConflictsRestricted = (state: StateIF, value: Array<string>) => {
  state.nameCheckModel.conflictsRestricted = value
}

export const mutateConflictsSimilar = (state: StateIF, value: Array<string>) => {
  state.nameCheckModel.conflictsSimilar = value
}

export const mutateDesignation = (state: StateIF, value: string) => {
  state.nameCheckModel.designation = value
}

export const mutateDesignationsCheckUse = (state: StateIF, value: Array<string>) => {
  state.nameCheckModel.designationsCheckUse = value
}

export const mutateDesignationsMismatched = (state: StateIF, value: Array<string>) => {
  state.nameCheckModel.designationsMismatched = value
}

export const mutateDesignationsMisplaced = (state: StateIF, value: Array<string>) => {
  state.nameCheckModel.designationsMisplaced = value
}

export const mutateDoNameCheck = (state: StateIF, doNameCheck: boolean) => {
  state.nameCheckModel.doNameCheck = doNameCheck
}

export const mutateFullName = (state: StateIF, value: string) => {
  state.nameCheckModel.fullName = value
}

export const mutateMissingDescriptive = (state: StateIF, value: boolean) => {
  state.nameCheckModel.missingDescriptive = value
}

export const mutateMissingDesignation = (state: StateIF, value: boolean) => {
  state.nameCheckModel.missingDesignation = value
}

export const mutateMissingDistinctive = (state: StateIF, value: boolean) => {
  state.nameCheckModel.missingDistinctive = value
}

export const mutateNameAnalysisTimedOut = (state: StateIF, nameAnalysisTimedOut: boolean) => {
  state.newRequestModel.nameAnalysisTimedOut = nameAnalysisTimedOut
}

export const mutateNumbersCheckUse = (state: StateIF, value: Array<string>) => {
  state.nameCheckModel.numbersCheckUse = value
}

export const mutateQuickSearchNames = (state: StateIF, quickSearchNames: any[]) => {
  state.newRequestModel.quickSearchNames = quickSearchNames
}

export const mutateSpecialCharacters = (state: StateIF, value: Array<string>) => {
  state.nameCheckModel.specialCharacters = value
}

export const mutateNameCheckErrorAdd = (state: StateIF, key: string) => {
  state.nameCheckModel.errors[key] = true
}

export const mutateNameCheckErrorClear = (state: StateIF, key: NameCheckErrorType) => {
  state.nameCheckModel.errors[key] = false
}

export const mutateFolioNumber = (state: StateIF, folioNumber: string) => {
  state.newRequestModel.folioNumber = folioNumber
}

export const mutateRefundParams = (state: StateIF, refundParams: RefundParamsIF) => {
  state.refundParams = refundParams
}

export const mutateWindowWidth = (state: StateIF, width: number) => {
  state.windowWidth = width
}

export const mutateIncorporateNowErrorStatus = (state: StateIF, errorIncorporateNow: boolean) => {
  state.newRequestModel.errorIncorporateNow = errorIncorporateNow
}

export const mutateAmalgamateNowErrorStatus = (state: StateIF, errorAmalgamateNow: boolean) => {
  state.newRequestModel.errorAmalgamateNow = errorAmalgamateNow
}

export const mutateContinuationInErrorStatus = (state: StateIF, errorContinuationIn: boolean) => {
  state.newRequestModel.errorContinuationIn = errorContinuationIn
}

export const mutateSearchBusiness = (state: StateIF, val: BusinessSearchIF) => {
  state.newRequestModel.search.business = val
}

export const mutateSearchCompanyType = (state: StateIF, val: CompanyTypes) => {
  state.newRequestModel.search.companyType = val
}

export const mutateSearchJurisdiction = (state: StateIF, val: any) => {
  state.newRequestModel.search.jurisdiction = val
}

export const mutateSearchRequest = (state: StateIF, val: RequestActionsI) => {
  state.newRequestModel.search.request = val
}

export const mutateBusinessAccountId = (state: StateIF, businessAccountId: string) => {
  state.newRequestModel.businessAccountId = businessAccountId
}
