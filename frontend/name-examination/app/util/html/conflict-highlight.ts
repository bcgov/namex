import { highlightWord } from '~/util/html/highlight'

const escapeRegExp = (value: string) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

const INITIALS_GROUP_MIN = 3

export function queryLetterTokens(query: string): string[] {
  return (query.match(/[A-Za-z]+/g) || []).map((token) => token.toUpperCase())
}

/** Letters belonging to a 3+ consecutive single-letter run in the search query. */
export function initialsGroupComponentLetters(query: string): Set<string> {
  const terms = queryLetterTokens(query)
  const suppress = new Set<string>()
  let i = 0
  while (i < terms.length) {
    if (terms[i].length === 1) {
      let j = i + 1
      while (j < terms.length && terms[j].length === 1) {
        j += 1
      }
      if (j - i >= INITIALS_GROUP_MIN) {
        for (let k = i; k < j; k += 1) {
          suppress.add(terms[k])
        }
      }
      i = j
    } else {
      i += 1
    }
  }
  return suppress
}

/** Exact terms used for paint only. Does not mutate backend highlighting metadata. */
export function visualExactTerms(exactList: string[], searchQuery: string): string[] {
  const suppress = initialsGroupComponentLetters(searchQuery)
  if (suppress.size === 0) return exactList
  return exactList.filter((term) => !(term.length === 1 && suppress.has(term.toUpperCase())))
}

/** 1-character terms match standalone letters, not letters inside words. */
export function highlightConflictTerm(
  term: string,
  text: string,
  highlightCss: string
): string {
  if (!term) return text
  if (term.length === 1) {
    const re = new RegExp(`(?<![A-Za-z])${escapeRegExp(term)}(?![A-Za-z])`, 'gi')
    return text.replace(
      re,
      (match: string) => `<span class="${highlightCss}">${match}</span>`
    )
  }
  return highlightWord(term, text, highlightCss)
}

export function highlightConflictName(
  name: string,
  highlighting: {
    exact?: string[]
    synonyms?: string[]
    stems?: string[]
  } | null | undefined,
  searchQuery: string
): string {
  if (!name || !highlighting) return name

  const tokens = name.split(/(\s+)/)
  const exactList = visualExactTerms(
    Array.isArray(highlighting.exact) ? highlighting.exact : [],
    searchQuery
  )
  const synonymList: string[] = Array.isArray(highlighting.synonyms)
    ? highlighting.synonyms
    : []
  const stemList: string[] = Array.isArray(highlighting.stems) ? highlighting.stems : []

  const applyFirstMatchingCategory = (word: string): string => {
    for (const exact of exactList) {
      const highlighted = highlightConflictTerm(exact, word, 'exact-highlight')
      if (highlighted !== word) return highlighted
    }
    for (const synonym of synonymList) {
      const highlighted = highlightConflictTerm(synonym, word, 'synonym-highlight')
      if (highlighted !== word) return highlighted
    }
    for (const stem of stemList) {
      const highlighted = highlightConflictTerm(stem, word, 'stem-highlight')
      if (highlighted !== word) return highlighted
    }
    return word
  }

  return tokens
    .map((token) => (token.trim().length === 0 ? token : applyFirstMatchingCategory(token)))
    .join('')
}
