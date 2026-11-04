import { EntityTypes, NrRequestActionCodes } from '@/enums'
import { RequestActionMappingI } from '@/interfaces'

// maps request_action_cd (key) to array of allowable entities (value)
// { [request_action_cd]: entity_type_cd[] }
export const BcMapping: RequestActionMappingI = {
  // Amalgamate
  AML: [
    EntityTypes.CR,
    EntityTypes.UL,
    EntityTypes.CC,
    EntityTypes.CP,
    EntityTypes.BC,
    EntityTypes.SO
  ],
  // Renew
  REN: [
    EntityTypes.CR,
    EntityTypes.CP,
    EntityTypes.CC,
    EntityTypes.UL,
    EntityTypes.FI,
    EntityTypes.BC,
    EntityTypes.SO
  ],
  // Restore
  REH: [
    EntityTypes.CR, // maps to BC Limited Company
    EntityTypes.CP,
    EntityTypes.CC,
    EntityTypes.UL, // maps to ULC
    EntityTypes.FI,
    EntityTypes.BC, // maps to Benefit Company
    EntityTypes.SO,
    EntityTypes.C,
    EntityTypes.CBEN,
    EntityTypes.CCC,
    EntityTypes.CUL
  ],
  // Change Name
  CHG: [
    EntityTypes.FR,
    EntityTypes.DBA,
    EntityTypes.CR,
    EntityTypes.UL,
    EntityTypes.GP,
    EntityTypes.LP,
    EntityTypes.LL,
    EntityTypes.CP,
    EntityTypes.BC,
    EntityTypes.CC,
    EntityTypes.SO,
    EntityTypes.PA,
    EntityTypes.FI,
    EntityTypes.PAR,
    EntityTypes.C,
    EntityTypes.CBEN,
    EntityTypes.CCC,
    EntityTypes.CUL
  ],
  // MVE = Continuation In
  MVE: [
    EntityTypes.CR, // will become CorpTypeCd.CONTINUE_IN
    EntityTypes.CC, // will become CorpTypeCd.CCC_CONTINUE_IN
    EntityTypes.CP,
    EntityTypes.UL, // will become CorpTypeCd.ULC_CONTINUE_IN
    EntityTypes.SO, // will becomes CorpTypeCd.CONT_IN_SOCIETY
    EntityTypes.BC // will become CorpTypeCd.BEN_CONTINUE_IN
  ]
}

export const XproMapping: RequestActionMappingI = {
  AML: [
    EntityTypes.XCP, // maps to Corp Type "XCP"
    EntityTypes.XCR // maps to Corp Type "XCR"
  ],
  ASSUMED: [
    EntityTypes.RLC, // maps to Corp Type "LLC"
    EntityTypes.XCR // maps to Corp Type "XCR"
  ],
  REN: [
    EntityTypes.RLC, // maps to Corp Type "LLC"
    EntityTypes.XCP, // maps to Corp Type "XCP"
    EntityTypes.XCR // maps to Corp Type "XCR"
  ],
  REH: [
    EntityTypes.RLC, // maps to Corp Type "LLC"
    EntityTypes.XCP, // maps to Corp Type "XCP"
    EntityTypes.XCR, // maps to Corp Type "EXTRA_PRO_A"
    EntityTypes.XSO // maps to Corp Type "XS"
  ],
  CHG: [
    EntityTypes.RLC, // maps to Corp Type "LLC"
    EntityTypes.XCP, // maps to Corp Type "XCP"
    EntityTypes.XCR, // maps to Corp Type "EXTRA_PRO_A"
    EntityTypes.XLL, // maps to Corp Type "XL"
    EntityTypes.XLP, // maps to Corp Type "XP"
    EntityTypes.XSO // maps to Corp Type "XS"
  ]
}

/** Request actions that require business lookup. */
export const BusinessLookupRequestActions = [
  NrRequestActionCodes.CHANGE_NAME,
  NrRequestActionCodes.CONVERSION,
  NrRequestActionCodes.RESTORE
]

/** Entity types that require business lookup. */
export const BusinessLookupEntityTypes = [
  EntityTypes.A,
  EntityTypes.BC, // Benefit Company
  EntityTypes.BEN, // invalid?
  EntityTypes.C,
  EntityTypes.CBEN,
  EntityTypes.CC,
  EntityTypes.CCC,
  EntityTypes.CUL,
  EntityTypes.CP,
  EntityTypes.CR, // BC Limited Company
  EntityTypes.FR, // Sole Proprietorship
  EntityTypes.GP,
  EntityTypes.LLC,
  EntityTypes.LP,
  EntityTypes.PA,
  EntityTypes.PAR,
  EntityTypes.SO,
  EntityTypes.UL,
  EntityTypes.XCP,
  EntityTypes.XCR,
  EntityTypes.XL,
  EntityTypes.XP,
  EntityTypes.XSO,
  EntityTypes.XUL
]

/** Entity types that support the numbered company option. */
export const NumberedEntityTypes = [
  EntityTypes.BC, // Benefit Company
  EntityTypes.CC,
  EntityTypes.CR, // BC Limited Company
  EntityTypes.UL,
  EntityTypes.C,
  EntityTypes.CBEN,
  EntityTypes.CCC,
  EntityTypes.CUL
]
