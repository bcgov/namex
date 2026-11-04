// import NamesCapture from '@/components/common/names-capture.vue'
import { createLocalVue } from '@vue/test-utils'
// import { shallowMount, mount } from '@vue/test-utils'
// import store from '@/store/new-request-module'
import Vuetify from 'vuetify'

const localVue = createLocalVue()
// const vuetify = new Vuetify()

localVue.use(Vuetify)

describe('NamesCapture component', () => {
  it('is an empty test', () => {})
  // describe('It initially renders correctly', () => {
  //   let wrapper

  //   beforeAll(async (done) => {
  //     store.mutateName('Test Name')
  //     wrapper = mount(NamesCapture, {
  //       localVue,
  //       vuetify,
  //     })
  //     store.mutateRequestAction('NEW')
  //     store.mutateLocation('BC')
  //     store.mutateEntityType('CR')
  //     await wrapper.vm.$nextTick()
  //     done()
  //   })
  //   it('displays the first choice text field and designation select', () => {
  //     expect(wrapper.find('#choice-1-text-field').element).toBeTruthy()
  //     expect(wrapper.find('#designation-1-select').element).toBeTruthy()
  //   })
  //   it('sets the first name choice to the analyzed name', () => {
  //     expect(wrapper.vm.nameChoices.name1).toBe('Test Name')
  //   })
  //   it('Initially renders the enabled continue button', () => {
  //     expect(wrapper.vm.isValid).toBe(false)
  //     expect(wrapper.find('.submit-continue-btn').classes().includes('v-btn')).toBeTruthy()
  //   })
  //   it('demonstrates correct validation logic when designation-1 is entered', async () => {
  //     store.mutateNameChoices({ key: 'name1', value: 'A Really Nice Name' })
  //     store.mutateNameChoices({ key: 'designation1', value: 'INC.' })
  //     await wrapper.vm.$nextTick()
  //     expect(wrapper.vm.isValid).toBe(true)
  //     expect(wrapper.find('.submit-continue-btn').element).toBeTruthy()
  //   })
  //   it('calls showNextComponent() when continue button is clicked and form is valid', async () => {
  //     store.mutateNameChoicesToInitialState()
  //     store.setActiveComponent('NamesCapture')
  //     store.mutateNameChoices({ key: 'name1', value: 'LALA NAME' })
  //     store.mutateNameChoices({ key: 'designation1', value: 'INC.' })
  //     await wrapper.vm.$nextTick()
  //     let btn = wrapper.find('.submit-continue-btn')
  //     btn.trigger('click')
  //     await wrapper.vm.$nextTick()
  //     expect(wrapper.vm.isValid).toBeTruthy()
  //   })
  //   it('detects when choice3 is made without choice2', async () => {
  //     store.mutateNameChoices({ key: 'name1', value: 'a great name' })
  //     store.mutateNameChoices({ key: 'designation1', value: 'LTD.' })
  //     store.mutateNameChoices({ key: 'name2', value: 'a great name' })
  //     store.mutateNameChoices({ key: 'designation2', value: 'LTD.' })
  //     store.mutateNameChoices({ key: 'name3', value: 'a great name' })
  //     store.mutateNameChoices({ key: 'designation3', value: '' })
  //     await wrapper.vm.$nextTick()
  //     expect(wrapper.vm.isValid).toBe(false)
  //     expect(wrapper.vm.messages.des3).toBe('Please choose a designation')
  //   })
  //   it('detects when choice2 is made without a designation', async () => {
  //     store.mutateNameChoices({ key: 'name2', value: 'a great name' })
  //     await wrapper.vm.$nextTick()
  //     expect(wrapper.vm.isValid).toBe(false)
  //   })
  // })
})
