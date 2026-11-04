import { createLocalVue, mount } from '@vue/test-utils'
// import { shallowMount } from '@vue/test-utils'
// import newReqModule from '@/store/new-request-module'
import Search from '@/components/new-request/search.vue'
import Vuetify from 'vuetify'
import { createPinia, setActivePinia } from 'pinia'
import { useStore } from '@/store'
import { CompanyTypes, EntityTypes, Location, NrRequestActionCodes } from '@/enums'
import { RequestActions } from '@/list-data'

const localVue = createLocalVue()
localVue.use(Vuetify)
const vuetify = new Vuetify()

// Prevent the warning "[Vuetify] Unable to locate target [data-app]"
document.body.setAttribute('data-app', 'true')

const mockFlags = vi.hoisted(() => ({ value: {} as Record<string, any> }))

vi.mock('@/plugins/launchDarkly', () => ({
  GetFeatureFlag: (name: string) => mockFlags.value[name],
  InitLdClient: vi.fn(),
  UpdateLdUser: vi.fn()
}))

setActivePinia(createPinia())
const store = useStore()

describe('Search component', () => {
  it('is an empty test to pre-empt test error', () => {})
  // let wrapper: any

  // beforeEach(async (done) => {
  //   wrapper = shallowMount(Search, {
  //     localVue,
  //     vuetify
  //   })
  //   await wrapper.vm.$nextTick()
  //   done()
  // })

  // it('Displays the necessary UI components', () => {
  //   expect(wrapper.find('#entity-type-options-select').element).toBeTruthy()
  //   expect(wrapper.find('#name-input-component').element).toBeTruthy()
  // })
  // it('Initially sets the state for controlling both info modals visibility to false', () => {
  //   expect(newReqModule.nrRequiredModalVisible).toBe(false)
  //   expect(newReqModule.helpMeChooseModalVisible).toBe(false)
  // })
  // it(
  //   'Initially renders with the BC Corporation entity type as empty and the PickEntityOrConversion modal invisible',
  //   () => {
  //     expect(wrapper.vm.entity_type_cd).toBe('')
  //     expect(newReqModule.pickEntityModalVisible).toBe(false)
  //   })
  // it('Sets PickEntityModal visibility state to true when View All Entity Types is selected', async () => {
  //   wrapper.vm.entity_type_cd = 'INFO'
  //   await wrapper.vm.$nextTick()
  //   expect(newReqModule.pickEntityModalVisible).toBe(true)
  // })
})

describe('Select Company Type block', () => {
  it('is an empty test to pre-empt test error', () => {})
  // let wrapperFactory: any

  // beforeEach(() => {
  //   wrapperFactory = () => mount(Search, { vuetify })
  // })

  // it('renders the component properly', () => {
  //   // verify the component is rendered
  //   const wrapper = wrapperFactory()

  //   expect(wrapper.find('#search-container').exists()).toBe(true)
  //   wrapper.destroy()
  // })

  // it('renders the incorporate button correctly when numbered company is selected', async () => {
  //   const wrapper = wrapperFactory()
  //   await wrapper.find('#numbered-company-radio').setChecked()

  //   expect(wrapper.find('#action-now-button').exists()).toBe(true)
  //   wrapper.destroy()
  // })

  // it('emits event that named company is selected (show check this name button)', async () => {
  //   const wrapper = wrapperFactory()
  //   await wrapper.find('#named-company-radio').setChecked()

  //   expect(wrapper.vm.getSearchCompanyType).toBe('namedCompany')
  //   wrapper.destroy()
  // })
})

describe('Numbered Company Launcher', () => {
  // the "Start a new BC-based business" request action (group 0)
  const newBcBusinessRequest = RequestActions.find(
    ra => !ra.isHeader && ra.group === 0 && ra.value === NrRequestActionCodes.NEW_BUSINESS
  )

  // stub child components -- the launcher buttons are in Search's own template
  const stubs = {
    BusinessLookupFetch: true,
    CompanyType: true,
    CorpNumberCheckbox: true,
    Designation: true,
    DummyInputBox: true,
    EntityType: true,
    Jurisdiction: true,
    NameInput: true,
    NumberedCompanyBullets: true,
    RequestAction: true,
    SocietiesInfo: true,
    XproFederalBullets: true
  }

  const wrapperFactory = () => mount(Search, { vuetify, stubs })

  beforeEach(() => {
    sessionStorage.setItem('CORPORATE_ONLINE_URL', 'https://corporate-online-url/')

    // default flags (launcher off, CR supported for incorporation)
    mockFlags.value = {
      'disable-analysis': true,
      'enable-numbered-company-launcher': false,
      'enable-society': false,
      'supported-amalgamation-entities': [],
      'supported-continuation-in-entities': [],
      'supported-incorporation-registration-entities': [EntityTypes.CR]
    }

    // set up the new BC business + numbered company flow
    store.setRequestAction(NrRequestActionCodes.NEW_BUSINESS)
    store.setSearchRequest(newBcBusinessRequest)
    store.setLocation(Location.BC)
    store.setEntityTypeCd(EntityTypes.CR)
    store.setSearchCompanyType(CompanyTypes.NUMBERED_COMPANY)
    store.setNumberedCompanyHelpModalVisible(false)
  })

  it('shows only the Action Now button when the flag is off and the entity is supported', () => {
    const wrapper = wrapperFactory()

    expect(wrapper.find('#action-now-button').exists()).toBe(true)
    expect(wrapper.find('#action-now-button').text()).toContain('Incorporate Now')
    expect(wrapper.find('#colin-button').exists()).toBe(false)
    expect(wrapper.find('#incorporate-colin-btn').exists()).toBe(false)
    expect(wrapper.find('#incorporate-registry-btn').exists()).toBe(false)
    expect(wrapper.find('#help-me-choose-launcher-btn').exists()).toBe(false)

    wrapper.destroy()
  })

  it('shows only the COLIN button when the flag is off and the entity is not supported', () => {
    mockFlags.value['supported-incorporation-registration-entities'] = []
    const wrapper = wrapperFactory()

    expect(wrapper.find('#colin-button').exists()).toBe(true)
    expect(wrapper.find('#colin-button').text()).toContain('Go to Corporate Online to Register')
    expect(wrapper.find('#action-now-button').exists()).toBe(false)
    expect(wrapper.find('#incorporate-colin-btn').exists()).toBe(false)
    expect(wrapper.find('#incorporate-registry-btn').exists()).toBe(false)

    wrapper.destroy()
  })

  it('shows the launcher buttons and help link when the flag is on', () => {
    mockFlags.value['enable-numbered-company-launcher'] = true
    const wrapper = wrapperFactory()

    const colinBtn = wrapper.find('#incorporate-colin-btn')
    expect(colinBtn.exists()).toBe(true)
    expect(colinBtn.text()).toContain('Incorporate using Corporate Online')
    expect(colinBtn.attributes('href')).toBe('https://corporate-online-url/')
    expect(colinBtn.attributes('target')).toBe('_blank')

    const registryBtn = wrapper.find('#incorporate-registry-btn')
    expect(registryBtn.exists()).toBe(true)
    expect(registryBtn.text()).toContain('Incorporate using the New BC Business Registry')
    expect(registryBtn.attributes('disabled')).toBeUndefined()

    const helpBtn = wrapper.find('#help-me-choose-launcher-btn')
    expect(helpBtn.exists()).toBe(true)
    expect(helpBtn.text()).toContain('Help me Choose')

    expect(wrapper.find('#action-now-button').exists()).toBe(false)
    expect(wrapper.find('#colin-button').exists()).toBe(false)

    wrapper.destroy()
  })

  it('disables the registry button when the entity is not supported', () => {
    mockFlags.value['enable-numbered-company-launcher'] = true
    mockFlags.value['supported-incorporation-registration-entities'] = []
    const wrapper = wrapperFactory()

    expect(wrapper.find('#incorporate-colin-btn').exists()).toBe(true)
    expect(wrapper.find('#incorporate-registry-btn').attributes('disabled')).toBe('disabled')

    wrapper.destroy()
  })

  it('opens the help dialog when the help link is clicked', async () => {
    mockFlags.value['enable-numbered-company-launcher'] = true
    const wrapper = wrapperFactory()

    expect(store.getNumberedCompanyHelpModalVisible).toBe(false)
    await wrapper.find('#help-me-choose-launcher-btn').trigger('click')
    expect(store.getNumberedCompanyHelpModalVisible).toBe(true)

    wrapper.destroy()
  })

  it('does not show the launcher for a benefit company', () => {
    mockFlags.value['enable-numbered-company-launcher'] = true
    mockFlags.value['supported-incorporation-registration-entities'] = [EntityTypes.BC]
    // NB: EntityTypes.BC is the namex code for Benefit Company
    store.setEntityTypeCd(EntityTypes.BC)
    const wrapper = wrapperFactory()

    expect(wrapper.find('#incorporate-colin-btn').exists()).toBe(false)
    expect(wrapper.find('#incorporate-registry-btn').exists()).toBe(false)
    expect(wrapper.find('#help-me-choose-launcher-btn').exists()).toBe(false)
    // a supported benefit company still shows the Action Now button
    expect(wrapper.find('#action-now-button').exists()).toBe(true)

    wrapper.destroy()
  })

  it('does not show the launcher in a non-new-business flow', () => {
    mockFlags.value['enable-numbered-company-launcher'] = true
    store.setRequestAction(NrRequestActionCodes.AMALGAMATE)
    store.setSearchRequest(RequestActions.find(
      ra => !ra.isHeader && ra.value === NrRequestActionCodes.AMALGAMATE
    ))
    const wrapper = wrapperFactory()

    expect(wrapper.find('#incorporate-colin-btn').exists()).toBe(false)
    expect(wrapper.find('#incorporate-registry-btn').exists()).toBe(false)
    expect(wrapper.find('#help-me-choose-launcher-btn').exists()).toBe(false)
    // amalgamation of an unsupported entity still shows the COLIN button
    expect(wrapper.find('#colin-button').exists()).toBe(true)

    wrapper.destroy()
  })
})
