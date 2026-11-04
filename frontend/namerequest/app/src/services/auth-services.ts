import Axios from 'axios'
import { AddAxiosInterceptors } from '@/plugins'
import { CreateNRAffiliationRequestBody } from '@/interfaces'

const axios = AddAxiosInterceptors(Axios.create())

export default class AuthServices {
  /** The Auth API URL. */
  static get authApiUrl (): string {
    return sessionStorage.getItem('AUTH_API_URL')
  }

  /**
   * Creates an affiliation for the specified account and NR.
   * Returns response on error.
   */
  static async createNrAffiliation (accountId: number, nr: any, newBusiness = true): Promise<any> {
    const newBusinessParam = newBusiness ? '?newBusiness=true' : ''
    const url = `${this.authApiUrl}/orgs/${accountId}/affiliations${newBusinessParam}`
    const requestBody: CreateNRAffiliationRequestBody = {
      businessIdentifier: nr.nrNum,
      phone: nr.applicants?.phoneNumber || '',
      email: nr.applicants?.emailAddress || ''
    }

    return axios.post(url, requestBody)
      .catch(error => error?.response)
  }

  /**
   * Removes an affiliation for the specified account and NR.
   * Throws on error.
   */
  static async removeNrAffiliation (accountId: number, nrNumber: string): Promise<any> {
    const url = `${this.authApiUrl}/orgs/${accountId}/affiliations/${nrNumber}`

    return axios.delete(url)
  }

  /**
   * Fetches affiliations for the specified account.
   * Throws on error.
   */
  static async fetchAffiliations (accountId: number): Promise<any> {
    const url = `${this.authApiUrl}/orgs/${accountId}/affiliations`

    return axios.get(url)
      .then(response => {
        if (response?.data) return response.data
        throw new Error('Invalid affiliations')
      })
  }

  /**
   * Fetches current user's info.
   * Throws on error.
   */
  static async fetchUserInfo (): Promise<any> {
    // don't fetch user info if session isn't synced (ie, user is not logged in)
    // to pre-empt a console error
    if (sessionStorage.getItem('SESSION_SYNCED') !== 'true') return null

    // don't fetch user info if there is no KC token (safety check)
    const token = sessionStorage.getItem('KEYCLOAK_TOKEN')
    if (!token) return null

    const url = `${this.authApiUrl}/users/@me`
    const headers = { Authorization: `Bearer ${token}` }

    return axios.get(url, { headers: headers })
      .then(response => {
        if (response?.data) return response.data
        throw new Error('Invalid user info')
      })
  }

  /**
   * Fetches current user's settings (including their accounts).
   */
  static async fetchUserSettings (keycloakGuid: string): Promise<any[]> {
    const url = `${this.authApiUrl}/users/${keycloakGuid}/settings`

    return axios.get(url)
      .then(response => {
        if (response?.data) return response.data
        throw new Error('Invalid user settings')
      })
  }

  /**
   * Fetches specified org's info.
   * Throws on error.
   */
  static async fetchOrgInfo (orgId: number): Promise<any> {
    const url = `${this.authApiUrl}/orgs/${orgId}`

    return axios.get(url)
      .then(response => {
        if (response?.data) return response.data
        throw new Error('Invalid org info')
      })
  }
}
