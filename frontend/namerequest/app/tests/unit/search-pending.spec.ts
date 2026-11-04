import { createLocalVue } from '@vue/test-utils'
// import { mount } from '@vue/test-utils'
import Vuetify from 'vuetify'
// import SearchPending from '@/components/existing-request/search-pending.vue'

const localVue = createLocalVue()
// const vuetify = new Vuetify()

localVue.use(Vuetify)

describe('SearchPending component', () => {
  it('is an empty test', () => {})
  // const wrapper = mount(SearchPending, {
  //   localVue,
  //   vuetify
  // })
  // it('renders a spinner', () => {
  //   expect(wrapper.find('#analyze-pending-spinner').exists()).toBe(true)
  // })
  // it('does not render a stop button', () => {
  //   expect(wrapper.find('#analyze-pending-stop-button').exists()).toBe(false)
  // })
})
