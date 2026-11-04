/** The request type codes that this application uses (retrieved from the request types JSON file)
 * and the ones that the backend uses are different for some NR types. This file contains utlities for translating
 * between the two.
 */
import {
  RequestTypeCode,
  RequestActionCode,
  EntityTypeCode,
} from '~/enums/codes'

type RequestTypeMap = { [key in RequestTypeCode]?: RequestTypeCode }

const NORMAL_TO_AMALGAMATED_MAP: RequestTypeMap = {
  [RequestTypeCode.CR]: RequestTypeCode.ACR,
  [RequestTypeCode.XCR]: RequestTypeCode.XACR,
  [RequestTypeCode.CP]: RequestTypeCode.ACP,
  [RequestTypeCode.CC]: RequestTypeCode.ACC,
}
const AMALGAMATED_TO_NORMAL_MAP = Object.fromEntries(
  Object.entries(NORMAL_TO_AMALGAMATED_MAP).map((e) => e.reverse())
)

const SOLE_PROP_TO_GP_MAP: RequestTypeMap = {
  [RequestTypeCode.FR]: RequestTypeCode.GP,
  [RequestTypeCode.CFR]: RequestTypeCode.CGP,
}
const GP_TO_SOLE_PROP_MAP = Object.fromEntries(
  Object.entries(SOLE_PROP_TO_GP_MAP).map((e) => e.reverse())
)

export function toMappedRequestType(
  requestType: RequestTypeCode,
  action: RequestActionCode,
  entityType: EntityTypeCode
) {
  // Map amalgamation split requests
  if (action === RequestActionCode.AML) {
    const newType = NORMAL_TO_AMALGAMATED_MAP[requestType]
    if (newType) return newType
  }
  // Map sole general partnership split requests
  if (entityType === EntityTypeCode.GP) {
    const newType = SOLE_PROP_TO_GP_MAP[requestType]
    if (newType) return newType
  }
  return requestType
}

export function fromMappedRequestType(
  requestType: RequestTypeCode,
  action: RequestActionCode
) {
  // Map amalgamation split requests
  if (action === RequestActionCode.AML) {
    const newType = AMALGAMATED_TO_NORMAL_MAP[requestType]
    if (newType) {
      return newType
    }
  }
  // Map sole general partnership split requests
  const newType = GP_TO_SOLE_PROP_MAP[requestType]
  if (newType) return newType
  return requestType
}
