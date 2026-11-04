import { Location } from '@/enums'

// blurbs strings correspond to:
//   1. NEW
//   2. MVE
//   3. REH
//   4. AML
//   5. CHG
//   6. CNV

export const Locations: any[] = [
  {
    text: 'British Columbia',
    value: Location.BC,
    blurbs: [
      `Your business does not currently exist anywhere (i.e., it is a new business).`,
      ``,
      `The business that needs to be restored or reinstated is based in BC.`,
      `One or more of the businesses that have amalgamated are incorporated in BC.`,
      `Your existing business is incorporated or registered in BC.`
    ]
  },
  {
    text: 'Extraprovincial (Canada based)',
    altText: 'Canadian',
    value: Location.CA,
    blurbs: [
      `Your existing business is currently located in any Province or Territory other than BC.`,
      `Your existing business is currently located in any Province or Territory other than BC.`,
      `The business that needs to be restored or reinstated is based in Canada and was
          extraprovincially registered in BC.`,
      `One or more of the businesses that have amalgamated are Canadian and are extraprovincially
           registered in BC.`,
      `Your existing Canada based business is extraprovincially registered in BC and has changed its name in the
           home jurisdiction.`
    ]
  },
  {
    text: 'Extraprovincial (Internationally based)',
    altText: 'International',
    value: Location.IN,
    blurbs: [
      `Your existing business is currently located outside of Canada.`,
      `Your existing business is currently located outside of Canada.`,
      `The business that needs to be restored or reinstated is internationally based and was
          extraprovincially registered in BC.`,
      `One or more of the businesses that have amalgamated are internationally based and are
          extraprovincially registered in BC.`,
      `Your existing internationally based business is extraprovincially registered in BC and has changed its name
           in the home jurisdiction.`
    ]
  }
]
