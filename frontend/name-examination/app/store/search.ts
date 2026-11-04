import { DateTime } from 'luxon'
import { defineStore } from 'pinia'
import { SearchColumns } from '~/enums/search-columns'
import {
  ClientNotification,
  ConsentRequired,
  LastUpdate,
  Priority,
  Submitted
} from '~/enums/filter-dropdowns'
import { getFormattedDateWithTime } from '~/util/date'
import { getNamexObject, getNamexApiUrl } from '~/util/namex-api'
import type { NameChoice } from '~/types'
import { sortNameChoices, getLocalStorageValue } from '~/util'
import { StatusSearchFilter, type Filters, type Row } from '~/types/search'
import { ConsentFlag } from '~/enums/codes'

export const defaultFilters = (): Filters => {
  return {
    [SearchColumns.Status]: getLocalStorageValue(SearchColumns.Status, StatusSearchFilter.Hold),
    [SearchColumns.LastModifiedBy]: '',
    [SearchColumns.NameRequestNumber]: '',
    [SearchColumns.Names]: '',
    [SearchColumns.ApplicantFirstName]: '',
    [SearchColumns.ApplicantLastName]: '',
    [SearchColumns.ConsentRequired]: getLocalStorageValue(SearchColumns.ConsentRequired, ConsentRequired.All),
    [SearchColumns.Priority]: getLocalStorageValue(SearchColumns.Priority, Priority.All),
    [SearchColumns.ClientNotification]: getLocalStorageValue(SearchColumns.ClientNotification, ClientNotification.All),
    [SearchColumns.Submitted]: getLocalStorageValue(SearchColumns.Submitted, Submitted.All),
    [SearchColumns.LastUpdate]: getLocalStorageValue(SearchColumns.LastUpdate, LastUpdate.All),
  }
}

export const DEFAULT_DISPLAY = 10

export const useSearchStore = defineStore('search', () => {
  const fixedColumns = Object.values(SearchColumns)
  const selectedColumns = ref(Object.values(SearchColumns)) // Initialize selected columns to all columns
  const rows: Ref<Row[]> = ref([])
  const resultNum = ref(0)
  const filters = reactive(defaultFilters())
  const selectedDisplay = ref(DEFAULT_DISPLAY)
  const selectedPage = ref(1)
  const lastPageNumber = computed(() =>
    Math.max(1, Math.ceil(resultNum.value / selectedDisplay.value))
  )
  const submittedDateOrder: Ref<'asc' | 'desc'> = ref('asc')
  const customSubmittedStartDate = ref('')
  const customSubmittedEndDate = ref('')
  const lastSubmittedDateOption = ref(filters.Submitted)
  const isLoading = ref(true)

  const formattedSearchParams = computed(() => {
      const params = {
      order: `submittedDate:${submittedDateOrder.value}`,
      queue:
        filters[SearchColumns.Status] === StatusSearchFilter.All
          ? ''
          : filters[SearchColumns.Status],
      consentOption: filters[SearchColumns.ConsentRequired],
      ranking: filters[SearchColumns.Priority],
      notification: filters[SearchColumns.ClientNotification],
      submittedInterval:
        filters[SearchColumns.Submitted] != Submitted.Custom
          ? filters[SearchColumns.Submitted]
          : '',
      lastUpdateInterval: filters[SearchColumns.LastUpdate],
      rows: selectedDisplay.value.toString(),
      start: (
        Math.max(0, selectedPage.value - 1) * selectedDisplay.value
      ).toString(),
      activeUser: filters[SearchColumns.LastModifiedBy],
      nrNum: filters[SearchColumns.NameRequestNumber],
      compName: filters[SearchColumns.Names],
      firstName: filters[SearchColumns.ApplicantFirstName],
      lastName: filters[SearchColumns.ApplicantLastName],
      hour: DateTime.now().hour.toString(),
      submittedStartDate: customSubmittedStartDate.value,
      submittedEndDate: customSubmittedEndDate.value,
    }

    // return the params object with all properties that have non-empty value
    return new URLSearchParams(
      Object.fromEntries(
        Object.entries(params).filter(([_, val]) => val !== '')
      )
    )
  })

  const formattedUrl = computed(() =>
    getNamexApiUrl(`/requests?${formattedSearchParams.value}`)
  )

  function parseRow(obj: any): Row {
    return {
      [SearchColumns.Status]: obj.stateCd,
      [SearchColumns.LastModifiedBy]: obj.activeUser,
      [SearchColumns.NameRequestNumber]: obj.nrNum,
      [SearchColumns.Names]: formatNames(obj.names),
      [SearchColumns.ApplicantFirstName]: obj.applicants[0]?.firstName,
      [SearchColumns.ApplicantLastName]: obj.applicants[0]?.lastName,
      [SearchColumns.NatureOfBusiness]:
        obj.natureBusinessInfo === null ? '' : obj.natureBusinessInfo,
      [SearchColumns.ConsentRequired]:
        obj.consentFlag === ConsentFlag.Received
          ? 'Received'
          : obj.consentFlag === ConsentFlag.Required
          ? 'Required'
          : obj.consentFlag === ConsentFlag.Waived
          ? 'Waived'
          :'No',
      [SearchColumns.Priority]:
        obj.priorityCd === 'Y' ? 'Priority' : 'Standard',
      [SearchColumns.ClientNotification]:
        obj.furnished === 'Y' ? 'Notified' : 'Not Notified',
      [SearchColumns.Submitted]: getFormattedDateWithTime(
        obj.submittedDate
      ),
      [SearchColumns.LastUpdate]: getFormattedDateWithTime(
        obj.lastUpdate
      ),
      [SearchColumns.LastComment]:
        obj.comments.length > 0
          ? obj.comments[obj.comments.length - 1].comment
          : '',
    }
  }

  async function getRows(url: URL): Promise<[numResults: number, rows: Row[]]> {
    try {
      const data = await getNamexObject(url)
      return [data.response.numFound, data.nameRequests[0].map(parseRow)]
    } catch (error) {
      return [0, []]
    }
  }

  async function updateRows() {
    isLoading.value = true // start loading

    const url = formattedUrl.value
    const [numResults, responseRows] = await getRows(url)

    // if the filters were changed while we were waiting for this response, discard the response
    if (url != formattedUrl.value) return

    resultNum.value = numResults
    rows.value = responseRows

    isLoading.value = false // end loading
  }

  function toggleSubmittedDateOrder() {
    if (submittedDateOrder.value === 'asc') {
      submittedDateOrder.value = 'desc'
    } else {
      submittedDateOrder.value = 'asc'
    }
  }

  function goToPreviousPage() {
    if (selectedPage.value > 1) {
      selectedPage.value--
    }
  }

  function goToNextPage() {
    if (selectedPage.value < lastPageNumber.value) {
      selectedPage.value++
    }
  }

  function resetColumns() {
    selectedColumns.value = Object.values(SearchColumns)
  }

  function resetFilters() {
    Object.assign(filters, defaultFilters())
  }

  function resetDisplayAndPage() {
    selectedDisplay.value = DEFAULT_DISPLAY
    selectedPage.value = 1
  }

  function $reset() {
    resetColumns()
    resetFilters()
    resetDisplayAndPage()
  }

  watch(
    () => [
      filters,
      selectedDisplay,
      submittedDateOrder,
      customSubmittedStartDate,
      customSubmittedEndDate,
    ],
    async (_state) => {
      selectedPage.value = 1

      // if the Submitted filter is set to custom but no custom dates are set yet, then that means
      // the user selected the custom date option in the dropdown but is still inputting the dates in the dialog.
      // the table should not update its rows in this scenario
      if (
        filters.Submitted === Submitted.Custom &&
        (customSubmittedStartDate.value === '' ||
          customSubmittedEndDate.value === '')
      ) {
        return
      }
      // clear custom date range if submitted date filter is not set to custom
      if (filters.Submitted !== Submitted.Custom) {
        customSubmittedStartDate.value = ''
        customSubmittedEndDate.value = ''
      }
      lastSubmittedDateOption.value = filters.Submitted
      await updateRows()
    },
    { deep: true }
  )

  watch(
    () => [selectedPage],
    async (_state) => {
      await updateRows()
    },
    { deep: true }
  )

  return {
    fixedColumns,
    selectedColumns,
    rows,
    resultNum,
    filters,
    selectedDisplay,
    selectedPage,
    lastPageNumber,
    submittedDateOrder,
    customSubmittedStartDate,
    customSubmittedEndDate,
    lastSubmittedDateOption,
    isLoading,
    formattedSearchParams,
    formattedUrl,
    updateRows,
    toggleSubmittedDateOrder,
    goToPreviousPage,
    goToNextPage,
    resetColumns,
    resetFilters,
    resetDisplayAndPage,
    $reset,
  }
})

function formatNames(names: Array<NameChoice>): string {
  sortNameChoices(names)
  let formatted = ''
  for (let name of names) {
    formatted += `${name.choice}. ${name.name}\n`
  }
  return formatted
}

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useSearchStore, import.meta.hot))
}
