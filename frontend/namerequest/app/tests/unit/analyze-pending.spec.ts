import { createLocalVue } from '@vue/test-utils'
import Vuetify from 'vuetify'
// import newReqModule from '@/store/new-request-module'

const localVue = createLocalVue()

localVue.use(Vuetify)

describe('AnalyzePending component', () => {
  it('is an empty test', () => {})
  // let wrapper: any
  // beforeAll(async () => {
  //   newReqModule.mutateEntityType('CR')
  //   newReqModule.mutateLocation('BC')
  //   newReqModule.mutateRequestAction('NEW')
  //   newReqModule.mutateAnalyzePending(true)
  //   wrapper = mount(AnalyzePending, {
  //     localVue,
  //     vuetify
  //   })
  // })
  // it('renders a spinner', () => {
  //   expect(wrapper.find('#analyze-pending-spinner').element).toBeTruthy()
  // })
  // it('renders a stop button', () => {
  //   expect(wrapper.find('#analyze-pending-stop-button').element).toBeTruthy()
  // })
})
