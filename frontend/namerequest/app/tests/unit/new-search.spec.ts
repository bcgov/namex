import { createLocalVue } from '@vue/test-utils'
// import {  mount, shallowMount } from '@vue/test-utils'
// import NewSearch from '@/components/new-request/search.vue'
// import newReqModule from '@/store/new-request-module'
import Vuetify from 'vuetify'

const localVue = createLocalVue()
// const vuetify = new Vuetify()

localVue.use(Vuetify)

describe('NewSearch component', () => {
  it('is an empty test', () => {})
  // let wrapper: any

  // beforeEach(async () => {
  //   wrapper = mount(NewSearch, {
  //     localVue,
  //     vuetify
  //   })
  //   newReqModule.mutateEntityType('CR')
  //   newReqModule.mutateLocation('BC')
  //   newReqModule.mutateRequestAction('NEW')
  //   newReqModule.mutateName('test valid name')
  //   await wrapper.vm.$nextTick()
  //   wrapper.vm.clearErrors()
  // })

  // it('Resists submission when there is no action selected', async () => {
  //   newReqModule.mutateRequestAction('')

  //   let button = wrapper.find('#search-name-btn')
  //   button.trigger('click')
  //   await wrapper.vm.$nextTick()
  //   expect(newReqModule.displayedComponent).toBe('Tabs')
  //   expect(newReqModule.errors).toContain('request_action_cd')
  //   expect(wrapper.vm.errors).toContain('request_action_cd')
  // })
  // it('Resists submission when there is no location selected', async () => {
  //   newReqModule.mutateLocation(null)

  //   let button = wrapper.find('#search-name-btn')
  //   button.trigger('click')
  //   await wrapper.vm.$nextTick()
  //   expect(newReqModule.displayedComponent).toBe('Tabs')
  //   expect(newReqModule.errors).toContain('location')
  //   expect(wrapper.vm.errors).toContain('location')
  // })
  // it('Resists submission when there is no entity type selected', async () => {
  //   newReqModule.mutateEntityType('')

  //   let button = wrapper.find('#search-name-btn')
  //   button.trigger('click')
  //   await wrapper.vm.$nextTick()
  //   expect(newReqModule.displayedComponent).toBe('Tabs')
  //   expect(newReqModule.errors).toContain('entity_type_cd')
  //   expect(wrapper.vm.errors).toContain('entity_type_cd')
  // })
})
