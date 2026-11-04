import { NameCheckErrorType } from '@/enums'

export interface NameCheckErrorI {
  [NameCheckErrorType.ERROR_DESIGNATION]: boolean
  [NameCheckErrorType.ERROR_EXACT]: boolean
  [NameCheckErrorType.ERROR_RESTRICTED]: boolean
  [NameCheckErrorType.ERROR_SIMILAR]: boolean
  [NameCheckErrorType.ERROR_STRUCTURE]: boolean
}
