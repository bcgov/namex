import { SessionStorageKeys } from 'sbc-common-components/src/util/constants'

/** Gets Keycloak JWT and parses it. */
function getJWT (): any {
  const token = sessionStorage.getItem(SessionStorageKeys.KeyCloakToken)
  if (token) {
    return parseToken(token)
  }
  throw new Error('Error getting Keycloak token')
}

/** Decodes and parses Keycloak token. */
function parseToken (token: string): any {
  try {
    const base64Url = token.split('.')[1]
    const base64 = decodeURIComponent(window.atob(base64Url).split('').map(function (c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
    }).join(''))
    return JSON.parse(base64)
  } catch (err) {
    throw new Error('Error parsing Keycloak token - ' + err)
  }
}

/** Gets Keycloak GUID (the "sub" claim) from JWT. */
export function getKeycloakGuid (): string {
  const jwt = getJWT()
  if (jwt.sub) {
    return jwt.sub
  }
  throw new Error('Error getting Keycloak GUID')
}

/** Gets Keycloak roles from JWT. */
export function getKeycloakRoles (): Array<string> {
  const jwt = getJWT()
  const keycloakRoles = jwt.roles
  if (keycloakRoles && keycloakRoles.length > 0) {
    return keycloakRoles
  }
  throw new Error('Error getting Keycloak roles')
}

/**
 * True when session storage holds a Registries account id.
 * The header writes CURRENT_ACCOUNT as "" when auth-api returns no account.
 * That value is not an account.
 */
function hasRegistriesAccount (): boolean {
  const raw = sessionStorage.getItem(SessionStorageKeys.CurrentAccount)
  if (!raw || raw === 'undefined' || raw === 'null') return false
  try {
    const account = JSON.parse(raw)
    return !!(account && typeof account === 'object' && account.id)
  } catch {
    return false
  }
}

/**
 * True when a BC Services Card or BCeID session exists and auth-api has no Registries account.
 * Staff are excluded: they pay without a public Registries account.
 */
export function isLoggedInWithoutRegistriesAccount (): boolean {
  const token = sessionStorage.getItem(SessionStorageKeys.KeyCloakToken)
  if (!token) return false
  if (hasRegistriesAccount()) return false
  try {
    return !getKeycloakRoles().includes('staff')
  } catch {
    return true
  }
}
