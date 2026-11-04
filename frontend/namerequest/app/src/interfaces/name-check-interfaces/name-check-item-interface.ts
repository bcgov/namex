import { NameCheckErrorType, NameCheckItemType } from '@/enums'
import { ConflictListItemI } from './conflict-list-item'

export interface NameCheckItemIF {
  count: number,
  expandedInfoBlock1?: Array<string>,
  expandedInfo1: string,
  expandedInfo2: string,
  expandedInfo3?: string,
  expandedInfo4?: string,
  expandedList: Array<ConflictListItemI>,
  expandLabel: {
    open: string,
    closed: string
  },
  icon: string,
  iconColor: string,
  info?: NameCheckErrorType | NameCheckItemType,
  problem: string,
  words: Array<string>
}
