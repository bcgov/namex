import removeAccents from 'remove-accents'

export function removeExcessSpaces (name: string): string {
  // trims any spaces padding <name> and any internal spaces between words in excess of a single space per two words.
  name = name.replace(/\s\s+/g, ' ')
  return name.trim()
}

export function sanitizeName (name: string): string {
  if (!name) return '' // safety check

  // replaces most characters from the extended-latin character set, such as those modified with diacritics, and most
  // ligatures, with their closest ASCII equivalents (eg. é => e, ø => o, æ => ae); removes any symbols outside of
  // the limited set supported by Namex; capitalizes; and trims any spaces padding <name> and any internal spaces
  // between words in excess of a single space per two words.
  name = removeAccents(name)
  // eslint-disable-next-line no-useless-escape
  name = name.replace(/[^\sa-zA-Z0-9^\[\]*/+&().,="'#@!?;:-]/g, '')
  return removeExcessSpaces(name.toUpperCase())
}

export function matchWord (name: string, word: string): string[] | string {
  // matches all occurrences of a word or phrase <word> in a longer string <name> where <word> appears in one of the
  // following three ways: "word ", " word ", or " word" [ RegExp: /(\\s|^)word(\\s|$)/ ] with awareness of the special
  // cases for LIMITED and LIMITEE which are both designations on their own and part of others so as to only return
  // one match for the longer designation in such cases.  Return value is an array of <word> of length equal to the
  // number of matches or null if there were none.
  if (name) name = name.toUpperCase()
  if (word) word = word.toUpperCase()
  function escWrd () {
    return word.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&')
  }
  function matchWrd () {
    return name.match(new RegExp('(\\s|^)' + escWrd() + '(\\s|$)'))
  }
  if (containsLongAndShortDesignation(name, word)) {
    return null
  }
  const { length } = word
  const output = []
  while (matchWrd()) {
    const match = matchWrd()
    output.push(match[0].trim())
    const newStartIndex = match.index + length - 1
    name = name.substring(newStartIndex)
  }
  if (output.length > 0) {
    return output
  }
  return null
}

export function replaceWord (name: string, word: string, substitution: string | null = null): string {
  // when called with 2 arguments (<name> and <word>), finds all matches of <word> within <name> according to the same
  // rules as matchWord above, replaces them with nothing (ie. removes them), and returns <name>.  When called with 3
  // arguments, it finds the first match for <word> in <name>, replaces it with <substitution>, and returns <name>.  In
  // either case, if there are no matches, <name> is returned without modification (aside from capitalization)
  if (name) name = name.toUpperCase()
  if (word) word = word.toUpperCase()

  if (containsLongAndShortDesignation(name, word)) {
    return name
  }
  function escWrd (w) {
    return w.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&')
  }
  function replWrd (n) {
    return n.replace(new RegExp('(\\s|^)' + escWrd(word) + '(\\s|$)'), ' ')
  }
  if (substitution) {
    substitution = ' ' + substitution.toUpperCase() + ' '
    name = name.replace(new RegExp('(\\s|^)' + escWrd(word) + '(\\s|$)'), substitution)
  } else {
    while (name !== replWrd(name)) {
      name = replWrd(name)
    }
  }
  return removeExcessSpaces(name)
}

export function containsLongAndShortDesignation (name: string, word: string): boolean {
  if (word) word = word.toUpperCase()
  if (name) name = name.toUpperCase()

  if (word === 'LIMITED') {
    const designationsContainingWord = [
      ' LIMITED LIABILITY CO.',
      ' LIMITED LIABILITY COMPANY',
      ' LIMITED LIABILITY PARTNERSHIP',
      ' LIMITED PARTNERSHIP'
    ]
    for (const designation of designationsContainingWord) {
      if (name.includes(designation)) {
        return true
      }
    }
  }
  if (word === 'LIMITEE') {
    const designationsContainingWord = [
      ' SOCIETE A RESPONSABILITE LIMITEE',
      ' SOCIETE EN NOM COLLECTIF A RESPONSABILITE LIMITEE'
    ]
    for (const designation of designationsContainingWord) {
      if (name.includes(designation)) {
        return true
      }
    }
  }
  return false
}

/**
 * Builds the URL of the Business Home (new Registry Home) login page.
 * If a valid idp is specified, that login is triggered immediately instead of
 * showing the login options.
 */
export function getBusinessHomeLoginUrl (returnUrl: string = window.location.href, idp?: string): string {
  const businessHomeUrl = sessionStorage.getItem('BUSINESS_HOME_URL')
  const idpParam = ['bcsc', 'bceid', 'idir'].includes(idp) ? `&idp=${idp}` : ''
  return `${businessHomeUrl}en-CA/auth/login?return=${encodeURIComponent(encodeURIComponent(returnUrl))}${idpParam}`
}

export function isSigningIn (): boolean {
  const path = window.location.pathname
  return path.includes('/signin') || path.includes('/signin-redirect') || path.includes('/signin-redirect-full')
}

export function isSigningOut (): boolean {
  const path = window.location.pathname
  return path.includes('/signout')
}
