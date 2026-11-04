import type { ConflictList, ConflictListItem, ConflictSource } from '~/types'
import { conflictSearchErrorMessage, getPossibleConflicts } from '~/util/namex-api'
import { highlightConflictName } from '~/util/html/conflict-highlight'
import { useExaminationRecipe } from './recipe'

export const useConflicts = defineStore('conflicts', () => {
  const exactMatches = ref<Array<ConflictListItem>>([])
  const synonymMatches = ref<Array<ConflictList>>([])
  const cobrsPhoneticMatches = ref<Array<ConflictList>>([])
  const phoneticMatches = ref<Array<ConflictList>>([])

  const loading = ref(false)

  const selectedConflicts = ref<Array<ConflictListItem>>([])
  const comparedConflicts = ref<Array<ConflictListItem>>([])
  const prevSelectedConflicts = ref<Array<ConflictListItem>>([])
  const prevComparedConflicts = ref<Array<ConflictListItem>>([])
  const autoAdd = ref(true)

  /** Flattened array of every `ConflictList` across all buckets. */
  const lists = computed<Array<ConflictList>>(() =>
    [
      synonymMatches.value,
      cobrsPhoneticMatches.value,
      phoneticMatches.value,
    ].flat()
  )

  /** List of all `ConflictList`s that contain items within them. */
  const nonEmptyLists = computed(() =>
    lists.value.filter((list) => list.children.length > 0)
  )

  /** The first `ConflictListItem` among every `ConflictList` across all buckets. */
  const firstConflictItem = computed(() =>
    [...exactMatches.value, ...lists.value.flatMap((list) => list.children)].at(
      0
    )
  )

  function isConflictSelected(conflict: ConflictListItem) {
    const conflictsList = autoAdd.value
      ? selectedConflicts.value
      : comparedConflicts.value
    return conflictsList.map((c) => c.nrNumber).includes(conflict.nrNumber)
  }

  /** If the given conflict is not selected, selects it. Otherwise, deselects it. */
  function toggleConflict(conflict: ConflictListItem) {
    if (isConflictSelected(conflict)) {
      deselectConflict(conflict)
    } else {
      selectConflict(conflict)
    }
  }

  /** Map a single result from possible-conflicts response to a ConflictListItem */
  function mapToItem(result: any, searchQuery: string): ConflictListItem {
    const source =
      result.parent_type === 'CORP'
        ? ('CORP' as unknown as ConflictSource)
        : ('NAMEREQUEST' as unknown as ConflictSource)
    return {
      text: result.name,
      highlightedText: highlightConflictName(
        result?.name ?? '',
        result?.highlighting,
        searchQuery
      ),
      nrNumber: result.parent_id,
      startDate: result.parent_start_date ?? '',
      jurisdiction: result.parent_jurisdiction ?? undefined,
      source,
      ui: { focused: false, open: false },
    }
  }

  /** Group results into ConflictList buckets - no filtering, all results pass through */
  function groupIntoLists(results: any[], searchQuery: string): Array<ConflictList> {
    if (!results?.length) return []
    const group: ConflictList = {
      text: '',
      highlightedText: '',
      meta: undefined,
      children: results.map((result) => mapToItem(result, searchQuery)),
      ui: { focused: false, open: false },
    }
    return group.children.length > 0 ? [group] : []
  }

  async function initialize(searchQuery: string, exactPhrase: string) {
    loading.value = true
    resetConflictLists()
    try {
      if (!searchQuery.trim() && !exactPhrase.trim()) {
        return []
      }
      const response = await getPossibleConflicts(searchQuery, exactPhrase)
      if (!response.ok) throw new Error(await conflictSearchErrorMessage(response))

      const data = await response.json()
      const results: any[] = data.names ?? []
      const exact: any[] = data.exactNames ?? []
      const histories: any[] = data.histories ?? []
      const paintQuery = searchQuery.trim() || exactPhrase.trim()

      // Exact Match bucket
      exactMatches.value = exact.map((result) => mapToItem(result, paintQuery))
      exactMatches.value.forEach((match) => selectConflict(match))

      const hasApiBucket = results.some(
        (r) => r.bucket === 'synonym' || r.bucket === 'phonetic',
      )
      if (hasApiBucket) {
        synonymMatches.value = groupIntoLists(
          results.filter((r) => r.bucket === 'synonym'),
          paintQuery,
        )
        phoneticMatches.value = groupIntoLists(
          results.filter((r) => r.bucket === 'phonetic'),
          paintQuery,
        )
      } else {
        const phoneticOnly = results.filter((r) => {
          const hasExact = r.highlighting?.exact?.length > 0
          const hasStems = r.highlighting?.stems?.length > 0
          const hasSynonyms = r.highlighting?.synonyms?.length > 0
          const hasPhonetic = r.highlighting?.phonetic?.length > 0
          return hasPhonetic && !hasExact && !hasStems && !hasSynonyms
        })

        const stemOrSynonym = results.filter((r) => {
          const hasExact = r.highlighting?.exact?.length > 0
          const hasStems = r.highlighting?.stems?.length > 0
          const hasSynonyms = r.highlighting?.synonyms?.length > 0
          const hasPhonetic = r.highlighting?.phonetic?.length > 0
          const hasAnyHighlight = hasExact || hasStems || hasSynonyms || hasPhonetic
          return (hasExact || hasStems || hasSynonyms) || !hasAnyHighlight
        })

        phoneticMatches.value = groupIntoLists(phoneticOnly, paintQuery)
        synonymMatches.value = groupIntoLists(stemOrSynonym, paintQuery)
      }

      cobrsPhoneticMatches.value = []

      if (exactMatches.value.length === 0 && nonEmptyLists.value.length > 0) {
        nonEmptyLists.value[0].ui.open = true
      }
      useExaminationRecipe().reset()

      // return raw history matches for the caller (parseHistoryMatches in the examine store)
      return histories
    } catch (e) {
      resetMatches()
      throw e
    } finally {
      loading.value = false
    }
  }

  function clearSelectedConflicts() {
    selectedConflicts.value = []
  }

  function resetMatches() {
    exactMatches.value = []
    synonymMatches.value = []
    cobrsPhoneticMatches.value = []
    phoneticMatches.value = []
    loading.value = false
  }

  function resetConflictLists() {
    clearSelectedConflicts()
    comparedConflicts.value = []
  }

  function selectConflict(conflict: ConflictListItem) {
    comparedConflicts.value.push(conflict)
    if (autoAdd.value) {
      selectedConflicts.value.push(conflict)
    }
  }

  function deselectConflict(conflict: ConflictListItem) {
    const notConflict = (c: ConflictListItem) =>
      c.nrNumber !== conflict.nrNumber
    selectedConflicts.value = selectedConflicts.value.filter(notConflict)
    comparedConflicts.value = comparedConflicts.value.filter(notConflict)
  }

  /** Keep compared conflicts synchronized with selected conflicts when auto add is enabled. */
  function syncSelectedAndComparedConflicts() {
    if (autoAdd.value) {
      comparedConflicts.value = selectedConflicts.value.slice()
    }
  }

  /** Reset selectedConflicts and comparedConflicts and save existing data */
  function disableAutoAdd () {
    if (!autoAdd.value) {
      const initialRun = (prevSelectedConflicts.value.length === 0 && prevComparedConflicts.value.length === 0)
      for (const conflict of selectedConflicts.value) {
        if (initialRun) {
          prevSelectedConflicts.value.push(conflict)
          prevComparedConflicts.value.push(conflict)
        }
        const notConflict = (c: ConflictListItem) =>
          c.nrNumber !== conflict.nrNumber
        selectedConflicts.value = selectedConflicts.value.filter(notConflict)
        comparedConflicts.value = comparedConflicts.value.filter(notConflict)
      }
    }
  }

  /** Reassign selectedConflicts and comparedConflicts */
  function enableAutoAdd () {
    if (autoAdd.value) {
      selectedConflicts.value = prevSelectedConflicts.value
      comparedConflicts.value = prevComparedConflicts.value
    }
  }

  return {
    initialize,
    exactMatches,
    synonymMatches,
    cobrsPhoneticMatches,
    phoneticMatches,
    selectedConflicts,
    comparedConflicts,
    loading,
    isConflictSelected,
    toggleConflict,
    resetMatches,
    clearSelectedConflicts,
    resetConflictLists,
    selectConflict,
    deselectConflict,
    disableAutoAdd,
    enableAutoAdd,
    autoAdd,
    lists,
    nonEmptyLists,
    firstConflictItem,
    syncSelectedAndComparedConflicts,
  }
})
