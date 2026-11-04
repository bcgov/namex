import { NrRequestActionCodes } from '@/enums'
import { RequestActionsI } from '@/interfaces/models'

/** All the request actions - some are group headers and others are selectable items. */
export const RequestActions: RequestActionsI[] = [
  {
    isHeader: true,
    group: 0,
    text: 'For businesses that do not exist yet',
    icon: 'mdi-briefcase-plus'
  },
  {
    group: 0,
    text: 'Start a new BC-based business',
    subtext: 'Incorporation or Registration',
    shortDesc: 'New Request',
    value: NrRequestActionCodes.NEW_BUSINESS
  },
  {
    isHeader: true,
    group: 1,
    text: 'For businesses that already exist outside BC',
    icon: 'mdi-earth'
  },
  {
    group: 1,
    text: 'Register a business in BC that is incorporated in another jurisdiction',
    subtext: 'Extraprovincial Registration',
    shortDesc: 'New Request',
    value: NrRequestActionCodes.NEW_BUSINESS
  },
  {
    group: 1,
    text: 'End business registration in another jurisdiction and transfer to BC',
    subtext: 'Continuation In',
    shortDesc: 'Move Request',
    value: NrRequestActionCodes.MOVE
  },
  {
    isHeader: true,
    group: 2,
    text: 'For businesses that are already incorporated or registered in BC',
    icon: 'mdi-domain'
  },
  {
    group: 2,
    text: 'Change the name of an existing BC business',
    subtext: 'Name Change',
    shortDesc: 'Change of Name Request',
    value: NrRequestActionCodes.CHANGE_NAME
  },
  {
    group: 2,
    text: 'Combine two or more businesses in BC using a new name',
    subtext: 'Amalgamation',
    shortDesc: 'Amalgamation Request',
    value: NrRequestActionCodes.AMALGAMATE
  },
  {
    group: 2,
    text: 'Alter from one BC business type to another',
    subtext: 'Alteration',
    shortDesc: 'Conversion Request',
    value: NrRequestActionCodes.CONVERSION
  },
  {
    group: 2,
    text: 'Reactivate a BC or Extraprovincial company',
    subtext: 'Restoration or Reinstatement',
    shortDesc: 'Restore-Historical Request',
    value: NrRequestActionCodes.RESTORE
  }
  // COMMENTED OUT FOR FUTURE IMPLEMENTATION
  // {
  //   group: 2,
  //   text: 'Restore a business that has been dissolved or cancelled',
  //   subtext: 'Restoration or Reinstatement',
  //   shortDesc: 'Restore-New Request',
  //   value: NrRequestActionCodes.RENEW
  // }
]
