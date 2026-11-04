import { ConditionalInstructionI } from './conditional-instructions'
export interface ParsedRestrictedResponseIF {
  conditionalInstructions: Array<ConditionalInstructionI>
  conditionalWords: Array<string>
  restrictedWords: Array<string>
}
