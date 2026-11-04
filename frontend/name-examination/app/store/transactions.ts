import {
  ConsentFlag,
  type EntityTypeCode,
  type RequestActionCode,
  type RequestTypeCode,
} from '~/enums/codes'
import { Status } from '~/enums/nr-status'
import {
  type NameChoice,
  type NameRequest,
  type TransactionEntry,
  type Transactions,
} from '~/types'
import { emitter } from '~/util/emitter'
import { getNameRequest, getTransactions } from '~/util/namex-api'
import { toMappedRequestType } from '~/util/request-type'
import requestTypes from '~/data/request_types.json'
import { sortNameChoices } from '~/util'

export const useTransactions = defineStore('transactions', () => {
  const nr = ref<NameRequest>()
  const transactions = ref<Array<TransactionEntry>>([])
  const loadingNr = ref(false)
  const loadingTransactions = ref(false)

  async function loadNr(nrNumber: string) {
    loadingNr.value = true
    const nrResponse = await getNameRequest(nrNumber)
    nr.value = await nrResponse.json()
    loadingNr.value = false
  }

  async function loadTransactions(nrNumber: string) {
    loadingTransactions.value = true
    const transactionsResponse = await getTransactions(nrNumber)
    const transactionsJson = (await transactionsResponse.json()) as Transactions
    transactionsJson.transactions.forEach(t => sortNameChoices(t.names))
    transactions.value = transactionsJson.transactions
    loadingTransactions.value = false
  }

  async function initialize(nrNumber: string) {
    try {
      await loadNr(nrNumber)
      await loadTransactions(nrNumber)
    } catch (e) {
      emitter.emit('error', {
        title: 'Transactions Error',
        message: 'Failed to retrieve transactions data.',
      })
    } finally {
      loadingNr.value = false
      loadingTransactions.value = false
    }
  }

  function getStatusDisplay(status: Status | null, names: Array<NameChoice>) {
    if (!status) return 'N/A'

    let displayState = status as string
    if (status === Status.Conditional) {
      displayState = 'CONDITIONAL APPROVED'
    } else if (status === Status.Consumed && names && names.length > 0) {
      const approvedName = names.find((name) =>
        [Status.Approved, Status.Condition].includes(name.state)
      )
      displayState =
        approvedName?.state === Status.Condition
          ? 'CONDITIONAL APPROVED'
          : 'APPROVED'
      displayState += ` / Used for ${approvedName?.corpNum}`
    }
    return displayState
  }

  function getRequestTypeDisplay(
    requestType: RequestTypeCode,
    action: RequestActionCode
  ) {
    if (!nr.value) return 'N/A'
    const mapped = toMappedRequestType(
      requestType,
      action,
      nr.value.entity_type_cd
    )
    return requestTypes.find((r) => r.value == mapped)?.text || 'N/A'
  }

  function getConsentDisplay(date: string | null, consentFlag: ConsentFlag) {
    return date
      ? 'Required. Received.'
      : consentFlag === ConsentFlag.Required
      ? 'Required. Not yet received.'
      : 'Not required'
  }

  async function getLatestIdir(nrNumber: string) {
    try {
      await loadNr(nrNumber)
      await loadTransactions(nrNumber)

      const latestIdirEntry = transactions.value
        .filter(entry => entry.user_name.includes('idir'))
        .sort((a, b) => new Date(b.eventDate).getTime() - new Date(a.eventDate).getTime())
        [0]

      return latestIdirEntry ? latestIdirEntry.user_name : 'N/A'
    } catch (error) {
      return 'N/A'
    }
  }

  return {
    nr,
    transactions,
    loadingNr,
    loadingTransactions,
    initialize,
    getStatusDisplay,
    getRequestTypeDisplay,
    getConsentDisplay,
    getLatestIdir
  }
})
