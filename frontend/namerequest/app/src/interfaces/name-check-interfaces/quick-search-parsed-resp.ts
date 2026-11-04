import { ConflictListItemI } from './conflict-list-item'
import { ConditionalInstructionI } from './conditional-instructions'

export interface QuickSearchParsedRespI {
  exactNames: Array<ConflictListItemI>,
  synonymNames: Array<ConflictListItemI>,
  restrictedWords: Array<string>,
  conditionalWords: Array<string>,
  conditionalInstructions: Array<ConditionalInstructionI>
}
