import { DateTime } from 'luxon'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, it, expect } from 'vitest'
import { SearchColumns } from '~/enums/search-columns'
import {
  ClientNotification,
  ConsentRequired,
  LastUpdate,
  Priority,
  Submitted,
} from '~/enums/filter-dropdowns'
import { Status } from "~/enums/nr-status"
import { DEFAULT_DISPLAY, defaultFilters, useSearchStore } from '~/store/search'
import { mockNextApiHelperResponse } from '../util'
import mockOneNameRequest from '../data/mockOneNameRequest.json'
import { getFormattedDateWithTime } from '~/util/date'

describe('Search store tests', () => {
  let search = useSearchStore()

  beforeEach(() => {
    setActivePinia(createPinia())
    search = useSearchStore()
  })

  it('creates the correct api params', () => {
    const testName = 'test'
    search.filters[SearchColumns.ApplicantFirstName] = testName

    let expectedParams = new URLSearchParams({
      // this is to match current code, verify with business if this is correct
      // order: 'priorityCd:desc,submittedDate:asc',
      order: 'submittedDate:asc',
      queue: Status.Hold,
      consentOption: ConsentRequired.All,
      ranking: Priority.All,
      notification: ClientNotification.All,
      submittedInterval: Submitted.All,
      lastUpdateInterval: LastUpdate.All,
      rows: '10',
      start: '0',
      firstName: testName,
      hour: DateTime.now().hour.toString(),
    })

    expect(search.formattedSearchParams).toEqual(expectedParams)
  })

  it('computed the last page number correctly', () => {
    search.resultNum = 1
    search.selectedDisplay = 10
    expect(search.lastPageNumber).toBe(1)

    search.resultNum = 11
    search.selectedDisplay = 10
    expect(search.lastPageNumber).toBe(2)

    search.resultNum = 11
    search.selectedDisplay = 20
    expect(search.lastPageNumber).toBe(1)

    search.resultNum = 20
    search.selectedDisplay = 20
    expect(search.lastPageNumber).toBe(1)
  })

  it('parses and updates the rows given an api response', async () => {
    mockNextApiHelperResponse(mockOneNameRequest)
    await search.updateRows()
    const nameRequests = mockOneNameRequest.nameRequests[0]

    expect(search.rows).toHaveLength(nameRequests.length)

    const actualRow = search.rows[0]
    const expectedRow = nameRequests[0]

    expect(actualRow[SearchColumns.Status]).toBe(expectedRow.stateCd)
    expect(actualRow[SearchColumns.LastModifiedBy]).toBe(expectedRow.activeUser)
    expect(actualRow[SearchColumns.NameRequestNumber]).toBe(expectedRow.nrNum)
    expect(actualRow[SearchColumns.Names]).toContain(expectedRow.names[0].name)
    expect(actualRow[SearchColumns.Names]).toContain(expectedRow.names[1].name)
    expect(actualRow[SearchColumns.Names]).toContain(expectedRow.names[2].name)
    expect(actualRow[SearchColumns.ApplicantFirstName]).toBe(
      expectedRow.applicants[0].firstName
    )
    expect(actualRow[SearchColumns.ApplicantLastName]).toBe(
      expectedRow.applicants[0].lastName
    )
    expect(actualRow[SearchColumns.NatureOfBusiness]).toBe('')
    expect(actualRow[SearchColumns.ConsentRequired]).toBe(ConsentRequired.No)
    expect(actualRow[SearchColumns.Priority]).toBe(Priority.Priority)
    expect(actualRow[SearchColumns.ClientNotification]).toBe(
      ClientNotification.NotNotified
    )
    expect(actualRow[SearchColumns.Submitted]).toBe(
      getFormattedDateWithTime(expectedRow.submittedDate)
    )
    expect(actualRow[SearchColumns.LastComment]).toBe(
      expectedRow.comments[expectedRow.comments.length - 1].comment
    )
  })

  it('toggles the submitted date order', () => {
    search.submittedDateOrder = 'asc'
    search.toggleSubmittedDateOrder()
    expect(search.submittedDateOrder).toBe('desc')

    search.toggleSubmittedDateOrder()
    expect(search.submittedDateOrder).toBe('asc')
  })

  it('goes to the previous page', () => {
    search.resultNum = 100
    search.selectedDisplay = 10
    search.selectedPage = 2

    search.goToPreviousPage()
    expect(search.selectedPage).toBe(1)

    search.goToPreviousPage()
    expect(search.selectedPage).toBe(1)
  })

  it('goes to the next page', () => {
    search.resultNum = 20
    search.selectedDisplay = 10
    search.selectedPage = 1

    search.goToNextPage()
    expect(search.selectedPage).toBe(2)

    search.goToNextPage()
    expect(search.selectedPage).toBe(2)
  })

  it('resets the filters', () => {
    search.filters[SearchColumns.ApplicantFirstName] = 'test1'
    search.filters[SearchColumns.ApplicantFirstName] = 'test2'
    search.filters[SearchColumns.Priority] = Priority.Standard

    search.$reset()
    expect(search.filters).toStrictEqual(defaultFilters())
  })

  it('resets the columns', () => {
    search.selectedColumns = [SearchColumns.NameRequestNumber]

    search.$reset()
    expect(search.selectedColumns).toEqual(Object.values(SearchColumns))
  })

  it('resets the display options', () => {
    search.resultNum = 500
    search.selectedDisplay = 100
    search.goToNextPage()

    search.$reset()
    expect(search.resultNum).toBe(500)
    expect(search.selectedDisplay).toBe(DEFAULT_DISPLAY)
    expect(search.selectedPage).toBe(1)
  })
})
