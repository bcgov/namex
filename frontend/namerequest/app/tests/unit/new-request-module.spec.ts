// import store from '@/store/new-request-module'

// Testing behavior of getters.showCorpNum: (state) => return value
describe('New Request module', () => {
  it('is an empty test', () => {})
  // /* -- SETUP CONSTANTS FOR TESTING -- */
  // function setState ({ entityType, requestAction, location, jurisdiction }) {
  //   store.mutateEntityType(entityType)
  //   store.mutateRequestAction(requestAction)
  //   store.mutateLocation(location)
  //   store.mutateXproJurisdiction(jurisdiction)
  // }
  // const spreadSheetData = [
  //   { number: 1, location: 'BC', requestAction: 'NEW', entityType: 'FR', showCorpNum: 'N/A' },
  //   { number: 2, location: 'BC', requestAction: 'NEW', entityType: 'CR', showCorpNum: 'N/A' },
  //   { number: 3, location: 'BC', requestAction: 'NEW', entityType: 'CR', showCorpNum: 'N/A' },
  //   { number: 4, location: 'BC', requestAction: 'NEW', entityType: 'UL', showCorpNum: 'N/A' },
  //   { number: 5, location: 'BC', requestAction: 'NEW', entityType: 'BC', showCorpNum: 'N/A' },
  //   { number: 6, location: 'BC', requestAction: 'NEW', entityType: 'GP', showCorpNum: 'N/A' },
  //   { number: 7, location: 'BC', requestAction: 'NEW', entityType: 'LP', showCorpNum: 'N/A' },
  //   { number: 8, location: 'BC', requestAction: 'NEW', entityType: 'LL', showCorpNum: 'N/A' },
  //   { number: 9, location: 'BC', requestAction: 'NEW', entityType: 'CP', showCorpNum: 'N/A' },
  //   { number: 10, location: 'BC', requestAction: 'NEW', entityType: 'CC', showCorpNum: 'N/A' },
  //   { number: 12, location: 'BC', requestAction: 'NEW', entityType: 'PA', showCorpNum: 'N/A' },
  //   { number: 13, location: 'BC', requestAction: 'NEW', entityType: 'FI', showCorpNum: 'N/A' },
  //   { number: 14, location: 'BC', requestAction: 'CHG', entityType: 'FR', showCorpNum: 'COLIN' },
  //   { number: 15, location: 'BC', requestAction: 'CHG', entityType: 'DBA', showCorpNum: 'COLIN' },
  //   { number: 16, location: 'BC', requestAction: 'CHG', entityType: 'CR', showCorpNum: 'COLIN' },
  //   { number: 17, location: 'BC', requestAction: 'CHG', entityType: 'UL', showCorpNum: 'COLIN' },
  //   { number: 18, location: 'BC', requestAction: 'CHG', entityType: 'BC', showCorpNum: 'COLIN' },
  //   { number: 19, location: 'BC', requestAction: 'CHG', entityType: 'GP', showCorpNum: 'COLIN' },
  //   { number: 20, location: 'BC', requestAction: 'CHG', entityType: 'LP', showCorpNum: 'COLIN' },
  //   { number: 21, location: 'BC', requestAction: 'CHG', entityType: 'LL', showCorpNum: 'COLIN' },
  //   { number: 22, location: 'BC', requestAction: 'CHG', entityType: 'CP', showCorpNum: 'COLIN' },
  //   { number: 23, location: 'BC', requestAction: 'CHG', entityType: 'CC', showCorpNum: 'COLIN' },
  //   { number: 25, location: 'BC', requestAction: 'CHG', entityType: 'FI', showCorpNum: 'COLIN' },
  //   { number: 26, location: 'BC', requestAction: 'MVE', entityType: 'CR', showCorpNum: 'MRAS' },
  //   { number: 27, location: 'BC', requestAction: 'MVE', entityType: 'UL', showCorpNum: 'MRAS' },
  //   { number: 28, location: 'BC', requestAction: 'MVE', entityType: 'BC', showCorpNum: 'MRAS' },
  //   { number: 29, location: 'BC', requestAction: 'MVE', entityType: 'CC', showCorpNum: 'MRAS' },
  //   { number: 30, location: 'BC', requestAction: 'MVE', entityType: 'CP', showCorpNum: 'MRAS' },
  //   { number: 32, location: 'BC', requestAction: 'AML', entityType: 'UL', showCorpNum: 'COLIN' },
  //   { number: 33, location: 'BC', requestAction: 'AML', entityType: 'CR', showCorpNum: 'COLIN' },
  //   { number: 34, location: 'BC', requestAction: 'AML', entityType: 'BC', showCorpNum: 'COLIN' },
  //   { number: 35, location: 'BC', requestAction: 'AML', entityType: 'CC', showCorpNum: 'COLIN' },
  //   { number: 36, location: 'BC', requestAction: 'AML', entityType: 'CP', showCorpNum: 'COLIN' },
  //   { number: 37, location: 'BC', requestAction: 'CNV', entityType: 'UL', showCorpNum: 'COLIN' },
  //   { number: 38, location: 'BC', requestAction: 'CNV', entityType: 'CC', showCorpNum: 'COLIN' },
  //   { number: 39, location: 'BC', requestAction: 'CNV', entityType: 'BC', showCorpNum: 'COLIN' },
  //   { number: 40, location: 'BC', requestAction: 'CNV', entityType: 'CR', showCorpNum: 'COLIN' },
  //   { number: 41, location: 'BC', requestAction: 'REH', entityType: 'CR', showCorpNum: 'COLIN' },
  //   { number: 42, location: 'BC', requestAction: 'REN', entityType: 'UL', showCorpNum: 'COLIN' },
  //   { number: 43, location: 'BC', requestAction: 'REH', entityType: 'BC', showCorpNum: 'COLIN' },
  //   { number: 44, location: 'BC', requestAction: 'REN', entityType: 'CP', showCorpNum: 'COLIN' },
  //   { number: 45, location: 'BC', requestAction: 'REH', entityType: 'CC', showCorpNum: 'COLIN' },
  //   { number: 46, location: 'BC', requestAction: 'REN', entityType: 'FI', showCorpNum: 'COLIN' }
  // ]

  // const testJurisdictions = ['ALBERTA', 'SASKATCHEWAN', 'MANITOBA', 'ONTARIO', 'QUEBEC', 'NEW BRUNSWICK']

  // let testData = []
  // for (let row of spreadSheetData) {
  //   interface Obj {
  //     showCorpNum: any,
  //     xproJurisdiction: any
  //   }
  //   let obj: Partial<Obj> = { ...row }
  //   obj['showCorpNum'] = obj['showCorpNum'].toLowerCase()
  //   if (obj.showCorpNum === 'n/a') {
  //     obj.showCorpNum = false
  //     obj.xproJurisdiction = null
  //   } else {
  //     if (obj['showCorpNum'] === 'colin') {
  //       obj['xproJurisdiction'] = null
  //     } else {
  //       let n = Math.round(Math.random() * 5)
  //       obj['xproJurisdiction'] = testJurisdictions[n]
  //     }
  //   }
  //   testData.push(obj)
  // }

  // /* -- ACTUAL TESTS -- */
  // let createTests = (i) => {
  //   let row = testData[i]
  //   let text = `#${row.number} (location: BC, request_action_cd: ${row.requestAction}, entity_type_cd:` +
  //   ` ${row.entityType}, xproJurisdiction: ${row.jurisdiction ? row.jurisdiction : 'null'}) => returns` +
  //   ` ${row.showCorpNum}`
  //   test(text, () => {
  //     let obj = {
  //       entityType: row.entityType,
  //       requestAction: row.requestAction,
  //       location: 'BC',
  //       jurisdiction: row.jurisdiction
  //     }
  //     setState(obj)
  //     setTimeout(() => {
  //       expect(store.showCorpNum === row.showCorpNum).toBeTruthy()
  //     }, 100)
  //   })
  // }
  // for (let i = 0; i < 43; i++) {
  //   createTests(i)
  // }
})
