import Vuetify from 'vuetify'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import NumberedCompanyHelpDialog from '@/components/dialogs/numbered-company-help.vue'
import { useStore } from '@/store'
import { EntityTypes } from '@/enums'

const vuetify = new Vuetify()

// Prevent the warning "[Vuetify] Unable to locate target [data-app]"
document.body.setAttribute('data-app', 'true')

const mockFlags = vi.hoisted(() => ({ value: {} as Record<string, any> }))

vi.mock('@/plugins/launchDarkly', () => ({
  GetFeatureFlag: (name: string) => mockFlags.value[name],
  InitLdClient: vi.fn(),
  UpdateLdUser: vi.fn()
}))

const mockNavigate = vi.hoisted(() => vi.fn())

vi.mock('@/plugins/navigate', () => ({
  Navigate: mockNavigate
}))

setActivePinia(createPinia())
const store = useStore()

// NB: store state is set before mounting because pinia -> component reactivity
// is not available in this test environment (pinia is externalized by vitest)
describe('NumberedCompanyHelpDialog', () => {
  beforeEach(() => {
    sessionStorage.setItem('CORPORATE_ONLINE_URL', 'https://corporate-online-url/')
    sessionStorage.setItem('BUSINESS_HOME_URL', 'https://business-home-url/')
    mockFlags.value = {
      'supported-incorporation-registration-entities': [EntityTypes.CR]
    }
    store.setEntityTypeCd(EntityTypes.CR)
    mockNavigate.mockClear()
  })

  afterEach(() => {
    store.setNumberedCompanyHelpModalVisible(false)
  })

  it('is hidden when the state is not set', () => {
    const wrapper = mount(NumberedCompanyHelpDialog, { vuetify })

    expect(wrapper.vm.showModal).toBe(false)
    expect(wrapper.find('#numbered-company-help-close-btn').exists()).toBe(false)

    wrapper.destroy()
  })

  it('shows the modal when the state is set and displays both option cards', () => {
    store.setNumberedCompanyHelpModalVisible(true)
    const wrapper = mount(NumberedCompanyHelpDialog, { vuetify })

    expect(wrapper.vm.showModal).toBe(true)
    expect(wrapper.text()).toContain('Choose the website you want to use')

    // Corporate Online card
    const coCard = wrapper.find('#corporate-online-card')
    expect(coCard.exists()).toBe(true)
    expect(coCard.text()).toContain('Corporate Online')
    expect(coCard.text()).toContain('For complex filings.')
    expect(coCard.text()).toContain('combine or merge your business with another business (Amalgamation)')
    expect(coCard.text()).toContain('reactivate a business (Restoration)')
    expect(coCard.text()).toContain('Note: all businesses in Corporate Online will be moved')
    const coBtn = coCard.find('#help-corporate-online-btn')
    expect(coBtn.text()).toContain('Continue to Corporate Online')
    expect(coBtn.attributes('href')).toBe('https://corporate-online-url/')
    expect(coBtn.attributes('target')).toBe('_blank')

    // BC Business Registry card
    const brCard = wrapper.find('#business-registry-card')
    expect(brCard.exists()).toBe(true)
    expect(brCard.text()).toContain('BC Business Registry')
    expect(brCard.text()).toContain('For everyday filings.')
    expect(brCard.text()).toContain('file annual reports')
    expect(brCard.text()).toContain('change your business address when you move')
    expect(brCard.text()).toContain('change directors names or addresses')
    expect(brCard.text()).toContain('change basic business information (Alteration)')
    const brBtn = brCard.find('#help-business-registry-btn')
    expect(brBtn.text()).toContain('Use the New BC Business Registry')
    expect(brBtn.attributes('disabled')).toBeUndefined()

    wrapper.destroy()
  })

  it('disables the registry button when the entity is not supported', () => {
    mockFlags.value['supported-incorporation-registration-entities'] = []
    store.setNumberedCompanyHelpModalVisible(true)
    const wrapper = mount(NumberedCompanyHelpDialog, { vuetify })

    expect(wrapper.find('#help-business-registry-btn').attributes('disabled')).toBe('disabled')

    wrapper.destroy()
  })

  it('closes the modal when the close button is pressed', async () => {
    store.setNumberedCompanyHelpModalVisible(true)
    const wrapper = mount(NumberedCompanyHelpDialog, { vuetify })
    expect(wrapper.vm.showModal).toBe(true)

    await wrapper.find('#numbered-company-help-close-btn').trigger('click')

    expect(store.getNumberedCompanyHelpModalVisible).toBe(false)

    wrapper.destroy()
  })

  it('closes the modal and actions the NR when the registry button is pressed', async () => {
    store.setNumberedCompanyHelpModalVisible(true)
    const wrapper = mount(NumberedCompanyHelpDialog, { vuetify })

    await wrapper.find('#help-business-registry-btn').trigger('click')

    expect(store.getNumberedCompanyHelpModalVisible).toBe(false)
    // unauthenticated user is redirected to login with a double-encoded return parameter
    const returnParam = encodeURIComponent(encodeURIComponent(window.location.href))
    expect(mockNavigate).toHaveBeenCalledWith(`https://business-home-url/en-CA/auth/login?return=${returnParam}`)

    wrapper.destroy()
  })
})
