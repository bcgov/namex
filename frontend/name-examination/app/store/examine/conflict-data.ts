import {
  ConflictSource,
  type ConflictData,
  type ConflictListItem,
  type Corporation,
  type NameRequest,
} from '~/types'
import { getBusiness, getCorporation, getNameRequest } from '~/util/namex-api'

export const useConflictData = defineStore('conflict-data', () => {
  async function getCorpConflict(corpNum: string): Promise<Corporation> {
    // Currently, the corp number is in the Colin format, so there's no need to search in BCROS.
    //const businessResponse = await getBusiness(corpNum)
    //if (businessResponse.ok) return businessResponse.json()
    
    // search for business in COLIN
    const response = await getCorporation(corpNum)
    return response.json()
  }

  async function getNamesConflict(nrNumber: string): Promise<NameRequest> {
    const response = await getNameRequest(nrNumber)
    return response.json()
  }

  async function getConflictData(
    item: ConflictListItem
  ): Promise<ConflictData> {
    try {
      if (item.source === ConflictSource.Corp) {
        return getCorpConflict(item.nrNumber)
      } else {
        return getNamesConflict(item.nrNumber)
      }
    } catch {
      throw new Error(`Failed to retrieve conflict data for ${item.text}`)
    }
  }

  return { getConflictData }
})
