import Vue from 'vue'
import Vuetify from 'vuetify'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import ExistingRequestDisplay from '@/components/existing-request/existing-request-display.vue'
import CheckStatusGrayBox from '@/components/existing-request/check-status-gray-box.vue'
import { useStore } from '@/store'
import { EntityTypes, NrState, PriorityCode } from '@/enums'

const vuetify = new Vuetify()

Vue.prototype.$vuetify = vuetify
document.body.setAttribute('data-app', 'true')

const NAMES_HOME = 'https://dev.names.bcregistry.gov.bc.ca'

setActivePinia(createPinia())
const store = useStore()

function nameRequest (overrides: Record<string, any> = {}) {
  return {
    nrNum: 'NR 8838730',
    entity_type_cd: EntityTypes.CR,
    names: [{ choice: 1, name: 'DAVE TEST FOR ANALYSIS CORPORATION', state: 'NE' }],
    submittedDate: '2026-10-21T21:43:00.000Z',
    request_action_cd: 'NEW',
    state: NrState.DRAFT,
    stateCd: NrState.DRAFT,
    priorityCd: PriorityCode.NO,
    consentFlag: 'N',
    furnished: 'Y',
    actions: [],
    applicants: {
      firstName: 'David',
      lastName: 'McKinnon',
      middleName: '',
      addrLine1: '200-940 Blanshard St',
      city: 'Victoria',
      stateProvinceCd: 'BC',
      postalCd: 'V8W 3E6',
      emailAddress: 'dave@example.com'
    },
    ...overrides
  }
}

describe('ExistingRequestDisplay estimated review times', () => {
  beforeEach(() => {
    sessionStorage.setItem('BASE_URL', NAMES_HOME)
  })

  function mountDisplay (overrides: Record<string, any> = {}) {
    store.setNrResponse(nameRequest(overrides))
    return mount(ExistingRequestDisplay, {
      vuetify,
      stubs: {
        MainContainer: {
          template: '<div><slot name="container-header" /><slot name="content" /></div>'
        },
        NamesGrayBox: true,
        CheckStatusGrayBox: true,
        NrApprovedGrayBox: true,
        NrNotApprovedGrayBox: true,
        ContactInfo: true
      }
    })
  }

  it('points a pending request at this environment Names home page and hides the calendar date', () => {
    const wrapper = mountDisplay()

    expect(wrapper.text()).not.toContain('Estimated Review Date')
    const link = wrapper.find('#names-home-link')
    expect(link.exists()).toBe(true)
    expect(link.text()).toBe(NAMES_HOME)
    expect(link.attributes('href')).toBe(NAMES_HOME)
    expect(wrapper.text()).toContain('For estimated review times, please visit')
    expect(wrapper.findComponent(CheckStatusGrayBox).exists()).toBe(true)
    expect(wrapper.find('#estimated-review-times').findComponent(CheckStatusGrayBox).exists()).toBe(false)

    wrapper.destroy()
  })

  it('keeps the home page link while the request is in progress', () => {
    const wrapper = mountDisplay({ state: NrState.INPROGRESS, stateCd: NrState.INPROGRESS })

    expect(wrapper.find('#names-home-link').attributes('href')).toBe(NAMES_HOME)
    expect(wrapper.text()).not.toContain('Estimated Review Date')

    wrapper.destroy()
  })

  it('keeps the priority review blurb and still links to the Names home page', () => {
    const wrapper = mountDisplay({ priorityCd: PriorityCode.YES })

    expect(wrapper.text()).not.toContain('Estimated Review Date')
    expect(wrapper.text()).toContain('Priority Requests are usually reviewed within')
    expect(wrapper.find('#names-home-link').attributes('href')).toBe(NAMES_HOME)

    wrapper.destroy()
  })

  it('hides the home page sentence once the request is approved', () => {
    const wrapper = mountDisplay({ state: NrState.APPROVED, stateCd: NrState.APPROVED })

    expect(wrapper.find('#estimated-review-times').exists()).toBe(false)
    expect(wrapper.text()).not.toContain('Estimated Review Date')

    wrapper.destroy()
  })

  it('uses the current origin when BASE_URL has not been set', () => {
    sessionStorage.removeItem('BASE_URL')
    const wrapper = mountDisplay()

    expect(wrapper.find('#names-home-link').attributes('href')).toBe(window.location.origin)

    wrapper.destroy()
  })
})
