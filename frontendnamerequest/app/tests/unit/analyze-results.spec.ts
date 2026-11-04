// import AnalyzeResults from '@/components/new-request/analyze-results.vue'
// import testData from './api/get-name-analysis'
import { createLocalVue } from '@vue/test-utils'
// import { mount } from '@vue/test-utils'
// import newReqModule from '@/store/new-request-module'
import Vuetify from 'vuetify'

document['getSelection'] = vi.fn()

const localVue = createLocalVue()
localVue.use(Vuetify)
// const vuetify = new Vuetify()

// function setState (data) {
//   newReqModule.mutateEntityType('CR')
//   newReqModule.mutateLocation('BC')
//   newReqModule.mutateRequestAction('NEW')
//   newReqModule.mutateName(data['name'])
//   newReqModule.mutateAnalysisJSON(data['analysisJSON'])
//   return new Promise(resolve => {
//     setTimeout(() => {
//       resolve('resolved')
//     }, 100)
//   })
// }

describe('AnalyzeResults component', () => {
  it('is an empty test', () => {})
  // let lengthTestData = testData.length
  // let wrapper: any

  // for (let iTestData = 0; iTestData < lengthTestData; iTestData++) {
  //   let data = testData[iTestData]
  //   let { name } = data
  //   let { corrected } = data
  //   let lengthIssues = data.analysisJSON.issues.length

  //   describe(`Testing name-analysis with location=BC, request_action=NEW, and entity_type=CR`, () => {
  //     let iIssues: number
  //     let issue: any
  //     let issue_type: string
  //     let issues = data.analysisJSON.issues.map(iss => iss.issue_type)

  //     describe(`originalName = ${name}`, () => {
  //       beforeAll(async (done) => {
  //         await setState(data)
  //         wrapper = mount(AnalyzeResults, {
  //           localVue,
  //           vuetify
  //         })
  //         await wrapper.vm.$nextTick()
  //         async function handleIssue () {
  //           switch (wrapper.vm.issue.issue_type) {
  //             case 'queue_conflict':
  //             case 'corp_conflict':
  //             case 'consent_required':
  //               // eslint-disable-next-line
  //               let checkbox = wrapper.find('#provide-consent-checkbox')
  //               await checkbox.setChecked()
  //               return new Promise(resolve => { resolve(null) })

  //             case 'designation_non_existent':
  //             case 'designation_mismatch':
  //             case 'end_designation_more_than_once':
  //               // eslint-disable-next-line
  //               let designation = wrapper.find('#designation-btn-0')
  //               await designation.trigger('click')
  //               return new Promise(resolve => { resolve(null) })

  //             case 'designation_misplaced':
  //               // eslint-disable-next-line
  //               let move = wrapper.find('#move-designation-btn')
  //               await move.trigger('click')
  //               return new Promise(resolve => { resolve(null) })
  //           }
  //         }

  //         await handleIssue()
  //         if (wrapper.find('#next-issue-btn').exists()) {
  //           // eslint-disable-next-line
  //           let btn = wrapper.find('#next-issue-btn')
  //           await btn.trigger('click')
  //           await handleIssue()
  //         }
  //         if (wrapper.find('#next-issue-btn').exists()) {
  //           // eslint-disable-next-line
  //           let btn = wrapper.find('#next-issue-btn')
  //           await btn.trigger('click')
  //           await handleIssue()
  //         }
  //         if (wrapper.find('#next-issue-btn').exists()) {
  //           // eslint-disable-next-line
  //           let btn = wrapper.find('#next-issue-btn')
  //           await btn.trigger('click')
  //           await handleIssue()
  //         }
  //         await wrapper.vm.$nextTick()
  //         done()
  //       })
  //       // These tests only check conditions after correcting all the Issues..
  //       test('Name Ready for review after resoling all issues', async () => {
  //         expect(wrapper.text()).toContain('Name Ready for Review')
  //       })
  //       test(`this.name === ${data.corrected}`, () => {
  //         expect(wrapper.vm.name).toBe(data.corrected)
  //       })
  //       test('Cannot alter the name once issues are corrected', async () => {
  //         expect(wrapper.find('#name-search-bar').text()).toBe(`${corrected}`)
  //         wrapper.vm.name = 'ALTERED NAME'

  //         await wrapper.vm.$nextTick()
  //         expect(wrapper.find('#name-search-bar').text()).toBe(`${corrected}`)
  //         expect(wrapper.text()).toContain('Name Ready for Review')
  //       })
  //     })
  //   })
  // }
})
