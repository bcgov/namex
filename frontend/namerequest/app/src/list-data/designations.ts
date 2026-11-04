import { EntityTypes } from '@/enums'
import { DesignationI } from '@/interfaces'

const CorporateDesignations: DesignationI = {
  words: [
    'CORP.',
    'CORPORATION',
    'INC.',
    'INCORPORATED',
    'LIMITED',
    'LTD.',
    'INCORPOREE',
    'LIMITEE',
    'LTEE'
  ],
  end: true
}

const CooperativeDesignations: DesignationI = {
  words: [
    'CO-OP',
    'CO-OPERATIVE',
    'COOP',
    'COOPERATIVE'
  ],
  end: false
}

export const Designations = {
  BC: CorporateDesignations,
  C: CorporateDesignations, // continued in BC Limited Company
  CBEN: CorporateDesignations, // continued in Benefit Company
  CC: {
    words: [
      'CCC',
      'COMMUNITY CONTRIBUTION COMPANY',
      ...CorporateDesignations.words
    ],
    end: true
  },
  CCC: { // continued in Community Contribution Company
    words: [
      'CCC',
      'COMMUNITY CONTRIBUTION COMPANY',
      ...CorporateDesignations.words
    ],
    end: true
  },
  CP: CooperativeDesignations,
  CR: CorporateDesignations,
  CUL: { // continued in Unlimited Liability Company
    words: [
      'ULC',
      'UNLIMITED LIABILITY COMPANY'
    ],
    end: true
  },
  DBA: {
    words: [],
    end: false
  },
  FI: {
    words: [],
    end: false
  },
  FR: {
    words: [],
    end: false
  },
  GP: {
    words: [],
    end: false
  },
  LL: {
    words: [
      'LIMITED LIABILITY PARTNERSHIP',
      'LLP',
      'SENCRL',
      'SRL',
      'SOCIETE A RESPONSABILITE LIMITEE',
      'SOCIETE EN NOM COLLECTIF A RESPONSABILITE LIMITEE'
    ],
    end: true
  },
  LP: {
    words: ['LIMITED PARTNERSHIP'],
    end: true
  },
  PA: {
    words: [],
    end: false
  },
  PAR: {
    words: [],
    end: false
  },
  RLC: {
    words: [
      'L.L.C.',
      'LIMITED LIABILITY CO.',
      'LIMITED LIABILITY COMPANY',
      'LLC'
    ],
    end: true
  },
  SO: {
    words: [
      'ASSOCIATION',
      'ASSN.',
      'CHAMBER OF COMMERCE',
      'CHURCH',
      'EGLISE',
      'CLUB',
      'CHRISTIAN SCHOOL',
      'FELLOWSHIP',
      'FOUNDATION',
      'FONDATION',
      'GUILD',
      'PARISH',
      'SOCIETY',
      'SOCIETE',
      'WATERSHED'
    ],
    end: false
  },
  UL: {
    words: [
      'ULC',
      'UNLIMITED LIABILITY COMPANY'
    ],
    end: true
  },
  XCP: CooperativeDesignations,
  XCR: CorporateDesignations
}

function getAllDesignations () {
  const output = []
  for (const entity in Designations) {
    for (const word of Designations[entity].words) {
      if (!output.includes(word)) {
        output.push(word)
      }
    }
  }
  return output
}

// a string[] containing each designation code used in namex
// eg. [ 'CR', 'BC', 'CCC', etc... ]
export const AllDesignationsList = getAllDesignations()

/**
 * Validate Designation in name
 */
const ValidDesignationInFirmName = [
  'CHURCH',
  'EGLISE',
  'CLUB',
  'CHRISTIAN SCHOOL',
  'FELLOWSHIP',
  'PARISH',
  'WATERSHED',
  'FOUNDATION',
  'FONDATION',
  'GUILD'
]

function getInvalidFirmDesignations () {
  const excludeWords = new Set(
    ValidDesignationInFirmName.flatMap(word => [word, word.replace(/\./g, '')])
  )

  // Get all designations and ensure both original & "dotless" versions exist
  const allDesignation = new Set<string>(
    getAllDesignations().flatMap(word => [word, word.replace(/\./g, '')])
  )

  // Convert Set to an array to filter it
  return [...allDesignation].filter(word => !excludeWords.has(word))
}

const InvalidDesignations = {
  FR: getInvalidFirmDesignations,
  DBA: getInvalidFirmDesignations,
  GP: getInvalidFirmDesignations,
  LP: getInvalidFirmDesignations,
  LL: getInvalidFirmDesignations
}

/**
 * Checks if the given name contains any invalid designations at the end.
 * Returns an error message if an invalid designation is found, otherwise returns null.
 *
 * @param entityTypeCd - The entity type code.
 * @param name - The name to be checked.
 * @returns An error message if an invalid designation is found, otherwise null.
 */
export function checkInvalidDesignation (entityTypeCd: string | EntityTypes, name: string): string | null {
  // Return null if name is empty or if there are no invalid designations for the given entity type
  if (!name || !InvalidDesignations[entityTypeCd]) {
    return null
  }

  // Get the list of invalid designations for the given entity type
  const invalidDesignationList = InvalidDesignations[entityTypeCd]()
  if (!invalidDesignationList) {
    return null
  }

  // Trim the name to remove any trailing spaces
  const trimmedName = name.trim()

  // Check if any invalid designation appears at the end of the name
  const foundWord = invalidDesignationList.find((word: string) => {
    const escapedWord = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    const regex = new RegExp(`\\b${escapedWord.toUpperCase()}$`, 'i')
    return regex.test(trimmedName.toUpperCase())
  })

  // Return an error message if an invalid designation is found
  if (foundWord) {
    return `The designation "${foundWord}" cannot be used in the name`
  }

  // Return null if no invalid designation is found
  return null
}
