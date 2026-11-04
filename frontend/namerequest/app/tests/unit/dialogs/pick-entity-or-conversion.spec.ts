import { createLocalVue } from '@vue/test-utils'
// import { mount } from '@vue/test-utils'

import Vuetify from 'vuetify'
// import { PickEntityOrConversionDialog } from '@/components/dialogs'
// import newReqModule from '@/store/new-request-module'

// Prevent the warning "[Vuetify] Unable to locate target [data-app]"
document.body.setAttribute('data-app', 'true')

const localVue = createLocalVue()
// const vuetify = new Vuetify()

localVue.use(Vuetify)

describe('PickEntityOrConversionDialog', () => {
  it('is an empty test', () => {})
  // let wrapper: any

  // beforeEach(() => {
  //   wrapper = mount(PickEntityOrConversionDialog, { localVue, vuetify })
  //   newReqModule.mutateRequestAction('NEW')
  //   newReqModule.mutateLocation('BC')
  // })

  // afterEach(() => {
  //   wrapper.destroy()
  // })

  // it('When the location is set to BC, it displays options for BC', () => {
  //   expect(wrapper.vm.tableData).toStrictEqual(wrapper.vm.tableDataBC)
  // })

  // it('When the location is not set to BC, it displays XPRO options', async () => {
  //   newReqModule.mutateLocation(null)
  //   await wrapper.vm.$nextTick()
  //   expect(wrapper.vm.tableData).toStrictEqual(wrapper.vm.tableDataXPRO)
  // })

  // it('clicking an entity sets the entity_type_cd and closes the modal', async (): Promise<void> => {
  //   wrapper.vm.showModal = true
  //   newReqModule.mutateLocation('CA')
  //   await wrapper.vm.$nextTick()
  //   let foreignCorp = wrapper.find('#XCR')
  //   foreignCorp.trigger('click')
  //   await wrapper.vm.$nextTick()
  //   expect(wrapper.vm.showModal).toBe(false)
  //   expect(newReqModule.entity_type_cd).toBe('XCR')
  // })
})
