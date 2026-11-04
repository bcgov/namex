import { Component, Vue } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import axios, { AxiosError } from 'axios'
import querystring from 'qs'
import { Debounce } from 'vue-debounce-decorator'
import canadaPostAPIKey from '@/config'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { ApplicantI } from '@/interfaces'

@Component({})
export class ActionMixin extends Vue {
  qs: any = querystring

  @Getter(useStore) getApplicant!: ApplicantI

  @Action(useStore) setApplicantDetails!: ActionBindingIF
  @Action(useStore) setAddressSuggestions!: ActionBindingIF

  private isAxiosError (err: AxiosError | Error): boolean {
    return (err as AxiosError).isAxiosError !== undefined
  }

  /**
   * Throws an error with error message extracted and formatted.
   * @param err error object from the catch statement
   * @param defaultMessage optional fallback message
   */
  async handleApiError (err: any, defaultMessage = ''): Promise<string> {
    if (this.isAxiosError(err)) {
      let message = ''
      const responseData = err?.response?.data
      const hasResponseData = !!responseData

      if (hasResponseData && responseData instanceof Blob) {
        // Handle any cases where the API error response is a Blob (eg, request for PDF receipt fails).
        const errorText = await responseData.text()
        const errorJson = JSON.parse(errorText)
        if (errorJson?.message) {
          message = `${err.toString()} [ ${errorJson.message} ]`
        }
      } else if (hasResponseData && responseData instanceof String) {
        // Handle any cases where the API error response is a String.
        message = `${err.toString()} [ ${responseData.toString()} ]`
      } else if (hasResponseData && responseData.message) {
        // Handle any cases where the API error response in an object (eg, { message: 'Ipsum lorem dolor' }).
        message += responseData.message
        message = `${err.toString()} [ ${responseData.message} ]`
      } else if (defaultMessage) {
        // Handle any other cases.
        message = `${err.toString()} [ ${defaultMessage} ]`
      } else {
        return err.toString()
      }

      // Replace line breaks with HTML line breaks.
      return message.replace(/(?:\r\n|\r|\n)/g, '<br>')
    } else {
      // Handle non-axios error (ie, probably a JS error).
      return (err?.toString() || defaultMessage)
    }
  }

  async fetchAddressDetails (id): Promise<void> {
    try {
      const url = 'https://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/Retrieve/v2.11/json3.ws'
      const params = {
        Key: canadaPostAPIKey,
        Id: id
      }

      const resp = await axios.post(url, this.qs.stringify(params), {
        headers: { 'Content-type': 'application/x-www-form-urlencoded' }
      })

      // FUTURE: add error handling in case post() failed

      if (resp.data.Items && Array.isArray(resp.data.Items)) {
        const addressData = resp.data.Items.find(item => item.Language === 'ENG')
        const canadaPostFieldsMapping = {
          CountryIso2: 'countryTypeCd',
          PostalCode: 'postalCd',
          ProvinceCode: 'stateProvinceCd',
          City: 'city',
          Line1: 'addrLine1',
          Line2: 'addrLine2'
        }

        for (const ln of ['2', '3']) {
          if (!addressData[`Line${ln}`]) {
            this.setApplicantDetails({ key: `addrLine${ln}`, value: '' })
          }
        }

        if (addressData['ProvinceCode']) {
          if (addressData['ProvinceCode'].length > 2) {
            this.setApplicantDetails({ key: 'stateProvinceCd', value: '' })
            if (!addressData['ProvinceName']) {
              canadaPostFieldsMapping['ProvinceCode'] = 'addrLine3'
            } else {
              delete canadaPostFieldsMapping.ProvinceCode
              canadaPostFieldsMapping['ProvinceName'] = 'addrLine3'
            }
          }
        } else {
          delete canadaPostFieldsMapping.ProvinceCode
          this.setApplicantDetails({ key: 'stateProvinceCd', value: '' })
          if (addressData['ProvinceName']) {
            canadaPostFieldsMapping['ProvinceName'] = 'addrLine3'
          }
        }

        const fields = Object.keys(canadaPostFieldsMapping)
        for (const field of fields) {
          if (addressData[field]) {
            const value = addressData[field]
            const mappedField = canadaPostFieldsMapping[field]
            this.setApplicantDetails({ key: mappedField, value })
          }
        }
      }
    } catch (err) {
      const msg = await this.handleApiError(err, 'Could not get address details')
      // AddressComplete problem - use console.log not console.error
      console.log('fetchAddressDetails() =', msg) // eslint-disable-line no-console
    }
  }

  @Debounce(250)
  async fetchAddressSuggestions (appKV: { key, value }): Promise<void> {
    try {
      if (!appKV.value) return

      const url = 'https://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/Find/v2.10/json3.ws'
      const params = {
        Key: canadaPostAPIKey,
        SearchTerm: appKV.value,
        MaxSuggestions: 3,
        Country: this.getApplicant.countryTypeCd
      }

      const resp = await axios.post(url, this.qs.stringify(params), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })

      // FUTURE: add error handling in case post() failed

      if (Array.isArray(resp.data.Items)) {
        const filteredItems = resp.data.Items.filter(item => item.Next === 'Retrieve')
        if (this.getApplicant.addrLine1) {
          // this.setApplicantDetails(filteredItems)
          this.setAddressSuggestions(filteredItems)
        }
        return
      }

      this.setApplicantDetails(null)
    } catch (err) {
      const msg = await this.handleApiError(err, 'Could not get address suggestions')
      // AddressComplete problem - use console.log not console.error
      console.log('fetchAddressSuggestions() =', msg) // eslint-disable-line no-console
    }
  }
}
