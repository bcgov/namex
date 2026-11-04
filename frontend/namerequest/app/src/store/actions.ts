import { usePaymentStore } from './payment-store'
import { state } from './state'
import * as Getters from './getters'
import * as Mutations from './mutations'
import axios from 'axios'
import {
  AuthorizedActions,
  CompanyTypes,
  EntityStates,
  EntityTypes,
  Location,
  NameCheckAnalysisJurisdiction,
  NameCheckAnalysisType,
  NameCheckConflictType,
  NameCheckErrorType,
  NrAffiliationErrors,
  NrRequestActionCodes,
  NrState,
  NrType,
  XproNameType
} from '@/enums'
import { BAD_REQUEST, NOT_FOUND, OK, SERVICE_UNAVAILABLE } from 'http-status-codes'
import removeAccents from 'remove-accents'
import { GetFeatureFlag, Sleep, sanitizeName } from '@/plugins'
import { dateToYyyyMmDd } from '@/utils/vancouver-date'
import BusinessServices from '@/services/business-services'
import NamexServices from '@/services/namex-services'
import { DFLT_MIN_LENGTH, DFLT_MAX_LENGTH, MRAS_MIN_LENGTH, MRAS_MAX_LENGTH } from '@/components/new-request/constants'

// List Data
// NB: can't use `this.$xxx` because we don't have `this` (ie, Vue)
import { CanJurisdictions, Designations, checkInvalidDesignation, IntlJurisdictions, RequestActions } from '@/list-data'

import {
  BusinessSearchIF,
  CleanedNameIF,
  ConflictListItemI,
  ConversionTypesI,
  NameRequestI,
  NewRequestNameSearchI,
  ParsedRestrictedResponseIF,
  QuickSearchParamsI,
  QuickSearchParsedRespI,
  RefundParamsIF,
  RequestActionsI,
  RestrictedResponseIF,
  SelectOptionsI,
  StatsI,
  StaffPaymentIF,
  SubmissionTypeT
} from '@/interfaces'

const namexApiUrl = sessionStorage.getItem('NAMEX_API_URL')

export const setActiveComponent = (component: string): void => {
  enum Tabs {
    NewSearch,
    ExistingRequestSearch
  }
  if (typeof Tabs[component] === 'number') {
    Mutations.mutateTabNumber(state, Tabs[component])
    Mutations.mutateDisplayedComponent(state, 'Tabs')
    return
  }

  enum SubmissionTabs {
    EntityNotAutoAnalyzed,
    NamesCapture,
    ApplicantInfo1,
    ApplicantInfo2,
    ApplicantInfo3 = ApplicantInfo2,
    InvalidActionMessage,
    Timeout
  }
  if (typeof SubmissionTabs[component] === 'number') {
    Mutations.mutateSubmissionTabNumber(state, SubmissionTabs[component])
    Mutations.mutateDisplayedComponent(state, 'SubmissionTabs')
    return
  }

  Mutations.mutateDisplayedComponent(state, component)
}

/**
 * Confirms whether the specified action is allowed.
 * @param action the action to confirm
 * @returns True if confirmed, otherwise False
 */
export const confirmAction = async (action: string): Promise<boolean> => {
  try {
    const nrData = await NamexServices.getNameRequest(true)
    if (!nrData) throw new Error('Got error from getNameRequest()')
    Mutations.setNrResponse(state, nrData)
    return Boolean(nrData.actions.includes(action))
  } catch (err) {
    // don't generate errors - getNameRequest() already did that
    return false
  }
}

export const findNameRequest = async (): Promise<void> => {
  try {
    resetAnalyzeName()
    Mutations.mutateDisplayedComponent(state, 'SearchPending')

    const request = await NamexServices.getNameRequest(false)
    if (!request) {
      Mutations.mutateNameRequest(state, {
        text: 'No records were found that match the information you entered.<br>' +
          'Please verify the NR Number and the phone / email and try again.',
        failed: true
      })

      // go back to calling page
      Mutations.mutateDisplayedComponent(state, 'Tabs')

      return
    }
    Mutations.mutateNameRequest(state, request)
    Mutations.mutateDisplayedComponent(state, 'ExistingRequestDisplay')
  } catch (err) {
    const msg = await NamexServices.handleApiError(err, 'Could not find name request')
    console.error('findNameRequest()', msg) // eslint-disable-line no-console
    Mutations.mutateNameRequest(state, {
      text: 'A network error occurred. Please check your network connection and try again.',
      failed: true
    })
    // go back to calling page
    Mutations.mutateDisplayedComponent(state, 'Tabs')
  }
}

/**
 * Stores NR data into app state and displays the ExistingRequestDisplay component.
 * NB: To fetch the NR from the API, use getNameRequest().
 * @param nrData the NR data object
 */
export const loadExistingNameRequest = async (nrData: any): Promise<void> => {
  if (!nrData) {
    Mutations.mutateNameRequest(state, {
      text: 'No records were found that match the information you entered.<br>' +
        'Please verify the NR Number and the phone / email and try again.',
      failed: true
    })
    Mutations.mutateDisplayedComponent(state, 'Tabs')
  } else {
    const { names } = nrData
    Mutations.resetApplicantDetails(state)
    Mutations.setNrResponse(state, nrData)
    Mutations.updateReservationNames(names)
    // FUTURE: instead of "mutating the component", route to "/existing/:id"
    Mutations.mutateDisplayedComponent(state, 'ExistingRequestDisplay')
  }
}

export const setStats = (stats: StatsI): void => {
  Mutations.mutateStats(state, stats)
}

export const userClickedStopAnalysis = (): void => {
  Mutations.mutateUserCancelledAnalysis(state, true)
  Mutations.mutateSubmissionType(state, 'examination')
}

export const resetAnalyzeName = (): void => {
  Mutations.clearAssumedNameOriginal(state)
  if (!Getters.getUserCancelledAnalysis(state)) {
    Mutations.mutateAnalysisJSON(state, null)
  }
  Mutations.mutateEditMode(state, false)
  Mutations.mutateSubmissionType(state, 'normal')
  Mutations.mutateShowActualInput(state, false)
  Mutations.resetApplicantDetails(state)
  Mutations.resetNrData(state)
  Mutations.resetRequestExaminationOrProvideConsent(state)
  Mutations.resetNameChoices(state)
  Mutations.mutateNameRequest(state, {})
  Mutations.mutateNameAnalysisTimedOut(state, false)
  Mutations.mutateAnalyzeDesignationPending(state, false)
  Mutations.mutateAnalyzeStructurePending(state, false)
  Mutations.mutateAnalyzeConflictsPending(state, false)
  Mutations.mutateConflictsConditional(state, [])
  Mutations.mutateConflictsExact(state, [])
  Mutations.mutateConflictsRestricted(state, [])
  Mutations.mutateConflictsSimilar(state, [])
  Mutations.mutateDesignationsCheckUse(state, [])
  Mutations.mutateDesignationsMismatched(state, [])
  Mutations.mutateDesignationsMisplaced(state, [])
  Mutations.mutateMissingDescriptive(state, false)
  Mutations.mutateMissingDesignation(state, false)
  Mutations.mutateMissingDistinctive(state, false)
  Mutations.mutateNameCheckErrorClear(state, NameCheckErrorType.ERROR_DESIGNATION)
  Mutations.mutateNameCheckErrorClear(state, NameCheckErrorType.ERROR_EXACT)
  Mutations.mutateNameCheckErrorClear(state, NameCheckErrorType.ERROR_RESTRICTED)
  Mutations.mutateNameCheckErrorClear(state, NameCheckErrorType.ERROR_SIMILAR)
  Mutations.mutateNameCheckErrorClear(state, NameCheckErrorType.ERROR_STRUCTURE)
  Mutations.mutateNumbersCheckUse(state, [])
  Mutations.mutateSpecialCharacters(state, [])
}

export const cancelAnalyzeName = (destination: string): void => {
  Mutations.mutateAnalyzeDesignationPending(state, false)
  Mutations.mutateAnalyzeStructurePending(state, false)
  Mutations.mutateAnalyzeConflictsPending(state, false)
  if (destination === 'Tabs') {
    Mutations.mutateName(state, Getters.getOriginalName(state))
    Mutations.mutateUserCancelledAnalysis(state, false)
  }
  setActiveComponent(destination)
  if (destination !== 'NamesCapture') {
    resetAnalyzeName()
  }
}

export const cancelEditExistingRequest = (): void => {
  Mutations.mutateDisplayedComponent(state, 'ExistingRequestDisplay')
  Mutations.resetApplicantDetails(state)
  Mutations.mutateNameChoicesToInitialState(state)
  Mutations.resetApplicantDetails(state)
  Mutations.resetNrData(state)
  Mutations.mutateEditMode(state, false)
}

// called to commit data into "newRequestModel" object
export const commitExistingData = (): void => {
  Mutations.populateApplicantData(state)
  Mutations.populateNrData(state)
  if (['clientFirstName', 'clientLastName', 'contact'].some(field => !!Getters.getNr(state).applicants[field])) {
    Mutations.mutateActingOnOwnBehalf(state, false)
  }
  const { entity_type_cd } = Getters.getNr(state)
  if (Getters.getEntityTypesBC(state).some(type => type.value === entity_type_cd)) {
    Mutations.mutateLocation(state, Location.BC)
  } else if (Getters.getNr(state).xproJurisdiction) {
    const { xproJurisdiction } = Getters.getNr(state)
    let location: Location
    for (const key of ['value', 'text']) {
      if (CanJurisdictions.some(j => j[key].toUpperCase() === xproJurisdiction.toUpperCase())) {
        location = Location.CA
        break
      }
      if (IntlJurisdictions.some(j => j[key].toUpperCase() === xproJurisdiction.toUpperCase())) {
        location = Location.IN
        break
      }
    }
    Mutations.mutateLocation(state, location)
  }
  state.newRequestModel.entity_type_cd = entity_type_cd

  if (!Getters.getEntityTypeOptions(state).some(option => option.value === entity_type_cd)) {
    const obj = Getters.getEntityTypesBC(state).find(entity => entity.value === entity_type_cd)
      ? Getters.getEntityTypesBC(state).find(entity => entity.value === entity_type_cd)
      : Getters.getEntityTypesXPRO(state).find(entity => entity.value === entity_type_cd)
    Mutations.mutateEntityTypeAddToSelect(state, obj)
  }
  const { requestTypeCd } = Getters.getNr(state)
  let { request_action_cd } = Getters.getNr(state)
  if (
    [XproNameType.AS, XproNameType.AL, XproNameType.XASO, XproNameType.XCASO, XproNameType.UA]
      .includes(requestTypeCd)
  ) {
    request_action_cd = NrRequestActionCodes.ASSUMED
  }
  Mutations.mutateRequestAction(state, request_action_cd)
  if (request_action_cd !== NrRequestActionCodes.NEW_BUSINESS) {
    const reqObj = RequestActions.find(type => type.value === request_action_cd)
    Mutations.mutateExtendedRequestType(state, reqObj as SelectOptionsI)
  }
  if (Getters.getNr(state).corpNum) {
    Mutations.mutateCorpNum(state, Getters.getNr(state).corpNum)
  }
}

export const editExistingRequest = (): void => {
  Mutations.mutateEditMode(state, true)
  commitExistingData()
  if (Getters.getNrState(state) === NrState.DRAFT) {
    Mutations.mutateSubmissionTabComponent(state, 'NamesCapture')
  } else {
    Mutations.mutateSubmissionTabComponent(state, 'ApplicantInfo1')
  }
  Mutations.mutateDisplayedComponent(state, 'ExistingRequestEdit')
}

export const setApplicantDetails = (appKV: any): void => {
  Mutations.mutateApplicant(state, appKV)
  if (!appKV || !appKV.value || appKV.key !== 'addrLine1') {
    Mutations.mutateAddressSuggestions(state, null)
  }
}

export const setAddressSuggestions = (addressSuggestions: any[]): void => {
  Mutations.mutateAddressSuggestions(state, addressSuggestions)
}

/**
 * Searches Entities or COLIN to fetch a business' info.
 * @param corpNum the business identifier to search for
 * @returns a resolved promise on success or a rejected promise on failure
 */
// FUTURE: not an action - move it to another module?
export async function searchBusiness (corpNum: string): Promise<BusinessSearchIF> {
  try {
    // first try to find business in Entities (Legal API)
    const data = await NamexServices.searchEntities(corpNum)
    // for restoration requests, verify business eligibility
    if (Getters.isRestoration(state) && data.state !== EntityStates.HISTORICAL) {
      // check if business is eligible for restoration by verifying restorationExpiryDate exists and not expired
      if (!data.restorationExpiryDate ||
        dateToYyyyMmDd(Getters.getCurrentJsDate(state)) > data.restorationExpiryDate) {
        throw new Error('This business is not eligible for restoration name request')
      }
    }

    return {
      identifier: data.identifier,
      legalName: data.legalName,
      legalType: data.legalType,
      state: data.state
    }
  } catch (error) {
    if ((error as any).response?.status === NOT_FOUND) {
      // now try to find business in COLIN
      try {
        const data = await NamexServices.searchColin(corpNum)
        return {
          identifier: corpNum,
          legalName: data.legalName,
          legalType: data.legalType,
          state: data.state
        }
      } catch (error) {
        return Promise.reject(error) // network error
      }
    }

    return Promise.reject(error) // network error
  }
}

export const fetchMRASProfile = async (): Promise<any> => {
  if (Getters.getCorpSearch(state)) {
    try {
      const jurisdictionCd = Getters.getJurisdictionCd(state)
      const corpSearch = Getters.getCorpSearch(state)
      const url = `${namexApiUrl}/mras-profile/${jurisdictionCd}/${corpSearch}`
      const response = await NamexServices.axios.get(url)
      if (response?.status === OK) {
        return response.data
      }
      throw new Error(`Status was not 200, response = ${response}`)
    } catch (error) {
      const err = error as any
      const status: number = err?.response?.status
      // do not generate console error for the errors codes
      // that mras-search-info page handles
      if (![BAD_REQUEST, NOT_FOUND, SERVICE_UNAVAILABLE].includes(status)) {
        const msg = await NamexServices.handleApiError(err, 'Could not fetch mras profile')
        console.error('fetchMRASProfile() =', msg) // eslint-disable-line no-console
      }
      Mutations.mutateName(state, '')
      Mutations.mutateMrasSearchResult(state, status)
      Mutations.mutateMrasSearchInfoModalVisible(state, true)
    }
  }
  return null
}

// FUTURE: not an action - move it to another module?
export const getNrStateData = (): any => {
  let nrState = Getters.getNrState(state)
  if (Getters.getAssumedName(state)) nrState = NrState.ASSUMED
  let data: any
  switch (nrState) {
    case NrState.DRAFT:
      data = Getters.getDraftNameReservation(state)
      break
    case NrState.COND_RESERVED:
      data = Getters.getConditionalNameReservation(state)
      break
    case NrState.RESERVED:
      data = Getters.getReservedNameReservation(state)
      break
    case NrState.ASSUMED:
      data = Getters.getEditNameReservation(state)
      break
    case NrState.PENDING_PAYMENT:
      // The user clicked Review and Confirm, which POSTed the draft NR.
      // Then they closed the modal (eg, so they could fix something),
      // and now they clicked Review and Confirm again.
      // Treat this like a new NR, but keep the same state.
      data = Getters.getDraftNameReservation(state)
      data['stateCd'] = NrState.PENDING_PAYMENT
      break
  }

  if (Getters.getShowCorpNum(state) && Getters.getCorpNum(state)) {
    data['corpNum'] = Getters.getCorpNum(state)
  }
  return data
}

// FUTURE: not an action - move it to another module?
export const getNrTypeData = (type: NrType): any => {
  if (Getters.getAssumedName(state)) type = NrType.ASSUMED
  switch (type) {
    case NrType.ASSUMED:
    case NrType.DRAFT:
      return Getters.getDraftNameReservation(state)
    case NrType.CONDITIONAL:
      return Getters.getConditionalNameReservation(state)
    case NrType.RESERVED:
      return Getters.getReservedNameReservation(state)
  }
  return undefined // should never happen
}

/** Submits an edited NR or a new name submission. */
export const submit = async (): Promise<any> => {
  if (Getters.getEditMode(state)) {
    // FUTURE: Refactor the way these async requests are used to provide conditional booleans
    const data = await NamexServices.patchNameRequests(Getters.getNrId(state), Getters.getRequestActionCd(state),
      Getters.getEditNameReservation(state))
    if (data) {
      // FUTURE: change this flow to use the patch response instead of getting the request again
      //         and remove code below
      // FUTURE: cases where applicants can be a list or object -> make this consistent (api) +
      //         update UI accordingly
      // need to set phone/email in case they changed in the patch
      if (data.applicants instanceof Array && data.applicants.length > 0) {
        sessionStorage.setItem('BCREG-emailAddress', data.applicants[0].emailAddress)
        sessionStorage.setItem('BCREG-phoneNumber', data.applicants[0].phoneNumber)
      } else {
        sessionStorage.setItem('BCREG-emailAddress', data.applicants?.emailAddress)
        sessionStorage.setItem('BCREG-phoneNumber', data.applicants?.phoneNumber)
      }
      Mutations.mutateNameRequest(state, data)
      // FUTURE: remove checkin/checkout process (api should handle it whenever a put/patch is attempted)
      const checkin = await NamexServices.checkinNameRequest(Getters.getNrId(state), Getters.getNrState(state))
      if (checkin) {
        // cancel edit mode
        Mutations.mutateEditMode(state, false)

        // show success page briefly
        Mutations.mutateDisplayedComponent(state, 'Success')
        await Sleep(1000)

        // reload NR and show existing NR component
        const nrData = await NamexServices.getNameRequest(true)
        if (nrData) loadExistingNameRequest(nrData)
      }
    }
  } else {
    let request
    if (!Getters.getNrId(state)) {
      const data = getNrTypeData(NrType.DRAFT)
      request = await NamexServices.postNameRequest(Getters.getRequestActionCd(state), data)
      if (request) Mutations.setNrResponse(state, request)
    } else {
      const data = getNrStateData()
      if (
        !Getters.getEditMode(state) && [NrState.COND_RESERVED, NrState.RESERVED].includes(Getters.getNrState(state))
      ) {
        request = await NamexServices.getNameRequest(true)
        if (request?.stateCd === NrState.CANCELLED) {
          setActiveComponent('Timeout')
          return
        }
      }
      request = await NamexServices.putNameReservation(Getters.getNrId(state), Getters.getRequestActionCd(state), data)
      if (request) Mutations.setNrResponse(state, request)
    }
    if (request) usePaymentStore().toggleConfirmNrModal(true)
  }
}

/**
 * Re-submits an expired NR (without changing the current NR data).
 */
export const resubmit = async (): Promise<boolean> => {
  // safety check
  if (Getters.getEditMode(state)) {
    console.error('resubmit() - should not be edit mode') // eslint-disable-line no-console
    return false
  }

  // get current NR data
  const nrData = Getters.getNr(state)

  // safety check
  if (!nrData) {
    console.error('resubmit() - could not get current NR data') // eslint-disable-line no-console
    return false
  }

  // commit the original NR's data
  commitExistingData()

  // build the request data
  const nrTypeData = getNrTypeData(NrType.DRAFT)

  // add resubmit NR number (for internal use only - API ignores it)
  nrTypeData['resubmitNrNum'] = nrData['nrNum']
  // check against entity types if it should have designation or not : if length returns to be 0
  // then NR should not have any designation otherwise work as getNameDesignation
  const checkEntityType = (Designations[nrData['entity_type_cd']].words.length === 0)
  // clean names data
  nrTypeData['names'] = nrData.names.map(name => ({
    choice: name.choice,
    consent_words: '',
    conflict1: '',
    conflict1_num: '',
    designation: !checkEntityType ? getNameDesignation(name) : '',
    name: name.name,
    name_type_cd: name.name_type_cd
  }))

  // clean applicants partyIds
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  for (const [key, value] of Object.entries(nrTypeData['applicants'])) {
    value['partyId'] = ''
  }

  // post new NR
  const request = await NamexServices.postNameRequest(Getters.getRequestActionCd(state), nrTypeData)
  if (request) {
    Mutations.setNrResponse(state, request)
    return true
  }

  return false
}

/**
 * Sometimes name objects have a null designation (because the designation is part of the name).
 * This helper returns the designation, if there is one, or the last word of the name, which is
 * assumed to be the designation.
 */
function getNameDesignation (name: any): string {
  if (name.designation) return name.designation
  const words = name.name.split(' ')
  const len = words.length
  return words[len - 1]
}

export const setCurrentJsDate = (date: Date): void => {
  Mutations.mutateCurrentJsDate(state, date)
}

export const setName = (name: string): void => {
  Mutations.mutateName(state, name)
}

export const setLocation = (location: Location): void => {
  Mutations.mutateLocation(state, location)
}

export const setDisplayedComponent = (component: string): void => {
  Mutations.mutateDisplayedComponent(state, component)
}

export const setTabNumber = (tabNumber: number): void => {
  state.newRequestModel.tabNumber = tabNumber
}

export const setCorpSearch = (corpSearch: string): void => {
  state.newRequestModel.corpSearch = corpSearch
}

export const setEntityTypeCd = (entityTypeCd: EntityTypes): void => {
  state.newRequestModel.entity_type_cd = entityTypeCd
}

export const setOriginEntityTypeCd = (originEntityTypeCd: EntityTypes): void => {
  Mutations.mutateOriginEntityType(state, originEntityTypeCd)
}

export const setConversionType = (conversionType: any): void => {
  Mutations.mutateConversionType(state, conversionType)
}

export const setJurisdictionCd = (jurisdictionCd: string): void => {
  Mutations.mutateJurisdictionCd(state, jurisdictionCd)
}

export const setIsLearBusiness = (isLearBusiness: boolean): void => {
  Mutations.mutateIsLearBusiness(state, isLearBusiness)
}

export const setIsPersonsName = (isPersonsName: boolean): void => {
  Mutations.mutateIsPersonsName(state, isPersonsName)
}

export const setNameIsEnglish = (isEnglishName: boolean): void => {
  Mutations.mutateNameIsEnglish(state, isEnglishName)
}

export const setNoCorpNum = (noCorpNum: boolean): void => {
  Mutations.mutateNoCorpNum(state, noCorpNum)
}

export const setExtendedRequestType = (extendedRequestType: SelectOptionsI): void => {
  Mutations.mutateExtendedRequestType(state, extendedRequestType)
}

export const setRequestAction = (requestAction: NrRequestActionCodes): void => {
  Mutations.mutateRequestAction(state, requestAction)
}

export const setConversionTypeAddToSelect = (conversionType: ConversionTypesI): void => {
  Mutations.mutateConversionTypeAddToSelect(state, conversionType)
}

export const setEntityTypeAddToSelect = (entityType: SelectOptionsI): void => {
  Mutations.mutateEntityTypeAddToSelect(state, entityType)
}

export const setClearErrors = (): void => {
  Mutations.clearErrors(state)
}

export const setUserCancelledAnalysis = (cancelledAnalysis: boolean): void => {
  Mutations.mutateUserCancelledAnalysis(state, cancelledAnalysis)
}

export const setNameRequest = (nameRequest: NameRequestI): void => {
  Mutations.mutateNameRequest(state, nameRequest)
}

export const setExistingRequestSearch = (existingRequest: { key: string, value: string }): void => {
  const prefix = 'BCREG-'
  // if nr changes set session email/phone to whatever is in store (prevents previous values from interfering)
  if (existingRequest.value.includes('NR')) {
    sessionStorage.setItem(prefix + 'emailAddress', Getters.getExistingRequestSearch(state).emailAddress)
    // Do not persist phone data (even masked) in clear text.
    sessionStorage.removeItem(prefix + 'phoneNumber')
  }
  if (existingRequest.value.includes('NR L')) {
    sessionStorage.setItem(prefix + 'nrl', existingRequest.value)
  } else {
    sessionStorage.setItem(prefix + existingRequest.key, existingRequest.value)
  }
  Mutations.mutateExistingRequestSearch(state, existingRequest)
}

export const setNrResponse = (request: NameRequestI): void => {
  Mutations.setNrResponse(state, request)
}

export const setSubmissionTabNumber = (tabNumber: number): void => {
  Mutations.mutateSubmissionTabNumber(state, tabNumber)
}

export const setSubmissionType = (submissionType: SubmissionTypeT): void => {
  Mutations.mutateSubmissionType(state, submissionType)
}

export const setCorpNum = (corpNum: string): void => {
  Mutations.mutateCorpNum(state, corpNum)
}

export const setActingOnOwnBehalf = (isActingOnOwn: boolean): void => {
  Mutations.mutateActingOnOwnBehalf(state, isActingOnOwn)
}

export const setNRData = (nrData: any): void => {
  const { key, value } = nrData
  state.newRequestModel.nrData[key] = value
}

export const setEditMode = (editMode: boolean): void => {
  Mutations.mutateEditMode(state, editMode)
}

export const setAssumedNameOriginal = (): void => {
  Mutations.mutateAssumedNameOriginal(state)
}

export const setNameChoicesToInitialState = (): void => {
  Mutations.mutateNameChoicesToInitialState(state)
}

export const setNameChoices = (choiceObj: any): void => {
  Mutations.mutateNameChoices(state, choiceObj)
}

export const setPriorityRequest = (isPriorityRequest: boolean): void => {
  Mutations.mutatePriorityRequest(state, isPriorityRequest)
}

export const setIsLoadingSubmission = (isLoading: boolean): void => {
  Mutations.mutateIsLoadingSubmission(state, isLoading)
}

export const setShowActualInput = (showInput: boolean): void => {
  Mutations.mutateShowActualInput(state, showInput)
}

//
// Dialog Actions
//
export const setPickEntityModalVisible = (isVisible: boolean): void => {
  Mutations.mutatePickEntityModalVisible(state, isVisible)
}

export const setMrasSearchInfoModalVisible = (isVisible: boolean): void => {
  Mutations.mutateMrasSearchInfoModalVisible(state, isVisible)
}

export const setExitModalVisible = (isVisible: boolean): void => {
  Mutations.mutateExitModalVisible(state, isVisible)
}

export const setExitIncompletePaymentVisible = (isVisible: boolean): void => {
  Mutations.mutateExitIncompletePaymentVisible(state, isVisible)
}

export const setSubmissionTabComponent = (component: string): void => {
  Mutations.mutateSubmissionTabComponent(state, component)
}

export const setConditionsModalVisible = (isVisible: boolean): void => {
  Mutations.mutateConditionsModalVisible(state, isVisible)
}

export const setAffiliationErrorModalValue = (modalValue: NrAffiliationErrors): void => {
  Mutations.mutateAffiliationErrorModalValue(state, modalValue)
}

export const setHelpMeChooseModalVisible = (isVisible: boolean): void => {
  Mutations.mutateHelpMeChooseModalVisible(state, isVisible)
}

export const setNrRequiredModalVisible = (isVisible: boolean): void => {
  Mutations.mutateNrRequiredModalVisible(state, isVisible)
}

export const setNumberedCompanyHelpModalVisible = (isVisible: boolean): void => {
  Mutations.mutateNumberedCompanyHelpModalVisible(state, isVisible)
}

export const setSocietiesModalVisible = (isVisible: boolean): void => {
  Mutations.mutateSocietiesModalVisible(state, isVisible)
}

export const setRequestExaminationOrProvideConsent = (requestExamOrConsent: any): void => {
  Mutations.mutateRequestExaminationOrProvideConsent(state, requestExamOrConsent)
}

export const setKeycloakRoles = (keycloakRoles: string[]): void => {
  Mutations.mutateKeycloakRoles(state, keycloakRoles)
}

export const setAuthorizedActions = (authorizedActions: AuthorizedActions[]): void => {
  Mutations.mutateAuthorizedActions(state, authorizedActions)
}

export const fetchAuthorizedActions = async (): Promise<void> => {
  try {
    const response = await BusinessServices.getAuthorizedActions()
    const authorizedActions = response.data.authorizedPermissions || []
    Mutations.mutateAuthorizedActions(state, authorizedActions)
  } catch (error) {
    // eslint-disable-next-line no-console
    console.error('Error fetching authorized actions:', error)
    Mutations.mutateAuthorizedActions(state, [])
  }
}

export const setStaffPayment = (staffPayment: StaffPaymentIF): void => {
  Mutations.mutateStaffPayment(state, staffPayment)
}

export const setFolioNumber = (folioNumber: string): void => {
  Mutations.mutateFolioNumber(state, folioNumber)
}

export const setWindowWidth = (width: number): void => {
  Mutations.mutateWindowWidth(state, width)
}

/**
 * Name Check actions
 * FUTURE: move these into a factory if converting to composition api
 */
export const getMatchesExact = async (token: string, cleanedName: string): Promise<Array<ConflictListItemI>> => {
  const exactResp = await NamexServices.axios.get(
    `${namexApiUrl}/exact-match?query=` + cleanedName,
    { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } }
  ).catch(() => {
    Mutations.mutateNameCheckErrorAdd(state, NameCheckErrorType.ERROR_EXACT)
    return null
  })
  return exactResp?.data ? parseExactNames(exactResp.data) : []
}

// todo: look into differences #31690
export const getMatchesSimilar_main_branch = async (
  token: string, cleanedName: string, exactNames: Array<ConflictListItemI>
): Promise<Array<ConflictListItemI>> => {
  const synonymResp = await NamexServices.axios.get(
    `${namexApiUrl}/requests/synonymbucket/` + cleanedName + '/*',
    { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } }
  ).catch(() => {
    Mutations.mutateNameCheckErrorAdd(state, NameCheckErrorType.ERROR_SIMILAR)
    return null
  })
  if (synonymResp?.data) synonymResp.data.exactNames = exactNames || []
  return synonymResp?.data ? parseSynonymNames(synonymResp.data) : []
}

const getMatchesSimilar = async (
  token: string,
  cleanedName: string
): Promise<{ names: Array<any>, exactNames: Array<any> }> => {
  const synonymResp = await NamexServices.axios.get(
    `${namexApiUrl}/requests/possible-conflicts/${cleanedName}`,
    {
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }
    }).catch(() => {
    Mutations.mutateNameCheckErrorAdd(state, NameCheckErrorType.ERROR_SIMILAR)
    return null
  })

  return {
    names: synonymResp.data.names || [],
    exactNames: synonymResp.data.exactNames || []
  }
}

export const getMatchesRestricted = async (
  token: string, cleanedName: string
): Promise<ParsedRestrictedResponseIF> => {
  const restrictedResp = await NamexServices.axios.get(
    `${namexApiUrl}/documents/restricted-words?content=${cleanedName}`,
    { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } }
  ).catch(() => {
    Mutations.mutateNameCheckErrorAdd(state, NameCheckErrorType.ERROR_RESTRICTED)
    return null
  })
  return restrictedResp?.data
    ? parseRestrictedWords(restrictedResp.data)
    : { conditionalInstructions: [], conditionalWords: [], restrictedWords: [] }
}

export const getNameAnalysis = async (options: { xpro: boolean, designationOnly: boolean }) => {
  const name = Getters.getFullName(state)
  try {
    if (options.designationOnly) Mutations.mutateAnalyzeDesignationPending(state, true)
    else Mutations.mutateAnalyzeStructurePending(state, true)
    Mutations.resetRequestExaminationOrProvideConsent(state)
    const params: NewRequestNameSearchI = {
      name: name,
      location: Getters.getLocation(state),
      entity_type_cd: Getters.getEntityTypeCd(state),
      request_action_cd: Getters.getRequestActionCd(state),
      jurisdiction: options.xpro ? NameCheckAnalysisJurisdiction.XPRO : NameCheckAnalysisJurisdiction.BC,
      analysis_type: options.designationOnly ? NameCheckAnalysisType.DESIGNATION : NameCheckAnalysisType.STRUCTURE
    }
    const analysis = await NamexServices.nameAnalysis(params)
    // verify the user did not start a new search on a different name
    if (name === Getters.getFullName(state)) {
      const json = analysis
      Mutations.mutateAnalysisJSON(state, json)
      if (Array.isArray(json.issues) && json.issues.length > 0) {
        for (let i = 0; i < json.issues.length; i++) {
          switch (json.issues[i].issue_type) {
            case 'add_descriptive':
              Mutations.mutateMissingDescriptive(state, true)
              continue
            case 'add_distinctive':
              Mutations.mutateMissingDistinctive(state, true)
              continue
            case 'designation_non_existent':
              Mutations.mutateMissingDesignation(state, true)
              continue
            case 'designation_mismatch':
              if (Array.isArray(json.issues[i].name_actions) && json.issues[i].name_actions.length > 0) {
                let items = json.issues[i].name_actions.map(item => { return item.word })
                items = [...new Set(items)]
                Mutations.mutateDesignationsMismatched(state, items)
              }
              continue
            case 'designation_misplaced':
              if (Array.isArray(json.issues[i].name_actions) && json.issues[i].name_actions.length > 0) {
                let items = json.issues[i].name_actions.map(item => { return item.word })
                items = [...new Set(items)]
                Mutations.mutateDesignationsMisplaced(state, items)
              }
              continue
            case 'end_designation_more_than_once':
              if (Array.isArray(json.issues[i].name_actions) && json.issues[i].name_actions.length > 0) {
                let items = json.issues[i].name_actions.map(item => { return item.word })
                items = [...new Set(items)]
                Mutations.mutateDesignationsMisplaced(state, items)
              }
              continue
            case 'incorrect_year':
              if (Array.isArray(json.issues[i].name_actions) && json.issues[i].name_actions.length > 0) {
                let items = json.issues[i].name_actions.map(item => { return item.word })
                items = [...new Set(items)]
                Mutations.mutateNumbersCheckUse(state, items)
              }
              continue
            default:
              if (Array.isArray(json.issues[i].name_actions) && json.issues[i].name_actions.length > 0) {
                let items = json.issues[i].name_actions.map(item => { return item.word })
                items = [...new Set(items)]
                Mutations.mutateDesignationsCheckUse(state, items)
              }
          }
        }
      }
      if (options.designationOnly) Mutations.mutateAnalyzeDesignationPending(state, false)
      else Mutations.mutateAnalyzeStructurePending(state, false)
    }
  } catch (err) {
    // verify the user did not start a new search on a different name
    if (name === Getters.getFullName(state)) {
      const msg = await NamexServices.handleApiError(err, 'Could not get name analysis')
      console.error('getNameAnalysis() =', msg) // eslint-disable-line no-console
      if (options.designationOnly) {
        Mutations.mutateNameCheckErrorAdd(state, NameCheckErrorType.ERROR_DESIGNATION)
        Mutations.mutateAnalyzeDesignationPending(state, false)
      } else {
        Mutations.mutateNameCheckErrorAdd(state, NameCheckErrorType.ERROR_STRUCTURE)
        Mutations.mutateAnalyzeStructurePending(state, false)
      }
    }
  }
}

export const getQuickSearch = async (
  cleanedName: CleanedNameIF, checks: QuickSearchParamsI
): Promise<QuickSearchParsedRespI> => {
  try {
    const quickSearchPublicId = window['quickSearchPublicId']
    const quickSearchPublicSecret = window['quickSearchPublicSecret']

    // throw error if no quickSearchPublicId or quickSearchPublicSecret
    if (!quickSearchPublicId || !quickSearchPublicSecret) {
      throw new Error('quickSearchPublicId/quickSearchPublicSecret not set in config')
    }
    const encodedAuth = btoa(`${quickSearchPublicId}:${quickSearchPublicSecret}`)

    const tokenResp = await axios.post(window['authTokenUrl'], 'grant_type=client_credentials', {
      headers: { Authorization: `Basic ${encodedAuth}`, 'content-type': 'application/x-www-form-urlencoded' }
    })
    const token = tokenResp.data.access_token
    const { names, exactNames } = (
      checks.similar
        ? await getMatchesSimilar(token, cleanedName.synonymMatch)
        : { names: [], exactNames: [] }
    )

    const parsedRestrictedResp: ParsedRestrictedResponseIF = (
      checks.restricted
        ? await getMatchesRestricted(token, cleanedName.restrictedMatch)
        : { restrictedWords: [], conditionalWords: [], conditionalInstructions: [] }
    )

    return {
      exactNames: exactNames,
      synonymNames: names,
      restrictedWords: parsedRestrictedResp.restrictedWords,
      conditionalWords: parsedRestrictedResp.conditionalWords,
      conditionalInstructions: parsedRestrictedResp.conditionalInstructions
    }
  } catch (err) {
    const msg = await NamexServices.handleApiError(err, 'Could not get quick search')
    // send error and move on to detailed search
    // (do not show error to user)
    console.error('getQuickSearch() =', msg) // eslint-disable-line no-console
    // add errors to name check for all quick search checks
    if (checks.exact) Mutations.mutateNameCheckErrorAdd(state, NameCheckErrorType.ERROR_EXACT)
    if (checks.similar) Mutations.mutateNameCheckErrorAdd(state, NameCheckErrorType.ERROR_SIMILAR)
    if (checks.restricted) Mutations.mutateNameCheckErrorAdd(state, NameCheckErrorType.ERROR_RESTRICTED)

    return {
      exactNames: [],
      synonymNames: [],
      restrictedWords: [],
      conditionalWords: [],
      conditionalInstructions: []
    }
  }
}

export const nameCheckClearError = (key: NameCheckErrorType): void => {
  Mutations.mutateNameCheckErrorClear(state, key)
}

export const parseExactNames = (json: { names: [string] }): Array<ConflictListItemI> => {
  const nameObjs = json?.names || []
  const names = []
  for (let i = 0; i < nameObjs.length; i++) {
    names.push({ name: `${nameObjs[i]['name']}`, type: NameCheckConflictType.EXACT })
  }
  return names
}

export const parseRestrictedWords = (resp: RestrictedResponseIF): ParsedRestrictedResponseIF => {
  const phrases = resp.restricted_words_conditions
  const parsedResp: ParsedRestrictedResponseIF = {
    conditionalInstructions: [],
    conditionalWords: [],
    restrictedWords: []
  }
  // restrictedWords: add any word with cnd_info[..].allow_use = N
  // conditionalWords: all other words in the list
  for (let i = 0; i < phrases.length; i++) {
    const phrase = phrases[i].word_info.phrase.toUpperCase()

    // rules for ignoring restricted/conditional phrases
    const entityCd = Getters.getEntityTypeCd(state)
    if (entityCd === EntityTypes.CR && Designations[EntityTypes.CC].words.includes(phrase)) continue
    if (Designations[entityCd].words.includes(phrase)) continue

    // split into restricted vs conditional
    let restricted = false
    // there can be multiple conditions per word / phrase
    for (const k in phrases[i].cnd_info) {
      if (phrases[i].cnd_info[k].allow_use === 'N') {
        restricted = true
        break
      }
    }

    // add restricted and conditional info to the response
    if (restricted) parsedResp.restrictedWords.push(phrase)
    else {
      parsedResp.conditionalWords.push(phrase)
      for (const k in phrases[i].cnd_info) {
        let info = phrases[i].cnd_info[k].text ? phrases[i].cnd_info[k].text?.trim() : ''
        if (info && !info.endsWith('.')) info = info + '.'
        const instructions = phrases[i].cnd_info[k].instructions
          ? `${info} ${phrases[i].cnd_info[k].instructions}`
          : info
        parsedResp.conditionalInstructions.push({
          word: phrase,
          instructions: instructions || 'This word needs to be reviewed by staff.'
        })
      }
    }
  }
  return parsedResp
}

// todo: verify is used #31690
export const parseSynonymNames = (
  json: { names: Array<string>, exactNames: Array<ConflictListItemI> }
): Array<ConflictListItemI> => {
  const duplicateNames = []
  for (let i = 0; i < json.exactNames.length; i++) {
    duplicateNames.push(json.exactNames[i].name)
  }
  const nameObjs = json.names
  const names = []
  for (let i = 0; i < nameObjs.length; i++) {
    if (nameObjs[i]['name_info']['id']) {
      const name = nameObjs[i]['name_info']['name']
      if (!duplicateNames.includes(name)) {
        names.push({ name: name, type: NameCheckConflictType.SIMILAR })
      }
    }
  }
  return names
}

export const setDesignation = (designation: string): void => {
  Mutations.mutateDesignation(state, designation)
}

export const setDoNameCheck = (check: boolean): void => {
  Mutations.mutateDoNameCheck(state, check)
}

export const startEditName = () => {
  if (!Getters.getEntityTypeCd(state)) Mutations.setErrors(state, 'entity_type_cd')
}

export const startAnalyzeName = async () => {
  resetAnalyzeName()
  setUserCancelledAnalysis(false)

  // check basic state values
  if (!Getters.getRequestActionCd(state)) Mutations.setErrors(state, 'request_action_cd')
  if (!Getters.getLocation(state)) Mutations.setErrors(state, 'location')
  if (!Getters.getEntityTypeCd(state)) Mutations.setErrors(state, 'entity_type_cd')

  // check if designation selection is required and present
  if (!Getters.isXproFlow(state) && Designations[Getters.getEntityTypeCd(state)]?.end) {
    if (!Getters.getDesignation(state)) Mutations.setErrors(state, 'designation')
  }

  // Check for designations should not be in the name
  if (checkInvalidDesignation(Getters.getEntityTypeCd(state), Getters.getName(state))) {
    Mutations.setErrors(state, 'invalid_designation_in_name')
  }

  // check if jurisdiction selection is required and present
  if (
    [Location.CA, Location.IN].includes(Getters.getLocation(state)) &&
    ![NrRequestActionCodes.MOVE].includes(Getters.getRequestActionCd(state)) &&
    !Getters.getJurisdictionCd(state)
  ) {
    Mutations.setErrors(state, 'jurisdiction')
    return
  }

  if (!Getters.getCorpSearch(state)) {
    if (!Getters.getName(state)) {
      Mutations.setErrors(state, 'name')
      return
    }

    const min = Getters.isXproFlow(state) ? MRAS_MIN_LENGTH : DFLT_MIN_LENGTH
    const max = Getters.isXproFlow(state) ? MRAS_MAX_LENGTH : DFLT_MAX_LENGTH

    if (Getters.getName(state).length < min) {
      Mutations.setErrors(state, 'min_length')
      return
    }
    if (Getters.getName(state).length > max) {
      Mutations.setErrors(state, 'max_length')
      return
    }
  }

  if (Getters.getErrors(state).length > 0) {
    return
  }

  // prep name for analysis
  let name = removeAccents(Getters.getName(state))
  name = name.toUpperCase()

  // auto fix LTD/INC/CORP designations without a period unless xpro
  if (!Getters.isXproFlow(state)) {
    name = name.replace(/^LTD$/g, 'LTD.')
      .replace(/^LTD\s/g, 'LTD. ')
      .replace(/\sLTD\s/g, ' LTD. ')
      .replace(/\sLTD$/g, ' LTD.')
      .replace(/^INC$/g, 'INC.')
      .replace(/^INC\s/g, 'INC. ')
      .replace(/\sINC\s/g, ' INC. ')
      .replace(/\sINC$/g, ' INC.')
      .replace(/^CORP$/g, 'CORP.')
      .replace(/^CORP\s/g, 'CORP. ')
      .replace(/\sCORP\s/g, ' CORP. ')
      .replace(/\sCORP$/g, ' CORP.')
  }
  Mutations.mutateName(state, name)
  const designation = Getters.getDesignation(state)
  Mutations.mutateFullName(state, `${name} ${designation}`)
  Mutations.mutateNameOriginal(state, name) // Set original name for reset baseline

  // xpro get name call
  if (Getters.isXproFlow(state)) {
    Mutations.mutateXproJurisdiction(state, Getters.getJurisdictionText(state))
    // set home juris num only if we have a corp num
    // (don't set if we entered a corp name instead)
    if (!Getters.getHasNoCorpNum(state)) {
      Mutations.mutateHomeJurisNum(state, Getters.getCorpSearch(state))
    }
    // only make MRAS call for MRAS jurisdictions and if we have a corp num
    if (Getters.isMrasJurisdiction(state) && !Getters.getHasNoCorpNum(state)) {
      const profile = await fetchMRASProfile()
      if (profile) {
        const hasMultipleNames = profile?.LegalEntity?.names && profile?.LegalEntity?.names.constructor === Array
        name = hasMultipleNames
          ? sanitizeName(profile?.LegalEntity?.names[0]?.legalName)
          : sanitizeName(profile?.LegalEntity?.names?.legalName)
        Mutations.mutateName(state, name)
      } else {
        Mutations.mutateNoCorpNum(state, true)
        return
      }
    }
  }

  // name check
  if (Getters.getDoNameCheck(state)) {
    Mutations.mutateAnalyzeDesignationPending(state, true)
    Mutations.mutateAnalyzeStructurePending(state, true)
    Mutations.mutateAnalyzeConflictsPending(state, true)
    Mutations.mutateDisplayedComponent(state, 'NameCheck')
    // similar name check / conditional + restricted word check
    startQuickSearch({ exact: true, similar: true, restricted: true })
    // we don't do a structure name check for xpro names
    if (Getters.isXproFlow(state)) {
      Mutations.mutateAnalyzeDesignationPending(state, false)
      Mutations.mutateAnalyzeStructurePending(state, false)
    } else {
      // designation check
      getNameAnalysis({ xpro: false, designationOnly: true })
      // descriptive/distinctive check - if disabled in LD then ignore
      if (GetFeatureFlag('disable-analysis')) {
        Mutations.mutateAnalyzeStructurePending(state, false)
      } else {
        getNameAnalysis({ xpro: false, designationOnly: false })
      }
      // special chars
      const specialChars = name.match(/[~`$%_{}|\\<>]/g)
      if (specialChars) Mutations.mutateSpecialCharacters(state, specialChars)
      else Mutations.mutateSpecialCharacters(state, [])
      // extra designation rules that aren't in the backend for coops/cccs
      const entity_type_cd = Getters.getEntityTypeCd(state)
      if ([EntityTypes.CP, EntityTypes.XCP, EntityTypes.CC].includes(entity_type_cd)) {
        let entityPhraseChoices = []
        const basePhrases = Designations[entity_type_cd].words
        // These are the inner phrases for the CCC and CP types. Filtering out CR designations from CPs
        // has no effect and CCC designations are a mix of CR-type ending designations and CCC specific
        // inner phrases so filter out // the CR designations for the purposes of this getter.
        entityPhraseChoices = basePhrases.filter(phrase => !Designations[EntityTypes.CR].words.includes(phrase))
        if (entityPhraseChoices.some(phrase => name.startsWith(phrase))) {
          const phrase = name.split(' ')[0].replace('COMMUNITY', 'COMMUNITY CONTRIBUTION COMPANY')
          Mutations.mutateDesignationsCheckUse(state, [phrase])
        } else if (entityPhraseChoices.every(phrase => {
          phrase = phrase.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&')
          return (name.search(new RegExp('(\\s)' + phrase + '(\\s|$)')) === -1)
        })) {
          Mutations.mutateMissingDesignation(state, true)
        }
      }
    }
  } else {
    // skip name check
    Mutations.mutateAnalyzeDesignationPending(state, false)
    Mutations.mutateAnalyzeStructurePending(state, false)
    Mutations.mutateAnalyzeConflictsPending(state, false)
    setActiveComponent('NamesCapture')
  }
}

export const startQuickSearch = async (checks: QuickSearchParamsI) => {
  Mutations.mutateAnalyzeConflictsPending(state, true)
  if (Getters.getFullName(state)) {
    const name = Getters.getFullName(state)
    // eslint-disable-next-line no-useless-escape
    let exactMatchName = name.replace(' \/', '\/')
      .replace(/(^|\s+)(\$+(\s|$)+)+/g, '$1DOLLAR$3')
      .replace(/(^|\s+)(¢+(\s|$)+)+/g, '$1CENT$3')
      .replace(/\$/g, 'S')
      .replace(/¢/g, 'C')
      .replace(/\\/g, '')
      .replace(/\//g, '')
      .replace(/(`|~|!|\||\(|\)|\[|\]|\{|\}|:|"|\^|#|%|\?)/g, '')
      // eslint-disable-next-line no-useless-escape
      .replace(/[\+\-]{2,}/g, '')
      // eslint-disable-next-line no-useless-escape
      .replace(/\s[\+\-]$/, '')
    exactMatchName = exactMatchName.substring(0, 1) === '+' ? exactMatchName.substring(1) : exactMatchName
    exactMatchName = encodeURIComponent(exactMatchName)

    const synonymsName = name.replace(/\//g, ' ')
      .replace(/\\/g, ' ')
      .replace(/&/g, ' ')
      .replace(/\+/g, ' ')
      // eslint-disable-next-line no-useless-escape
      .replace(/\-/g, ' ')
      .replace(/(^| )(\$+(\s|$)+)+/g, '$1DOLLAR$3')
      .replace(/(^| )(¢+(\s|$)+)+/g, '$1CENT$3')
      .replace(/\$/g, 'S')
      .replace(/¢/g, 'C')
      .replace(/(`|~|!|\||\(|\)|\[|\]|\{|\}|:|"|\^|#|%|\?|,|\*|)/g, '')

    const cleanedName = {
      'exactMatch': exactMatchName,
      'synonymMatch': synonymsName,
      'restrictedMatch': Getters.getName(state)
    }
    const resp = await getQuickSearch(cleanedName, checks)
    // make sure a new search on a different name has not started
    if (Getters.getFullName(state) === name) {
      if (checks.exact) Mutations.mutateConflictsExact(state, resp.exactNames as unknown as string[])
      if (checks.similar) Mutations.mutateConflictsSimilar(state, resp.synonymNames as unknown as string[])
      if (checks.restricted) {
        Mutations.mutateConflictsRestricted(state, resp.restrictedWords)
        Mutations.mutateConflictsConditional(state, resp.conditionalWords)
        Mutations.mutateConflictsConditionalInstructions(state, resp.conditionalInstructions)
      }

      Mutations.mutateAnalyzeConflictsPending(state, false)
    }
  }
}

export const setRefundParams = (refundParams: RefundParamsIF): void => {
  Mutations.mutateRefundParams(state, refundParams)
}

export const setIncorporateNowErrorStatus = (errorIncorporateNow: boolean): void => {
  Mutations.mutateIncorporateNowErrorStatus(state, errorIncorporateNow)
}

export const setAmalgamateNowErrorStatus = (errorAmalgamateNow: boolean): void => {
  Mutations.mutateAmalgamateNowErrorStatus(state, errorAmalgamateNow)
}

export const setContinuationInErrorStatus = (errorContinuationIn: boolean): void => {
  Mutations.mutateContinuationInErrorStatus(state, errorContinuationIn)
}

export const setSearchBusiness = (val: BusinessSearchIF): void => {
  Mutations.mutateSearchBusiness(state, val)
}

export const setSearchCompanyType = (val: CompanyTypes): void => {
  Mutations.mutateSearchCompanyType(state, val)
}

export const setSearchJurisdiction = (val: any): void => {
  Mutations.mutateSearchJurisdiction(state, val)
}

export const setSearchRequest = (val: RequestActionsI): void => {
  Mutations.mutateSearchRequest(state, val)
}

export const setBusinessAccountid = (val: any): void => {
  Mutations.mutateBusinessAccountId(state, val)
}
