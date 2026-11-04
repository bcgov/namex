import type { ConflictList, ConflictListItem, NameChoice } from '~/types'
import { getBusiness, getCorporation, getNameRequest } from './namex-api'
import { Status } from '~/enums/nr-status'

/**
 * Return whether a given string is in a valid NR number format, i.e. NR xxxxxxx
 * @param input The NR number string to validate
 * @param allowNumbersOnly allow strings that are just a seven digit number, i.e. without the 'NR'
 */
export function isValidNrFormat(
  input: string,
  allowNumbersOnly: boolean = false
): boolean {
  const withLetters = /^NR \d{7}$/
  const numbersOnly = /^\d{7}$/
  return (
    withLetters.test(input) || (allowNumbersOnly && numbersOnly.test(input))
  )
}

export async function nrExists(nrNumber: string): Promise<boolean> {
  try {
    const response = await getNameRequest(nrNumber)
    return response.ok
  } catch (e) {
    return false
  }
}

/** Return whether the given input is in the correct format for a corp number.
 * @throws an error if the corp num check fails (e.g. the API request times out)
 *
 */
export function isValidCorpNumFormat(input: string) {
  // valid corp numbers are between 7 and 10 characters long
  return input.length >= 7 && input.length <= 10
}

/** Return whether the company with the given corp num exists. */
export async function corpExists(input: string) {
  // query entities for the corp num. if not found, query again from colin
  const businessResponse = await getBusiness(input)
  if (businessResponse.ok) return true

  // ignore corp num prefix 'BC' if applicable to match colin BC corp num format for the validation
  const corpNum = input.replace(/^BC+/i, '')
  const corporationResponse = await getCorporation(corpNum)
  if (corporationResponse.ok) {
    // the corporation exists
    return true
  } else if (corporationResponse.status === 404) {
    return false
  } else {
    throw new Error('Failed to get corporation')
  }
}

export function sortNameChoices(choices: Array<NameChoice>) {
  return choices.sort((n1, n2) => n1.choice - n2.choice)
}

/** Get a default empty `NameChoice` object. */
export function getEmptyNameChoice(
  choiceIndex: number,
  nameString = ''
): NameChoice {
  return {
    choice: choiceIndex,
    name: nameString,
    state: Status.NotExamined,
    decision_text: null,
    conflict1: null,
    conflict2: null,
    conflict3: null,
    consumptionDate: null,
    corpNum: null,
    conflict1_num: null,
    conflict2_num: null,
    conflict3_num: null,
    comment: null,
  }
}

/** Sanitize the given query string to remove special characters. */
export function sanitizeQuery(query: string, exactMatch = false) {
  const baseSanitized = query
    .replace(/(^| )(\$+(\s|$)+)+/g, '$1DOLLAR$3')
    .replace(/(^| )(¢+(\s|$)+)+/g, '$1CENT$3')
    .replace(/\$/g, 'S')
    .replace(/¢/g, 'C')
    .replace(/[\\\/]/g, ' ')
    .replace(/(`|~|!|\||\(|\)|\[|\]|\{|\}|:|"|\^|#|%|\?)/g, '')
  if (exactMatch) {
    return baseSanitized
      .replace(' /', '/')
      .replace(/[\+\-]{2,}/g, '')
      .replace(/\s[\+\-]$/, '')
  } else {
    return baseSanitized.replace(/[&+\-]/, ' ').replace(/,/g, '')
  }
}

/** Parse an array of address strings returned from the NameX API into 2-3 lines of addresses. */
export function parseAddress(lines: Array<string>): Array<string> {
  const firstTwoLines = lines.slice(0, lines.length - 4)
  const lastFourLines = lines.slice(lines.length - 4).join(' ')
  const output = [...firstTwoLines, lastFourLines]
  if (
    output[0].toUpperCase() === 'N' &&
    output[1].toUpperCase() === 'O' &&
    output[2].toUpperCase() === 'T'
  ) {
    return ['Address not', 'available']
  }
  return output
}

/** Get the circular index of `i` in an array of length `n` */
export function getCircularIndex(i: number, n: number) {
  return ((i % n) + n) % n
}

/** Distinguish a parameter that may be a `ConflictListItem` */
export function isConflictListItem(
  obj: ConflictListItem | ConflictList
): obj is ConflictListItem {
  return 'nrNumber' in obj
}

/** Distinguish a parameter that may be a `ConflictList` */
export function isConflictList(
  obj: ConflictListItem | ConflictList
): obj is ConflictList {
  return !isConflictListItem(obj)
}

/** Clamp `value` to interval [`min`, `max`] (inclusive) */
export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max)
}

/** Get `value` from local storage using `key` */
export const getLocalStorageValue = <T>(key: string, defaultValue: T): T => {
  const storedValue = window.localStorage.getItem(key)
  if (storedValue === null) {
    window.localStorage.setItem(key, JSON.stringify(defaultValue))
    return defaultValue
  }
  try {
    // Try to parse into the correct type
    const item = JSON.parse(storedValue) as T
    return item
  } catch (error) {
      window.localStorage.setItem(key, JSON.stringify(defaultValue))
      return defaultValue
    }
}
