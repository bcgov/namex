import { NameCheckErrorType, NameCheckItemType } from '@/enums'

export const baseItemsConflicts = {
  [NameCheckErrorType.ERROR_EXACT]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'There was an issue checking exact matches against your name',
    words: null,
    expandExtraInfo: false,
    expandedInfo1: '',
    expandedInfo2: null,
    expandedList: [],
    expandLabel: {
      closed: 'View Details',
      open: 'Hide Details'
    },
    count: 0,
    info: NameCheckErrorType.ERROR_EXACT
  },
  [NameCheckErrorType.ERROR_SIMILAR]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'There was an issue checking similar matches against your name',
    words: null,
    expandExtraInfo: false,
    expandedInfo1: '',
    expandedInfo2: null,
    expandedList: [],
    expandLabel: {
      closed: 'View Details',
      open: 'Hide Details'
    },
    count: 0,
    info: NameCheckErrorType.ERROR_SIMILAR
  },
  [NameCheckItemType.EXACT_MATCH]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'This <b>exact name</b> is currently in use or reserved for use by a BC corporation',
    words: null,
    expandExtraInfo: false,
    expandedInfo1: 'This exact name is currently in use or reserved for use. A name will not be approved if there is ' +
    'an existing business  or approved name request with the exact same name.',
    expandedInfo2: null,
    expandedList: [],
    expandLabel: {
      closed: 'View Details',
      open: 'Hide Details'
    },
    count: 0,
    info: NameCheckItemType.EXACT_MATCH
  },
  [NameCheckItemType.EXACT_MATCH_XPRO]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'This <b>exact name</b> is currently in use or reserved for use by a BC corporation',
    words: null,
    expandExtraInfo: false,
    expandedInfo1: 'This exact name is currently in use or reserved for use. You must use (assume) a new name ' +
    'unless you can obtain consent to use this name.',
    expandedInfo2: 'You will be able to enter up to two Assumed Name ' +
    'choices as part of the name request submission process. Assumed ' +
    'names must be reviewed by Registries staff.',
    expandedInfo3: '<b>To proceed, select "Submit this Name for Review".</b>',
    expandedList: [],
    expandLabel: {
      closed: 'View Details',
      open: 'Hide Details'
    },
    count: 0,
    info: NameCheckItemType.EXACT_MATCH_XPRO
  },
  [NameCheckItemType.LOADING]: {
    count: 0,
    expandedInfo1: null,
    expandedInfo2: null,
    expandedList: null,
    expandLabel: {
      open: null,
      closed: null
    },
    icon: null,
    iconColor: null,
    problem: null,
    words: null,
    info: NameCheckItemType.LOADING
  },
  [NameCheckItemType.NO_ISSUES]: {
    icon: null,
    iconColor: null,
    info: NameCheckItemType.NO_ISSUES,
    problem: 'No similar names have been found.',
    words: [],
    expandedInfo1: null,
    expandedInfo2: null,
    expandedList: null,
    expandLabel: null,
    count: null
  },
  [NameCheckItemType.SIMILAR_MATCH]: {
    icon: 'mdi-alert',
    iconColor: 'caution',
    problem: '<b>Similar names</b> are currently in use or reserved for use by a BC corporation',
    words: null,
    expandExtraInfo: false,
    expandedInfo1: 'custom text for similarMatch in component',
    expandedInfo2: null,
    expandedList: [],
    expandLabel: {
      closed: 'View Details',
      open: 'Hide Details'
    },
    count: 0,
    info: NameCheckItemType.SIMILAR_MATCH
  },
  [NameCheckItemType.SIMILAR_MATCH_XPRO]: {
    icon: 'mdi-alert',
    iconColor: 'caution',
    problem: '<b>Similar names</b> are currently in use or reserved for use by a BC corporation',
    words: null,
    expandExtraInfo: false,
    expandedInfo1: 'No exact matches were found for your name, ' +
    'but you should review the above list to help determine if ' +
    'there is a similar business name already in use or reserved in' +
    ' BC that might prevent your name from being approved.',
    expandedInfo2: 'If an existing or reserved name is too similar to your ' +
    'name you will be required to use (assume) a new name in BC. ' +
    'You will be notified as part of the review process if you ' +
    'need to use an assumed name, or if consent is required to ' +
    'use your preferred name.',
    expandedInfo3: 'You will be able to enter up to two Assumed ' +
    'Name choices as part of the name request submission process, ' +
    'and it is recommended that you enter two Assumed Name choices. ' +
    'Assumed names must be reviewed by Registries staff.',
    expandedInfo4: '<b>To proceed, select "Submit this Name for Review".</b>',
    expandedList: [],
    expandLabel: {
      closed: 'View Details',
      open: 'Hide Details'
    },
    count: 0,
    info: NameCheckItemType.SIMILAR_MATCH_XPRO
  }
}
