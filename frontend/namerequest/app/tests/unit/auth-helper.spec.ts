import { SessionStorageKeys } from 'sbc-common-components/src/util/constants'
import { isLoggedInWithoutRegistriesAccount } from '@/plugins/authHelper'

function tokenWithRoles (roles: string[]): string {
  const payload = btoa(JSON.stringify({ sub: 'user-1', roles }))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '')
  return `header.${payload}.signature`
}

describe('isLoggedInWithoutRegistriesAccount', () => {
  beforeEach(() => {
    sessionStorage.clear()
  })

  it('is false when there is no Keycloak session', () => {
    expect(isLoggedInWithoutRegistriesAccount()).toBe(false)
  })

  it('is false when the session already has a Registries account', () => {
    sessionStorage.setItem(SessionStorageKeys.KeyCloakToken, tokenWithRoles(['public']))
    sessionStorage.setItem(SessionStorageKeys.CurrentAccount, JSON.stringify({ id: 1 }))
    expect(isLoggedInWithoutRegistriesAccount()).toBe(false)
  })

  it('is false for staff, who pay without a public Registries account', () => {
    sessionStorage.setItem(SessionStorageKeys.KeyCloakToken, tokenWithRoles(['staff']))
    expect(isLoggedInWithoutRegistriesAccount()).toBe(false)
  })

  it('is true for a BCSC or BCeID login with no Registries account', () => {
    sessionStorage.setItem(SessionStorageKeys.KeyCloakToken, tokenWithRoles(['public']))
    expect(isLoggedInWithoutRegistriesAccount()).toBe(true)
  })

  it('is true when the header stored an empty account', () => {
    sessionStorage.setItem(SessionStorageKeys.KeyCloakToken, tokenWithRoles(['public']))
    sessionStorage.setItem(SessionStorageKeys.CurrentAccount, JSON.stringify(''))
    expect(isLoggedInWithoutRegistriesAccount()).toBe(true)
  })

  it('is true when the stored account has no id', () => {
    sessionStorage.setItem(SessionStorageKeys.KeyCloakToken, tokenWithRoles(['public']))
    sessionStorage.setItem(SessionStorageKeys.CurrentAccount, JSON.stringify({}))
    expect(isLoggedInWithoutRegistriesAccount()).toBe(true)
  })
})
