import { DateTime } from 'luxon'
import { defineStore } from 'pinia'
import { getDateWithTimeFromDateTime } from '~/util/date'
import { getNamexObject, getNamexApiUrl } from '~/util/namex-api'

export const useStatusStore = defineStore('status', () => {
  const holdNum = ref(0)
  const notExaminedNum = ref(0)
  const todayStr = computed(() => getDateWithTimeFromDateTime(DateTime.now()))

  /**
   * Return the number of name requests found from the given API call
   */
  async function getNumFound(url: URL): Promise<number> {
    try {
      const data = await getNamexObject(url)
      return data.response.numFound
    } catch (error) {
      console.error(error)
      return 0
    }
  }

  /**
   * Update the state of the status store
   */
  async function update() {
    const baseParams = new URLSearchParams({
      order: 'priorityCd:desc,submittedDate:asc',
      furnished: 'true',
      unfurnished: 'true',
      rows: '3',
      start: '0',
    })
    const url = () => getNamexApiUrl(`/requests?${baseParams}`)

    baseParams.set('queue', 'hold')
    const newHoldNum = await getNumFound(url())

    baseParams.set('queue', 'draft')
    const newNotExaminedNum = await getNumFound(url())

    holdNum.value = newHoldNum
    notExaminedNum.value = newNotExaminedNum
  }

  return { holdNum, notExaminedNum, todayStr, update }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useStatusStore, import.meta.hot))
}
