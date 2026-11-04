import { createLocalVue } from '@vue/test-utils'
// import { mount, shallowMount } from '@vue/test-utils'
// import NameInput from '@/components/new-request/name-input.vue'
// import newReqModule from '@/store/new-request-module'
import Vuetify from 'vuetify'

const localVue = createLocalVue()
// const vuetify = new Vuetify()

localVue.use(Vuetify)

describe('NameInput component', () => {
  it('is an empty test', () => {})
  // let wrapper: any

  // beforeEach(async () => {
  //   wrapper = mount(NameInput, {
  //     localVue,
  //     vuetify
  //   })
  //   await wrapper.vm.$nextTick()
  //   wrapper.vm.clearErrors()
  // })

  // afterEach(() => {
  //   newReqModule.mutateEntityType('CR')
  //   newReqModule.mutateLocation('BC')
  //   newReqModule.mutateRequestAction('NEW')
  //   newReqModule.mutateName('')
  // })

  // it('Displays the required ui elements', () => {
  //   expect(wrapper.find('#name-input-component').element).toBeTruthy()
  //   expect(wrapper.find('#name-input-icon').element).toBeTruthy()
  // })
  // it('Resists submitting when the entity type is set to "INFO" and detects the correct error type', async () => {
  //   newReqModule.mutateEntityType('INFO')
  //   newReqModule.mutateRequestAction('NEW')
  //   wrapper.vm.nameSearch = 'test'
  //   await wrapper.vm.$nextTick()

  //   expect(newReqModule.displayedComponent).toBe('Tabs')
  // })
  // it('Resists submission when the request type is set to "all" and detects the correct error type', async () => {
  //   newReqModule.store.state.newRequestModule.entity_type_cd = 'CR'
  //   newReqModule.store.state.newRequestModule.request_action_cd = 'INFO'
  //   wrapper.vm.searchValue = 'test'
  //   await wrapper.vm.$nextTick()

  //   let button = wrapper.find('#name-input-icon')
  //   button.trigger('click')
  //   await wrapper.vm.$nextTick()
  //   expect(newReqModule.displayedComponent).toBe('Tabs')
  //   expect(wrapper.vm.errors).toStrictEqual(['request_action_cd'])
  // })
  // it('Resists submission when there is no name entered', async () => {
  //   newReqModule.mutateEntityType('CR')
  //   newReqModule.mutateRequestAction('CNV')

  //   let button = wrapper.find('#name-input-icon')
  //   button.trigger('click')
  //   await wrapper.vm.$nextTick()
  //   expect(newReqModule.displayedComponent).toBe('Tabs')
  //   expect(newReqModule.errors).toEqual([])
  // })
  // it('Resists submission when the name entered is too short and detects the correct error type', async () => {
  //   wrapper.vm.searchValue = 'ab'
  //   let button = wrapper.find('#name-input-icon')
  //   button.trigger('click')
  //   await wrapper.vm.$nextTick()
  //   expect(newReqModule.displayedComponent).toBe('Tabs')
  //   expect(wrapper.vm.errors).toStrictEqual(['length'])
  // })
})
