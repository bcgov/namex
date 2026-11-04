import { Status } from '~/enums/nr-status'
import {
  type Trademark,
  type Comment,
  type Condition,
  type Histories,
  type Macro,
  type TrademarksObject,
  type NameChoice,
  type RequestType,
  type RequestTypeRule,
  type Jurisdiction,
  type NameRequest,
  type HistoryEntry,
  type ConditionsList,
} from '~/types'

import requestTypes from '~/data/request_types.json'
import requestTypeRulesJSON from '~/data/request_type_rules.json'
import jurisdictionsData from '~/data/jurisdictions.json'
import { ConsentFlag, RequestTypeCode } from '~/enums/codes'
import {
  getDecisionReasons,
  getNameRequest,
  getNextNrNumber,
  patchNameRequest,
  postConditions,
  postHistories,
  postNewComment,
  postTrademarks,
  putNameChoice,
  putNameRequest,
} from '~/util/namex-api'
import { getEmptyNameChoice, isValidNrFormat, sortNameChoices } from '~/util'
import { DateTime } from 'luxon'
import { fromMappedRequestType, toMappedRequestType } from '~/util/request-type'
import { getDateFromDateTime, getVancouverDate, parseDate } from '~/util/date'
import { useConflicts } from './conflicts'
import { usePayments } from './payments'
import { useExaminationOptions } from './options'
import { Route } from '~/enums/routes'
import { emitter } from '~/util/emitter'

export const useExamination = defineStore('examine', () => {
  const conflicts = useConflicts()
  const payments = usePayments()

  /** Username of the current user */
  const userId = ref(useNuxtApp().$userProfile.username)
  const userRoles = ref(useNuxtApp().$auth.realmAccess?.roles ?? [])

  const priority = ref<boolean>(false)
  const isComplete = computed(() =>
    [
      Status.Approved,
      Status.Rejected,
      Status.Conditional,
      Status.Consumed,
      Status.Completed,
      Status.Cancelled,
      Status.Historical,
      Status.Expired,
    ].includes(nrStatus.value)
  )
  const examiner = ref<string>()
  const isCurrentExaminer = computed(() => examiner.value === userId.value)

  const conflictSelectionDisabled = computed(
    () =>
      (customerMessageOverride.value != null &&
        customerMessageOverride.value != '') ||
      !isCurrentExaminer.value ||
      !isMakingDecision.value
  )
  const autoAddDisabled = computed(
    () =>
      conflictSelectionDisabled.value
  )

  const comments = ref<Array<Comment>>([])

  const macros = ref<Array<Macro>>([])

  const trademarks = ref<Array<Trademark>>([])

  const isEditing = ref<boolean>()
  const isMakingDecision = computed(() => nrStatus.value === Status.InProgress)
  const isHeaderShown = ref<boolean>()
  const nrNumber = ref<string>('')
  const nrStatus = ref(Status.Draft)
  const isClosed = computed(() =>
    [
      Status.Rejected,
      Status.Approved,
      Status.Conditional,
      Status.Consumed,
    ].includes(nrStatus.value)
  )
  const previousState = ref<Status>()
  const listRequestTypes = ref<Array<RequestType>>(
    requestTypes as Array<RequestType>
  )
  const requestType = ref<RequestTypeCode>(listRequestTypes.value[0].value)
  const requestTypeObject = computed(
    () => findRequestTypeObject(requestType.value)!
  )
  const requestTypeRules = ref<Array<RequestTypeRule>>(
    requestTypeRulesJSON as Array<RequestTypeRule>
  )

  const requestActionCd = computed(
    () => requestTypeObject.value.request_action_cd
  )
  const entityTypeCd = computed(() => requestTypeObject.value.entity_type_cd)

  const conditions = ref<Array<Condition>>([])

  const histories = ref<Array<HistoryEntry>>([])

  const consentRequired = ref<boolean>()

  const selectedConditions = ref<Array<Condition>>([])

  const customerMessageOverride = ref<string>()

  const decisionSelectionsDisabled = computed(
    () => customerMessageOverride.value != null
  )

  const selectedMacros = ref<Array<Macro>>([])

  const selectedTrademarks = ref<Array<Trademark>>([])

  const conditionMessages = computed(() =>
    selectedConditions.value.map((condition) =>
      condition.phrase !== undefined && condition.phrase !== ''
        ? `${condition.phrase} - ${condition.instructions}`
        : condition.instructions
    )
  )

  const conflictMessages = computed(() => {
    if (conflicts.selectedConflicts.length === 0 && consentRequired.value) {
      return ['Consent Required \n']
    } else {
      return conflicts.selectedConflicts.map((conflict) =>
        consentRequired.value
          ? `Consent required from ${conflict.text}`
          : `Rejected due to conflict with ${conflict.text}`
      )
    }
  })

  const trademarkMessages = computed(() =>
    selectedTrademarks.value.map(
      (trademark) =>
        `Registered Trademark: ${trademark.name} - Application #${trademark.application_number}`
    )
  )

  const macroMessages = computed(() =>
    selectedMacros.value.map((macro) => macro.reason)
  )

  const requestorMessageStrings = computed(() =>
    conflictMessages.value.concat(
      conditionMessages.value,
      trademarkMessages.value,
      macroMessages.value
    )
  )

  const requestorMessage = computed(() => {
    if (customerMessageOverride.value) {
      return customerMessageOverride.value
    } else {
      return requestorMessageStrings.value.join('\n\n')
    }
  })

  const compName1 = reactive<NameChoice>(getEmptyNameChoice(1))
  const compName2 = reactive<NameChoice>(getEmptyNameChoice(2))
  const compName3 = reactive<NameChoice>(getEmptyNameChoice(3))
  const nameChoices = computed(() => [compName1, compName2, compName3])

  const currentNameObj = ref<NameChoice>()
  const currentName = computed(() => currentNameObj.value?.name || null)
  const currentChoice = computed(() => currentNameObj.value?.choice)

  const userHasApproverRole = computed(() =>
    userRoles.value.includes('names_approver')
  )
  const userHasEditRole = computed(
    () => userHasApproverRole.value || userRoles.value.includes('names_editor')
  )
  const isMyCurrentNr = computed(
    () => nrStatus.value === Status.InProgress && isCurrentExaminer.value
  )
  const furnished = ref<'Y' | 'N'>('N')

  const listJurisdictions = ref<Array<Jurisdiction>>(jurisdictionsData)
  const jurisdiction = ref<string>()
  const jurisdictionNumber = ref<string>()
  const jurisdictionRequired = ref<boolean>()

  const previousNr = ref<string>()
  const prevNrRequired = ref<boolean>()

  const consumedBy = computed(
    () =>
      nameChoices.value
        .filter((choice) => choice.consumptionDate && choice.corpNum)
        .at(0)?.corpNum
  )
  const consentDate = ref<string>()
  const consentFlag = ref<ConsentFlag>()

  const submittedDate = ref<DateTime>()
  const corpNum = ref<string>()
  const corpNumRequired = ref<boolean>()
  const expiryDate = ref<string>()

  const additionalInfo = ref<string>()
  const additional_info_template = ref<string>()
  const natureOfBusiness = ref<string>()

  const clientFirstName = ref<string>()
  const clientLastName = ref<string>()
  const firstName = ref<string>()
  const middleName = ref<string>()
  const lastName = ref<string>()
  const addressLine1 = ref<string>()
  const addressLine2 = ref<string>()
  const addressLine3 = ref<string>()
  const city = ref<string>()
  const province = ref<string>()
  const postalCode = ref<string>()
  const country = ref<string>()
  const phone = ref<string>()
  const fax = ref<string>()
  const conEmail = ref<string>()
  const contactName = ref<string>()

  const hasBeenReset = ref<boolean>()

  const initializing = ref(false)

  const additionalInfoTransformedTemplate = computed(() => {
    return additional_info_template.value
      ?.split('||')
      .map((template) =>
        template
          .replaceAll('<corp_num>', corpNum.value || '')
          .replaceAll('<prev_nr>', previousNr.value || '')
      )
      .join(' ')
  })

  const canEdit = computed(() => {
    if (consumptionDate.value) return false
    if (isMyCurrentNr.value) return true
    return (
      userHasEditRole.value &&
      [
        Status.Draft,
        Status.Hold,
        Status.Rejected,
        Status.Approved,
        Status.Conditional,
      ].includes(nrStatus.value)
    )
  })

  const otherExaminerInProgress = computed(
    () => !isCurrentExaminer.value && nrStatus.value === Status.InProgress
  )

  const expired = computed(
    () =>
      expiryDate.value &&
      DateTime.fromISO(expiryDate.value).endOf('day') < DateTime.now()
  )

  const isApprovedAndExpired = computed(
    // NR will move to 'EXPIRED' state once expiry date is reached for 'APPROVED', 'CONDITIONAL' state.
    // If currentState is 'EXPIRED', then it was approved and expired.
    () => expiryDate.value && nrStatus.value === Status.Expired
  )

  const canCancel = computed(
    () =>
      userHasEditRole.value &&
      !otherExaminerInProgress.value &&
      !expired.value &&
      !isMakingDecision.value &&
      nrStatus.value !== Status.Cancelled &&
      !isApprovedAndExpired.value
  )

  /** Can the current user claim the current name request for examination? */
  const canClaim = computed(
    () =>
      userHasApproverRole.value &&
      [Status.Draft, Status.Hold].includes(nrStatus.value)
  )

  const consumptionDate = computed(() =>
    nameChoices.value
      .map((d) => d.consumptionDate)
      .filter((d) => d != null)
      .at(0)
  )

  /** Status of an exact matches in history for alerting about previous submissions */
  const exactHistoryMatch = computed<Status | undefined>(() => {
    if (!histories.value) return

    let exactMatches = histories.value.filter(
      (entry) => currentName.value?.toUpperCase() === entry.name.toUpperCase()
    )

    for (const match of exactMatches) {
      if (
        match.name_state_type_cd === 'R' ||
        match.name_state_type_cd === 'REJECTED' ||
        match.submit_count > 3
      ) {
        return Status.Rejected
      }
    }

    if (exactMatches.length > 0) {
      return Status.Approved
    }
  })

  /** Get the state of this store formatted as a name request object from the NameX API */
  async function getNrData(): Promise<NameRequest> {
    const data = (await (
      await getNameRequest(nrNumber.value)
    ).json()) as NameRequest

    // NOTE: at this point, all store variables should be defined, but we will fallback to the API value just in case
    const applicant = data.applicants
    applicant.clientFirstName = clientFirstName.value || null
    applicant.clientLastName = clientLastName.value || null
    applicant.firstName = firstName.value || applicant.firstName
    applicant.lastName = lastName.value || applicant.lastName
    applicant.middleName = middleName.value || null
    applicant.addrLine1 = addressLine1.value || applicant.addrLine1
    applicant.addrLine2 = addressLine2.value || null
    applicant.addrLine3 = addressLine3.value || null
    applicant.city = city.value || applicant.city
    applicant.stateProvinceCd = province.value || applicant.stateProvinceCd
    applicant.postalCd = postalCode.value || applicant.postalCd
    applicant.countryTypeCd = country.value || applicant.countryTypeCd
    applicant.contact = contactName.value || ''
    applicant.phoneNumber = phone.value || applicant.phoneNumber
    applicant.emailAddress = conEmail.value || applicant.emailAddress
    applicant.faxNumber = fax.value || null

    nameChoices.value.forEach((choice) => {
      if (!choice.name) resetNameChoice(choice)
    })
    data.names = nameChoices.value

    data.requestTypeCd = fromMappedRequestType(
      requestType.value,
      requestActionCd.value
    )
    data.entity_type_cd = entityTypeCd.value
    data.request_action_cd = requestActionCd.value

    data.xproJurisdiction = jurisdiction.value || null
    data.natureBusinessInfo = natureOfBusiness.value || data.natureBusinessInfo
    data.additionalInfo = additionalInfo.value || ''
    data.comments = comments.value
    data.state = nrStatus.value
    data.previousStateCd = previousState.value || null
    data.previousNr = previousNr.value || null
    data.corpNum = corpNum.value || null
    data.furnished = furnished.value
    data.hasBeenReset = hasBeenReset.value || false
    data.consentFlag = consentFlag.value || null
    data.consent_dt = consentDate.value || null
    data.details = null
    data.nwpta = []

    const toFormattedDate = (dt: DateTime) =>
      dt.toUTC().toFormat('EEE, d MMM yyyy TTT')
    if (consentDate.value) {
      data.consent_dt = toFormattedDate(
        parseDate(consentDate.value).startOf('day')
      )
    }
    if (expiryDate.value) {
      data.expirationDate = parseDate(expiryDate.value).endOf('day').toISO()
    }
    if (submittedDate.value) {
      const submitDate = toFormattedDate(submittedDate.value)
      if (submitDate) data.submittedDate = submitDate
    }

    return data
  }

  interface EditAction {
    /** Return whether an edit action's internal state is valid (e.g. a name field is not empty).
     * This function is called before saving. A save will not occur if at least one edit action's validation fails.
     */
    validate: (() => boolean) | (() => Promise<boolean>)
    /** Update the store's value with the new values. This function is called after all validations have succeeded. */
    update: () => void
    /** Called when the user cancels an edit. */
    cancel: () => void
  }
  const editActions: Array<EditAction> = []
  function addEditAction(action: EditAction) {
    editActions.push(action)
  }

  /** Find a `RequestType` object from a `RequestTypeCode` */
  function findRequestTypeObject(code: RequestTypeCode) {
    return listRequestTypes.value.find((r) => r.value == code)
  }

  function parseIntoNameChoice(data: any, choice: NameChoice) {
    choice.choice = data.choice
    choice.name = data.name
    choice.state = data.state
    choice.consumptionDate = data.consumptionDate
    choice.corpNum = data.corpNum
    choice.conflict1 = data.conflict1
    choice.conflict2 = data.conflict2
    choice.conflict3 = data.conflict3
    choice.conflict1_num = data.conflict1_num
    choice.conflict2_num = data.conflict2_num
    choice.conflict3_num = data.conflict3_num
    choice.decision_text = data.decision_text
    choice.comment = data.comment
  }

  /** Parse a Name Request object into this store's variables.
   * @throws {Error} if the NR data is invalid.
   */
  async function parseNr(info: NameRequest) {
    if (!info || !info.names || info.names.length === 0)
      throw new Error('Cannot parse invalid NR data')

    clearConsent()

    resetNameChoice(compName1)
    resetNameChoice(compName2)
    resetNameChoice(compName3)

    sortNameChoices(info.names).forEach((nameChoice: NameChoice) =>
      parseIntoNameChoice(nameChoice, nameChoices.value[nameChoice.choice - 1])
    )

    const newCurrentNameChoice = nameChoices.value
      .filter(({ name, state }) => name && [Status.NotExamined, Status.Approved, Status.Condition].includes(state))[0]

    if (newCurrentNameChoice) {
      setCurrentNameChoice(newCurrentNameChoice)
    } else {
      const validNameChoices = nameChoices.value.filter(choice => choice.name)
      if (validNameChoices.every(choice => choice.state === Status.Rejected)) {
        currentNameObj.value = validNameChoices.at(-1)
      }
    }

    nrStatus.value = info.state
    previousState.value = info.previousStateCd ?? undefined
    requestType.value = toMappedRequestType(
      info.requestTypeCd,
      info.request_action_cd,
      info.entity_type_cd
    )

    consentFlag.value = info.consentFlag ?? undefined
    if (info.consent_dt) {
      const parsedConsentDate = parseDate(info.consent_dt)
      consentDate.value = getDateFromDateTime(parsedConsentDate) ?? undefined
    }

    // we keep the original data so that if fields exist that we do not use, we don't lose that
    // data when we put new data
    clientFirstName.value = info.applicants.clientFirstName ?? undefined
    clientLastName.value = info.applicants.clientLastName ?? undefined
    firstName.value = info.applicants.firstName
    middleName.value = info.applicants.middleName ?? undefined
    lastName.value = info.applicants.lastName
    addressLine1.value = info.applicants.addrLine1
    addressLine2.value = info.applicants.addrLine2 ?? undefined
    addressLine3.value = info.applicants.addrLine3 ?? undefined
    city.value = info.applicants.city
    province.value = info.applicants.stateProvinceCd
    postalCode.value = info.applicants.postalCd
    country.value = info.applicants.countryTypeCd
    contactName.value = info.applicants.contact
    phone.value = info.applicants.phoneNumber
    conEmail.value = info.applicants.emailAddress
    fax.value = info.applicants.faxNumber ?? undefined

    jurisdiction.value = info.xproJurisdiction ?? undefined
    jurisdictionNumber.value = info.homeJurisNum ?? undefined
    natureOfBusiness.value = info.natureBusinessInfo ?? undefined
    additionalInfo.value = info.additionalInfo ?? undefined
    comments.value = info.comments

    examiner.value = info.userId
    priority.value = info.priorityCd === 'Y'

    expiryDate.value = info.expirationDate
      ? getVancouverDate(info.expirationDate) ?? undefined
      : undefined

    submittedDate.value = parseDate(info.submittedDate)

    previousNr.value = info.previousNr ?? undefined
    corpNum.value = info.corpNum ?? undefined
    furnished.value = info.furnished
    hasBeenReset.value = info.hasBeenReset

    await payments.initialize(info.id)
  }

  function isUndoable(name: NameChoice): boolean {
    if (
      !userHasApproverRole.value || // if the NR is closed in any way, a name is not undoable - the NR will have to be re-opened first
      !isMyCurrentNr.value ||
      furnished.value === 'Y' || // if the NR is furnished, nothing is undoable
      name.state == Status.NotExamined || // if this name is complete (ie: anything other than NE) it's undoable
      name.state == null
    ) {
      return false
    }

    if (name.choice === 1) {
      // if name choices 2 and 3 have not been decided, then 1 is undoable
      return (
        (compName2.state == Status.NotExamined || compName2.state == null) &&
        (compName3.state == Status.NotExamined || compName3.state == null)
      )
    } else if (name.choice === 2) {
      // if name choice 3 has not been decided, then 2 is undoable
      return compName3.state == Status.NotExamined || compName3.state == null
    } else {
      return true
    }
  }

  /** Reset the given `NameChoice`.
   * @param keepName choose to preserve the name property instead of setting it to `null`.
   */
  function resetNameChoice(choice: NameChoice, keepName = false) {
    choice.state = Status.NotExamined
    choice.name = keepName ? choice.name : ''
    choice.decision_text = ''
    choice.conflict1 = ''
    choice.conflict2 = ''
    choice.conflict3 = ''
    choice.conflict1_num = ''
    choice.conflict2_num = ''
    choice.conflict3_num = ''
    choice.consumptionDate = null
    choice.corpNum = null
    choice.comment = null
  }

  async function undoNameChoiceDecision(name: NameChoice) {
    resetDecisionArea()
    currentNameObj.value = nameChoices.value[name.choice - 1]
    resetNameChoice(currentNameObj.value, true)
    await pushCurrentNameChoice()
    await fetchAndLoadNr(nrNumber.value)
  }

  /** Populate the currently examining name choice with selected conflicts and decision text. */
  function populateNameChoice(choice: NameChoice) {
    if (conflicts.selectedConflicts.length > 0) {
      // Populate the current name object's conflicts
      for (const n of [0, 1, 2]) {
        const conflict = conflicts.selectedConflicts[n]
        if (conflict == null) break

        switch (n) {
          case 0:
            choice.conflict1 = conflict.text
            choice.conflict1_num = conflict.nrNumber
            break
          case 1:
            choice.conflict2 = conflict.text
            choice.conflict2_num = conflict.nrNumber
            break
          case 2:
            choice.conflict3 = conflict.text
            choice.conflict3_num = conflict.nrNumber
            break
        }
      }
    }
    choice.name = choice.name?.trimEnd() ?? null
    choice.decision_text = requestorMessage.value.substring(0, 955)
  }

  /** Attempts to examine the next name choice. If that is not possible, rejects the entire NR. */
  async function attemptNextNameChoice() {
    try {
      await examineNextNameChoice()
    } catch (e) {
      await updateNRState(Status.Rejected)
    }
  }

  async function pushDecision(choice: NameChoice) {
    await pushCurrentNameChoice()
    if (choice.state === Status.Approved) {
      await updateNRState(Status.Approved)
    } else if (choice.state === Status.Condition) {
      await updateNRState(Status.Conditional)
    }
  }

  async function makeDecision(decision: Status) {
    if (!currentNameObj.value) return

    if (decision === Status.Approved) {
      if (consentRequired.value) {
        currentNameObj.value.state = Status.Condition
      } else {
        currentNameObj.value.state = Status.Approved
        // If there were conflicts selected but this is an approval, remove the selected conflicts.
        // Do NOT clear the conflicts if the "Consent Required" condition is also set - then it's intentional.
        conflicts.clearSelectedConflicts()
      }
    } else {
      currentNameObj.value.state = Status.Rejected
    }
    populateNameChoice(currentNameObj.value)

    await pushDecision(currentNameObj.value)
    if (
      ![Status.Approved, Status.Condition].includes(currentNameObj?.value?.state)
    ) {
      await attemptNextNameChoice()
    }
  }

  async function makeQuickDecision(decision: Status, decisionText: string) {
    if (!currentNameObj.value) return

    currentNameObj.value.decision_text = decisionText || null
    if (decision === Status.Approved) {
      currentNameObj.value.state = Status.Approved
    } else {
      currentNameObj.value.state = Status.Rejected
    }

    await pushDecision(currentNameObj.value)
    if (
      ![Status.Approved, Status.Condition].includes(currentNameObj?.value?.state)
    ) {
      await attemptNextNameChoice()
    }
  }

  /** Attempt to set the given name choice as the current one. Will throw an error if the choice cannot be set. */
  function setCurrentNameChoice(choice: NameChoice | undefined) {
    if (!choice) {
      currentNameObj.value = undefined
      return
    }
    const choiceHasAcceptableStatus = [
      Status.NotExamined,
      Status.Approved,
      Status.Condition,
    ].includes(choice.state)
    if (choiceHasAcceptableStatus && choice.name) {
      currentNameObj.value = choice
    } else {
      throw new Error(`Name choice ${choice.choice} cannot be examined`)
    }
  }

  /** Examine the next name choice in the name request. Throws an error if no name choice can be examined. */
  async function examineNextNameChoice() {
    const attempt = async (choice: NameChoice) => {
      try {
        setCurrentNameChoice(choice)
      } catch (e) {
        throw e
      }
    }
    if (currentChoice.value === 1) {
      await attempt(compName2)
    } else if (currentChoice.value === 2) {
      await attempt(compName3)
    } else {
      throw new Error('Cannot examine next name choice')
    }
  }

  async function updateNRStateAndPreviousState(
    nrState: Status,
    prevState: Status | null
  ) {
    const patch = { previousStateCd: prevState, state: nrState }
    await patchNameRequest(nrNumber.value, patch)
    await fetchAndLoadNr(nrNumber.value)
  }

  /** Revert to this NR's previous state if it exists. */
  async function revertToPreviousState() {
    if (previousState.value)
      return updateNRStateAndPreviousState(previousState.value, null)
  }

  /** Runs all edit actions, ensuring all actions have valid internal state before updating the store state.
   * @returns whether all the actions ran successfully
   */
  async function runEditActions(): Promise<boolean> {
    for (const action of editActions) {
      if (!(await action.validate())) {
        return false
      }
    }
    editActions.forEach((ea) => ea.update())
    return true
  }

  async function saveEdits() {
    if (!(await runEditActions())) {
      return
    }

    if (previousState.value === Status.Draft) {
      nrStatus.value = previousState.value
      previousState.value = undefined
    }

    await updateRequest()

    isEditing.value = false
    isHeaderShown.value = true
  }

  function updateRequestTypeRules(requestTypeObject: RequestType) {
    let rules = requestTypeRules.value.find(
      (rule) => rule.request_type == requestTypeObject.value
    )
    prevNrRequired.value = Boolean(rules?.prev_nr_required)
    corpNumRequired.value = Boolean(rules?.corp_num_required)
    additional_info_template.value = rules?.additional_info_template
    jurisdictionRequired.value = Boolean(rules?.jurisdiction_required)
  }

  async function getNextCompany() {
    conflicts.resetConflictLists()
    const nextNr = await getNextNrInQueue()
    await initialize(nextNr)
  }

  async function edit() {
    // if this isn't the user's INPROGRESS, make it that
    if (!isMyCurrentNr.value && !isClosed.value) {
      // track the previous state if it's currently in DRAFT (otherwise do not)
      if (nrStatus.value == Status.Draft) {
        await updateNRStateAndPreviousState(Status.InProgress, Status.Draft)
      } else {
        await updateNRState(Status.InProgress)
      }
    }
    isEditing.value = true
  }

  async function holdRequest() {
    await updateNRState(Status.Hold)
    conflicts.resetConflictLists()
  }

  function clearConsent() {
    consentDate.value = undefined
    consentFlag.value = undefined
  }

  function resetNrDecision() {
    conflicts.resetConflictLists()
    clearSelectedDecisionReasons()

    nrStatus.value = Status.InProgress
    if (!userHasApproverRole.value) {
      // initialize user in edit mode, with previous state set so NR gets set back to draft
      // when user is done changing name, adding comment, etc.
      previousState.value = Status.Draft
      isEditing.value = true
    }
  }

  async function reOpen() {
    // the NR could have been furnished in the time that it was approved to the time the user presses the Reopen button
    // double check to see if its furnished, if it is, reset the nr instead
    const nrResponse = await getNameRequest(nrNumber.value)
    const nrData = (await nrResponse.json()) as NameRequest
    if (nrData.furnished === 'Y') {
      alert('NR has been furnished, proceeding to reset NR instead.')
      return await resetNr()
    }
    resetNrDecision()
    // set reset flag so name data is managed between Namex and NRO correctly
    hasBeenReset.value = true
    await updateRequest()
  }

  async function resetNr() {
    resetNrDecision()
    clearConsent()
    furnished.value = 'N'
    await updateRequest()
  }

  async function claimNr() {
    await updateNRState(Status.InProgress)
  }

  async function cancelEdits() {
    if (previousState.value === Status.Draft) {
      await revertToPreviousState()
    } else {
      await fetchAndLoadNr(nrNumber.value)
    }
    isEditing.value = false
    isHeaderShown.value = false
    editActions.forEach((ea) => ea.cancel())
  }

  async function getTrademarks(query: string) {
    const response = await postTrademarks(query)
    const json = (await response.json()) as TrademarksObject
    return json.names
  }

  async function getConditions(query: string) {
    const response = await postConditions(query)
    const json = (await response.json()) as ConditionsList
    return json
  }

  async function getHistories(query: string) {
    // Remove Special Characters from query string.
    const cleanedQueryString: string = query.replace(/[^a-zA-Z\. ]/g, "")

    const response = await postHistories(cleanedQueryString)
    const json = (await response.json()) as Histories
    return json.names
  }

  async function getMacros(): Promise<Array<Macro>> {
    const response = await getDecisionReasons()
    return response.ok ? await response.json() : []
  }

  function parseHistoryMatches(historyMatches: Array<any>): Array<HistoryEntry> {
    return historyMatches.map((match) => {
      return {
          name: match.name,
          jurisdiction: match.parent_jurisdiction,
          nr_num: match.parent_id,
          start_date: match.parent_start_date,
          name_state_type_cd: match.parent_type,
          score: match.score ?? 0,
          submit_count: match.submit_count ?? 0
      }
    })
  }

  function parseConditions(data: ConditionsList): Array<Condition> {
    const conditions = []
    for (const word of data.restricted_words_conditions) {
      for (const cond of word.cnd_info) {
        conditions.push({
          ...cond,
          phrase: word.word_info.phrase,
        })
      }
    }
    return conditions
  }

  async function updateNRState(state: Status) {
    await patchNameRequest(nrNumber.value, { state: state })
    await fetchAndLoadNr(nrNumber.value)
  }

  async function cancelNr(commentText: string) {
    await postComment(commentText)
    resetDecisionArea()
    await updateNRState(Status.Cancelled)
  }

  /** Send name choice data to API */
  async function pushCurrentNameChoice() {
    if (currentNameObj.value)
      await putNameChoice(nrNumber.value, currentNameObj.value)
  }

  async function updateRequest() {
    try {
      const data = await getNrData()
      const response = await putNameRequest(nrNumber.value, data)
      if (!response.ok) {
        throw new Error('Failed to update NR')
      }
      await parseNr(await response.json())
    } catch {
        emitter.emit('error', {
          title: `Failed to update NR`,
          message: `An error occurred while trying to update ${nrNumber.value}`,
        })
      await fetchAndLoadNr(nrNumber.value)
    }
  }

  async function postComment(text: string) {
    const response = await postNewComment(nrNumber.value, text)
    if (response.ok) {
      comments.value.push(await response.json())
    }
  }

  function clearSelectedDecisionReasons() {
    conflicts.clearSelectedConflicts()
    selectedConditions.value = []
    selectedMacros.value = []
    selectedTrademarks.value = []
  }

  function resetDecisionArea() {
    conflicts.resetConflictLists()
    clearSelectedDecisionReasons()
    conflicts.autoAdd = true
    consentRequired.value = false
    customerMessageOverride.value = undefined
  }

  function resetHeader() {
    isEditing.value = false
    isHeaderShown.value = false
  }

  function resetRecipeData() {
    conflicts.resetMatches()
    conditions.value = []
    histories.value = []
    trademarks.value = []
  }

  /** Fetches the given NR's data and parses it into this store.
   * @throws {Error} if the NR data could not be fetched.
   */
  async function fetchAndLoadNr(nrNumber: string) {
    try {
      const response = await getNameRequest(nrNumber)
      if (response.ok) {
        await parseNr(await response.json())
      } else if (response.status === 404) {
        throw new Error('NR not found')
      } else {
        throw new Error('Failed to fetch NR data')
      }
    } catch (e) {
      throw new Error('Failed to fetch NR data')
    }
  }

  /** Fetch and load data for the recipe area (conflicts, trademarks, etc)
   * @throws {Error} if any part of the recipe data could not be loaded.
   */
  async function fetchAndLoadRecipeData(
    searchQuery: string,
    exactPhrase: string
  ) {
    if (!currentNameObj.value) return
    resetDecisionArea()
    const errors: Array<Error> = []
    /** TO_DO: Something needs to be done about this... */
    // try {
    //   trademarks.value = await getTrademarks(searchQuery)
    // } catch (e) {
    //   trademarks.value = []
    //   errors.push(e as Error)
    // }
    // try {
    //   histories.value = await getHistories(searchQuery)
    // } catch (e) {
    //   histories.value = []
    //   errors.push(e as Error)
    // }
    try {
      macros.value = await getMacros()
    } catch (e) {
      macros.value = []
      errors.push(e as Error)
    }
    try {
      const conditionsQuery = searchQuery.trim() || exactPhrase.trim()
      const conditionsJson = await getConditions(conditionsQuery)
      conditions.value = parseConditions(conditionsJson)
    } catch (e) {
      conditions.value = []
      errors.push(e as Error)
    }
    try {
      const results = await conflicts.initialize(searchQuery, exactPhrase)
      histories.value = parseHistoryMatches(results)
    } catch (e) {
      errors.push(e as Error)
    }
    if (errors.length > 0) {
      const message = errors.map(e => e.message).join('\n')
      throw new Error(message)
    }
  }

  /** Retrieves the NR number of the next NR that the user should examine. */
  async function getNextNrInQueue(): Promise<string> {
    const priorityQueue = useExaminationOptions().priorityQueue
    const response = await getNextNrNumber(priorityQueue)
    const json = await response.json()
    return json.nameRequest
  }

  /** Return a two-digit code for the given jurisdiction string.
   * Returns `undefined` if a code could not be found. */
  function getShortJurisdiction(jurisdiction: string): string | undefined {
    jurisdiction = jurisdiction.toUpperCase()
    if (jurisdiction.length === 2) return jurisdiction

    let index
    const textIndex = listJurisdictions.value.findIndex(
      (opt) => opt.text === jurisdiction
    )
    if (textIndex >= 0) index = textIndex
    const shortIndex = listJurisdictions.value.findIndex(
      (opt) => opt.short_desc === jurisdiction
    )
    if (shortIndex >= 0) index = shortIndex

    if (typeof index === 'number') {
      return listJurisdictions.value[index].value
    }
    return undefined
  }

  /** Update the route to the examine page, showing that it's examining the given NR number */
  async function updateRoute(nrNum: string) {
    await navigateTo({
      path: Route.Examine,
      query: { nr: nrNum.split(' ')[1] },
    })
  }

  /** Checks if the given NR number is valid. If not, throws an error. */
  async function checkNrNumber(nrNumber: string) {
    if (!isValidNrFormat(nrNumber)) {
      throw new Error('Incorrect NR number format')
    }
  }

  /** Retrieve the next NR in the queue and initialize this store with it. */
  async function initializeNext() {
    initializing.value = true
    const nrNumber = await getNextNrInQueue()
    await initialize(nrNumber)
    initializing.value = false
  }

  /** Initialize this store with the given NR. Throws an error if the NR data cannot be loaded.
   * If recipe area data cannot be loaded, the error will be captured and an error dialog will be shown.
   */
  async function initialize(newNrNumber: string) {
    initializing.value = true
    resetHeader()
    try {
      await checkNrNumber(newNrNumber)
      await fetchAndLoadNr(newNrNumber)
      await updateRoute(newNrNumber)
      updateRequestTypeRules(requestTypeObject.value)
      resetDecisionArea()
      nrNumber.value = newNrNumber
    } catch (e) {
      throw e
    } finally {
      initializing.value = false
    }
    try {
      resetRecipeData()
      await fetchAndLoadRecipeData(currentName.value || '', '')
    } catch (e: any) {
      emitter.emit('error', {
        title: 'Failed to load Recipe area',
        message: e.message,
      })
    }
  }

  return {
    initialize,
    initializeNext,
    updateRoute,
    priority,
    isComplete,
    examiner,
    isCurrentExaminer,
    trademarks,
    comments,
    isClosed,
    isEditing,
    isMakingDecision,
    isHeaderShown,
    nrNumber,
    nrStatus,
    previousState,
    listRequestTypes,
    requestType,
    requestTypeObject,
    requestTypeRules,
    requestActionCd,
    entityTypeCd,
    histories,
    autoAddDisabled,
    conflictSelectionDisabled,
    conditions,
    consentRequired,
    selectedConditions,
    customerMessageOverride,
    decisionSelectionsDisabled,
    macros,
    selectedMacros,
    selectedTrademarks,
    requestorMessageStrings,
    requestorMessage,
    compName1,
    compName2,
    compName3,
    nameChoices,
    currentNameObj,
    currentChoice,
    currentName,
    userHasApproverRole,
    userHasEditRole,
    isMyCurrentNr,
    furnished,
    listJurisdictions,
    previousNr,
    prevNrRequired,
    jurisdiction,
    jurisdictionRequired,
    jurisdictionNumber,
    consumptionDate,
    consumedBy,
    expiryDate,
    submittedDate,
    corpNum,
    corpNumRequired,
    consentDate,
    consentFlag,
    additionalInfo,
    additionalInfoTransformedTemplate,
    additional_info_template,
    natureOfBusiness,
    clientFirstName,
    clientLastName,
    firstName,
    middleName,
    lastName,
    addressLine1,
    addressLine2,
    addressLine3,
    city,
    province,
    postalCode,
    country,
    phone,
    fax,
    conEmail,
    contactName,
    canEdit,
    initializing,
    otherExaminerInProgress,
    expired,
    isApprovedAndExpired,
    canCancel,
    canClaim,
    exactHistoryMatch,
    addEditAction,
    isUndoable,
    getShortJurisdiction,
    makeDecision,
    undoNameChoiceDecision,
    makeQuickDecision,
    fetchAndLoadRecipeData,
    resetDecisionArea,
    fetchAndLoadNr,
    updateNRState,
    updateNRStateAndPreviousState,
    revertToPreviousState,
    saveEdits,
    updateRequest,
    cancelEdits,
    updateRequestTypeRules,
    getNextNrInQueue,
    getNextCompany,
    edit,
    holdRequest,
    reOpen,
    resetNr,
    claimNr,
    postComment,
    cancelNr,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useExamination, import.meta.hot))
}
