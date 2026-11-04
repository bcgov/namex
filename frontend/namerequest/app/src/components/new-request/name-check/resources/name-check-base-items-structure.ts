import { NameCheckErrorType, NameCheckItemType } from '@/enums'

export const baseItemsStructure = {
  [NameCheckItemType.CONFLICTS_CONDITIONAL]: {
    icon: 'mdi-alert',
    iconColor: 'caution',
    problem: 'You may need consent to use the following words:',
    words: [],
    expandedInfo1: 'Names that include well-known names (trademarks and trade names), ' +
    'names of public figures, or reference to the government, BC, the Crown or Royal ' +
    'Family, will not be allowed without the written consent of the holder. ' +
    'Consider revising your name unless you can obtain consent.',
    expandedInfo2: null,
    expandedList: null,
    expandLabel: {
      closed: 'Read More',
      open: 'Read Less'
    },
    count: null
  },
  [NameCheckItemType.DESCRIPTIVE_MISSING]: {
    icon: 'mdi-alert',
    iconColor: 'caution',
    problem: 'Ensure there is a <b>descriptive</b> element in your business name',
    words: [],
    expandedInfo1: 'Names in BC are required to contain a descriptive word ' +
    '(or words) that describes the business category or the type of business. ' +
    'For example:',
    expandedInfoBlock1: [
      'Fernie <b>Brake</b> Shop Ltd.',
      'Kamloops <b>Stationery</b> Ltd.',
      'Gentle Rain Fellowship of <b>Faith</b> Society',
      'Gentle <b>Teaching</b> International Society'
    ],
    expandedInfo2: 'A descriptive element is not required for names that ' +
    'include a made-up word with a geographical location (e.g. Altrex Canada Ltd.).',
    expandedList: null,
    expandLabel: {
      closed: 'Read More',
      open: 'Read Less'
    },
    count: null
  },
  [NameCheckItemType.DESIGNATIONS_CHECK_USE]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'Check corporate designation usage:',
    words: [],
    expandedInfo1: 'A name cannot contain the same designation word ' +
    'twice. A name can contain more than one designation word if the ' +
    'words are different, e.g., if you have choosen "Inc." for the ' +
    'desgination at the end of your name you cannot use "Inc." elsewhere ' +
    'in the name, but you can use "Company" elsewhere in the name.',
    expandedInfo2: null,
    expandedList: null,
    expandLabel: {
      closed: 'Read More',
      open: 'Read Less'
    },
    count: null
  },
  [NameCheckItemType.DESIGNATIONS_CHECK_USE_CP]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'Check corporate designation usage:',
    words: [],
    expandedInfo1: 'A Cooperative name should ' +
    'include (but not start with) one of the following ' +
    'phrases: CO-OP, CO-OPERATIVE, COOP, COOPERATIVE',
    expandedInfo2: null,
    expandedList: null,
    expandLabel: {
      closed: 'Read More',
      open: 'Read Less'
    },
    count: null
  },
  [NameCheckItemType.DESIGNATIONS_CHECK_USE_CCC]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'Check corporate designation usage:',
    words: [],
    expandedInfo1: 'A Community Contribution ' +
    'Company name must include (but not start with) one of ' +
    'the following phrases: CCC, COMMUNITY CONTRIBUTION COMPANY',
    expandedInfo2: null,
    expandedList: null,
    expandLabel: {
      closed: 'Read More',
      open: 'Read Less'
    },
    count: null
  },
  [NameCheckItemType.DESIGNATIONS_CHECK_USE_PROP]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'Check corporate designation usage:',
    words: [],
    expandedInfo1: 'A Sole proprietorship, ' +
    'Partnership, or Doing-Business-As (DBA) cannot ' +
    'use a corporate designation (Inc., Incorporated, ' +
    'LTD, Limited, etc.) but it can use Company or Co. ' +
    'in the business name. Note: A designation is not ' +
    'required for a Sole proprietorship, Partnership, ' +
    'or Doing-Business-As (DBA).',
    expandedInfo2: null,
    expandedList: null,
    expandLabel: {
      closed: 'Read More',
      open: 'Read Less'
    },
    count: null
  },
  [NameCheckItemType.DESIGNATIONS_MISMATCHED]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'Check corporate designation usage:',
    words: [],
    expandedInfo1: 'A name cannot contain designations for different types ' +
    'of business. Any designation in the name (e.g., "Company")  must ' +
    'match the business type designation at the end (e.g., "Inc.").',
    expandedInfo2: null,
    expandedList: null,
    expandLabel: {
      closed: 'Read More',
      open: 'Read Less'
    },
    count: null
  },
  [NameCheckItemType.DESIGNATIONS_MISPLACED]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'Check corporate designation usage:',
    words: [],
    expandedInfo1: 'A name cannot contain the same designation word twice. ' +
    'A name can contain more than one designation word if the words are ' +
    'different, e.g., if you have choosen "Inc." for the desgination at ' +
    'the end of your name you cannot use "Inc." elsewhere in the name, but ' +
    'you can use "Company" elsewhere in the name.',
    expandedInfo2: null,
    expandedList: null,
    expandLabel: {
      closed: 'Read More',
      open: 'Read Less'
    },
    count: null
  },
  [NameCheckItemType.DESIGNATIONS_MISSING]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'Ensure there is a <b>corporate designation</b> in your business name',
    words: [],
    expandedInfo1: '<i>TBD</i>',
    expandedInfo2: null,
    expandedList: null,
    expandLabel: {
      closed: 'Read More',
      open: 'Read Less'
    },
    count: null
  },
  [NameCheckItemType.DESIGNATIONS_MISSING_CP]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'Ensure there is a <b>corporate designation</b> in your business name',
    words: [],
    expandedInfo1: 'A Cooperative name should ' +
    'include (but not start with) one of the following ' +
    'phrases: CO-OP, CO-OPERATIVE, COOP, COOPERATIVE',
    expandedInfo2: null,
    expandedList: null,
    expandLabel: {
      closed: 'Read More',
      open: 'Read Less'
    },
    count: null
  },
  [NameCheckItemType.DESIGNATIONS_MISSING_CCC]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'Ensure there is a <b>corporate designation</b> in your business name',
    words: [],
    expandedInfo1: 'A Community Contribution ' +
    'Company name must include (but not start with) one of ' +
    'the following phrases: CCC, COMMUNITY CONTRIBUTION COMPANY',
    expandedInfo2: null,
    expandedList: null,
    expandLabel: {
      closed: 'Read More',
      open: 'Read Less'
    },
    count: null
  },
  [NameCheckItemType.DISTINCTIVE_MISSING]: {
    icon: 'mdi-alert',
    iconColor: 'caution',
    problem: 'Ensure there is a <b>distinctive</b> element in your business name',
    words: [],
    expandedInfo1: 'Names in BC are required to contain a distinctive word ' +
    '(or words) that makes the name unique. Words that can make a name unique ' +
    'include: an individual\'s name, a geographical location, a coined or ' +
    'made-up word, or an acronym.',
    expandedInfo2: null,
    expandedList: null,
    expandLabel: {
      closed: 'Read More',
      open: 'Read Less'
    },
    count: null
  },
  [NameCheckErrorType.ERROR_DESIGNATION]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'There was an issue checking designation in your name',
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
    info: NameCheckErrorType.ERROR_DESIGNATION
  },
  [NameCheckErrorType.ERROR_RESTRICTED]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'There was an issue checking restricted words in your name',
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
    info: NameCheckErrorType.ERROR_RESTRICTED
  },
  [NameCheckErrorType.ERROR_STRUCTURE]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'There was an issue checking descriptive/distinctive words in your name',
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
    info: NameCheckErrorType.ERROR_STRUCTURE
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
    problem: 'No name structure issues have been found.',
    words: [],
    expandedInfo1: null,
    expandedInfo2: null,
    expandedList: null,
    expandLabel: null,
    count: null
  },
  [NameCheckItemType.NUMBERS_CHECK_USE]: {
    icon: 'mdi-alert',
    iconColor: 'caution',
    problem: 'Ensure you are using numbers correctly:',
    words: [],
    expandedInfo1: 'Numerals may be used in company names as the distinctive element. ' +
    'A year may be used in a name provided that it is the year of incorporation, ' +
    'amalgamation, change of name, or registration.',
    expandedInfo2: 'For example:<br />Pacific Enterprises (1997) Ltd.',
    expandedList: null,
    expandLabel: {
      closed: 'Read More',
      open: 'Read Less'
    },
    count: null
  },
  [NameCheckItemType.RESTRICTED]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'Consider removing the following word(s):',
    words: [],
    expandedInfo1: 'This name appears to contain one or more words that are not ' +
    'available for use by the public. <br><b>Note:</b> Names involving a vulgar expression, ' +
    'obscene words or connotation, racial, physical or sexual slur will be rejected.',
    expandedInfo2: null,
    expandedList: null,
    expandLabel: {
      closed: 'Read More',
      open: 'Read Less'
    },
    count: null
  },
  [NameCheckItemType.SPECIAL_CHARACTERS]: {
    icon: 'mdi-alert-octagon',
    iconColor: 'red darken-2',
    problem: 'Please remove the following character(s):',
    words: [],
    expandedInfo1: 'Only the following special characters may be used in a ' +
    'business name: <b>/ [ ] ^ * + - = & ( ) . , ” ’ # @ ! ? ; :</b>',
    expandedInfo2: null,
    expandedList: null,
    expandLabel: {
      closed: 'Read More',
      open: 'Read Less'
    },
    count: null
  }
}
