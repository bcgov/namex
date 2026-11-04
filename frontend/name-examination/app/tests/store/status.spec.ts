import { DateTime } from 'luxon'
import { createPinia } from 'pinia'
import { beforeEach, describe, it, expect, vi } from 'vitest'
import { useStatusStore } from '~/store/status'
import { getDateWithTimeFromDateTime } from '~/util/date'
import { setApiHelperImpl } from '../util'

describe('Status store tests', () => {
  let status = useStatusStore()

  beforeEach(() => {
    status = useStatusStore(createPinia())
  })

  it('computes the correct date string', () => {
    expect(status.todayStr).toBe(getDateWithTimeFromDateTime(DateTime.now()))
  })

  it('updates the status data properly with a mock api response', async () => {
    const expectedHold = 20
    const expectedNotExamined = 100
    setApiHelperImpl((url: URL) => {
      const expectedNumFound =
        url.searchParams.get('queue')?.toLowerCase() === 'hold'
          ? expectedHold
          : expectedNotExamined

      const response = {
        response: {
          numFound: expectedNumFound,
        },
      }
      return new Promise((resolve) => resolve(response))
    })

    await status.update()
    expect(status.holdNum).toBe(expectedHold)
    expect(status.notExaminedNum).toBe(expectedNotExamined)
  })
})
