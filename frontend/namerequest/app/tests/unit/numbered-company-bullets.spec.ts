import Vuetify from 'vuetify'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import NumberedCompanyBullets from '@/components/new-request/search-components/numbered-company-bullets.vue'

const vuetify = new Vuetify()

const mockFlags = vi.hoisted(() => ({ value: {} as Record<string, any> }))

vi.mock('@/plugins/launchDarkly', () => ({
  GetFeatureFlag: (name: string) => mockFlags.value[name],
  InitLdClient: vi.fn(),
  UpdateLdUser: vi.fn()
}))

setActivePinia(createPinia())

describe('NumberedCompanyBullets component', () => {
  it('displays the original bullets when the launcher flag is disabled', () => {
    mockFlags.value = { 'enable-numbered-company-launcher': false }
    const wrapper = mount(NumberedCompanyBullets, { vuetify })

    const bullets = wrapper.findAll('li')
    expect(bullets.length).toBe(3)
    expect(bullets.at(0).text()).toBe('Your business name will be the Incorporation Number assigned by the Registry.')
    expect(bullets.at(1).text()).toBe('You can change your business name at a later date.')
    expect(bullets.at(2).text()).toBe('It is not possible to request a specific Incorporation Number.')

    wrapper.destroy()
  })

  it('displays the launcher bullets when the launcher flag is enabled', () => {
    mockFlags.value = { 'enable-numbered-company-launcher': true }
    const wrapper = mount(NumberedCompanyBullets, { vuetify })

    const bullets = wrapper.findAll('li')
    expect(bullets.length).toBe(2)
    expect(bullets.at(0).text())
      .toContain('Your business name will be the Incorporation Number assigned by the Registry.')
    expect(bullets.at(0).text()).toContain('(It is not possible to request a specific number)')
    expect(bullets.at(1).text()).toBe('You can change your business name at a later date.')

    wrapper.destroy()
  })
})
