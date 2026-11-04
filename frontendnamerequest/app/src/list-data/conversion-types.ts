import { EntityTypes, NrRequestTypeCodes } from '@/enums'
import { ConversionTypesI } from '@/interfaces/models'

export const ConversionTypes: ConversionTypesI[] = [
  //
  // Regular Businesses
  //
  {
    desc: 'Limited Company to a Benefit Company',
    text: 'Limited Company to a Benefit Company',
    entity_type_cd: EntityTypes.BC, // Benefit Company (namex)
    origin_entity_type_cd: EntityTypes.BC, // BC Limited (lear)
    blurbs: [
      'Alter business type from a limited company to a benefit company.'
    ],
    value: NrRequestTypeCodes.CONVERT_BC_TO_BEN,
    shortlist: false
  },
  {
    desc: 'Limited Company to a Community Contribution Company',
    text: 'Limited Company to a Community Contribution Company',
    entity_type_cd: EntityTypes.CC, // CCC (namex)
    origin_entity_type_cd: EntityTypes.BC, // BC Limited (lear)
    blurbs: [
      'Alter business type from a limited company to a community contribution company.'
    ],
    value: NrRequestTypeCodes.CONVERT_BC_TO_CCC,
    rank: 2,
    shortlist: true
  },
  {
    desc: 'Limited Company to an Unlimited Liability Company',
    text: 'Limited Company to an Unlimited Liability Company',
    entity_type_cd: EntityTypes.UL, // ULC (namex)
    origin_entity_type_cd: EntityTypes.BC, // BC Limited (lear)
    blurbs: [
      'Alter business type from a limited company to an unlimited liability company.'
    ],
    value: NrRequestTypeCodes.CONVERT_BC_TO_ULC,
    rank: 1,
    shortlist: true
  },
  {
    desc: 'Benefit Company to a Limited Company',
    text: 'Benefit Company to a Limited Company',
    entity_type_cd: EntityTypes.CR, // BC Limited (namex)
    origin_entity_type_cd: EntityTypes.BEN, // Benefit Company (lear)
    blurbs: [
      'Alter business type from a benefit company to a limited company.'
    ],
    value: NrRequestTypeCodes.CONVERT_BEN_TO_BC,
    shortlist: false
  },
  {
    desc: 'Benefit Company to a Community Contribution Company',
    text: 'Benefit Company to a Community Contribution Company',
    entity_type_cd: EntityTypes.CC, // CCC (namex)
    origin_entity_type_cd: EntityTypes.BEN, // Benefit Company (lear)
    blurbs: [
      'Alter business type from a benefit company to a community contribution company.'
    ],
    value: NrRequestTypeCodes.CONVERT_BEN_TO_CCC,
    shortlist: false
  },
  {
    desc: 'Unlimited Liability Company to a Limited Company',
    text: 'Unlimited Liability Company to a Limited Company',
    entity_type_cd: EntityTypes.CR, // BC Limited (namex)
    origin_entity_type_cd: EntityTypes.ULC, // ULC (lear)
    blurbs: [
      'Alter business type from an unlimited liability company to a limited company.'
    ],
    value: NrRequestTypeCodes.CONVERT_ULC_TO_BC,
    shortlist: false
  },
  {
    desc: 'Unlimited Liability Company to a Benefit Company',
    text: 'Unlimited Liability Company to a Benefit Company',
    entity_type_cd: EntityTypes.BC, // Benefit Company (namex)
    origin_entity_type_cd: EntityTypes.ULC, // ULC (lear)
    blurbs: [
      'Alter business type from an unlimited liability company to a benefit company.'
    ],
    value: NrRequestTypeCodes.CONVERT_ULC_TO_BEN,
    shortlist: false
  },
  //
  // Continued-in Businesses
  //
  {
    desc: 'Limited Company to a Benefit Company',
    text: 'Limited Company to a Benefit Company',
    entity_type_cd: EntityTypes.CBEN,
    origin_entity_type_cd: EntityTypes.C,
    blurbs: [
      'Alter business type from a limited company to a benefit company.'
    ],
    value: NrRequestTypeCodes.CONVERT_BC_TO_BEN,
    shortlist: false
  },
  {
    desc: 'Limited Company to a Community Contribution Company',
    text: 'Limited Company to a Community Contribution Company',
    entity_type_cd: EntityTypes.CCC,
    origin_entity_type_cd: EntityTypes.C,
    blurbs: [
      'Alter business type from a limited company to a community contribution company.'
    ],
    value: NrRequestTypeCodes.CONVERT_BC_TO_CCC,
    rank: 2,
    shortlist: true
  },
  {
    desc: 'Limited Company to an Unlimited Liability Company',
    text: 'Limited Company to an Unlimited Liability Company',
    entity_type_cd: EntityTypes.CUL,
    origin_entity_type_cd: EntityTypes.C,
    blurbs: [
      'Alter business type from a limited company to an unlimited liability company.'
    ],
    value: NrRequestTypeCodes.CONVERT_BC_TO_ULC,
    rank: 1,
    shortlist: true
  },
  {
    desc: 'Benefit Company to a Limited Company',
    text: 'Benefit Company to a Limited Company',
    entity_type_cd: EntityTypes.C,
    origin_entity_type_cd: EntityTypes.CBEN,
    blurbs: [
      'Alter business type from a benefit company to a limited company.'
    ],
    value: NrRequestTypeCodes.CONVERT_BEN_TO_BC,
    shortlist: false
  },
  {
    desc: 'Benefit Company to a Community Contribution Company',
    text: 'Benefit Company to a Community Contribution Company',
    entity_type_cd: EntityTypes.CCC,
    origin_entity_type_cd: EntityTypes.CBEN,
    blurbs: [
      'Alter business type from a benefit company to a community contribution company.'
    ],
    value: NrRequestTypeCodes.CONVERT_BEN_TO_CCC,
    shortlist: false
  },
  {
    desc: 'Unlimited Liability Company to a Limited Company',
    text: 'Unlimited Liability Company to a Limited Company',
    entity_type_cd: EntityTypes.C,
    origin_entity_type_cd: EntityTypes.CUL,
    blurbs: [
      'Alter business type from an unlimited liability company to a limited company.'
    ],
    value: NrRequestTypeCodes.CONVERT_ULC_TO_BC,
    shortlist: false
  },
  {
    desc: 'Unlimited Liability Company to a Benefit Company',
    text: 'Unlimited Liability Company to a Benefit Company',
    entity_type_cd: EntityTypes.CBEN,
    origin_entity_type_cd: EntityTypes.CUL,
    blurbs: [
      'Alter business type from an unlimited liability company to a benefit company.'
    ],
    value: NrRequestTypeCodes.CONVERT_ULC_TO_BEN,
    shortlist: false
  }
]
