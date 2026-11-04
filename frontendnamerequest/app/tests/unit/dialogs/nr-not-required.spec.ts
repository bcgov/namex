import { createLocalVue } from '@vue/test-utils'
// import { mount } from '@vue/test-utils'
import Vuetify from 'vuetify'
// import { NrNotRequiredDialog } from '@/components/dialogs'

const localVue = createLocalVue()
// const vuetify = new Vuetify()

localVue.use(Vuetify)

describe('NrNotRequiredDialog', () => {
  it('is an empty test', () => {})
  // let wrapper: any

  // beforeEach(() => {
  //   wrapper = mount(NrNotRequiredDialog, { localVue, vuetify })
  // })

  // afterEach(() => {
  //   wrapper.destroy()
  // })

  // it('Shows the modal when the state is set and it displays the required info', async () => {
  //   await wrapper.setData({ showModal: true })
  //   expect(wrapper.vm.showModal).toBe(true)
  //   expect(wrapper.find('#nr-required-close-btn').element).toBeTruthy()
  //   expect(wrapper.text().includes('You want a numbered company. The business does not need a name.')).toBe(true)
  // })

  // it('Closes the modal when the close button is pressed', async () => {
  //   await wrapper.setData({ showModal: true })
  //   expect(wrapper.vm.showModal).toBe(true)
  //   let button = wrapper.find('.v-btn__content')
  //   await button.trigger('click')
  //   expect(wrapper.vm.showModal).toBe(false)
  // })
})
