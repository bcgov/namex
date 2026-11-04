// import ApplicantInfo2 from '@/components/common/applicant-info-2.vue'
import { createLocalVue } from '@vue/test-utils'
// import { shallowMount, mount } from '@vue/test-utils'
// import module from '@/store/new-request-module'
import Vuetify from 'vuetify'
// import Vuex from 'vuex'

const localVue = createLocalVue()
// const vuetify = new Vuetify()
localVue.use(Vuetify)

describe('ApplicantInfo2 component', () => {
  it('is an empty test', () => {})
  // let wrapper: any

  // beforeEach(async (done) => {
  //   wrapper = mount(ApplicantInfo2, {
  //     localVue,
  //     vuetify
  //   })
  //   await wrapper.vm.$nextTick()
  //   done()
  // })
  // it('checks the corpNum against the appropriate database given the setup: BC location', async () => {
  //   const mrasActions = []
  //   function setStore (jurisdiction, action) {
  //     module.mutateXproJurisdiction('Alberta')
  //   }
  // })
})
