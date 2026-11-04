import { getStats } from '~/util/namex-api'
import { getFormattedDateWithTime } from '~/util/date'
import { sortNameChoices } from '~/util'
import { type NameRequest } from '~/types'
import { defineStore } from 'pinia'

export const useStatsStore = defineStore('stats', () => {
  /**
   * Fetches paged statistics data based on the provided timespan and myStats flag.
   *
   * @param {string | null} timespan - The timespan for the statistics data. If null, the default timespan is used.
   * @param {boolean} myStats - A flag indicating whether to fetch statistics related to user's own stats.
   * @return {Promise<any>} A promise that resolves with the fetched statistics data.
   * @throws {Error} Throws an error if the fetching process fails.
   */
  async function getPagedStats (timespan: string | null, myStats: boolean): Promise<any> {
    const params = new URLSearchParams({
      timespan: timespan || '1',
      currentpage: '1',
      perpage: '1000'
    })
    if (myStats) params.append('myStats', 'True')

    try {
      const response = await getStats(params)

      if (response.ok) {
        const jsonData = await response.json() // Parse response JSON

        if (jsonData.numRecords >= 0) {
          const requestsData = jsonData.nameRequests as Array<NameRequest>

          const processedData = requestsData.map((statsData:any) => {
            statsData.names = sortNameChoices(statsData.names)
            if (statsData.comments.length === 1 && statsData.comments[0].timestamp) {
              statsData.comments[0].timestamp = getFormattedDateWithTime(statsData.comments[0].timestamp)
            }
            statsData.lastUpdate = getFormattedDateWithTime(statsData.lastUpdate)
            statsData.names.forEach((name:any) => {
              if (name.decision_text) {
                name.decision_text = name.decision_text.split(/\n\n/)
              }
            })
            return statsData
          })
          return {
            nameRequests: processedData,
            numRecords: jsonData.numRecords
          }
        }
      } else {
        throw new Error('Network response was not ok')
      }
    } catch (error) {
      console.error('There was a problem with your fetch operation:', error)
      throw error // Rethrow the error to handle it elsewhere if needed
    }
  }

  return {
    getPagedStats
  }
})
