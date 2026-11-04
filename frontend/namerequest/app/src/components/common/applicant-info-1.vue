<template>
  <v-form
    id="applicant-info-1-form"
    ref="step1"
    v-model="isValid"
  >
    <v-container
      id="applicant-info-1"
      fluid
      class="pa-0 mt-6"
    >
      <v-row>
        <v-col
          cols="2"
          class="h6 align-self-start"
        >
          Applicant
        </v-col>

        <v-col
          cols="12"
          md="10"
          lg="10"
        >
          <!--FIRST NAME, MIDDLE NAME, LAST NAME-->
          <v-row class="mt-0 mb-n3">
            <v-col
              cols="12"
              md="4"
              lg="4"
              class="pt-0"
            >
              <label
                for="firstname"
                class="hidden"
              >First Name</label>
              <v-text-field
                id="firstname"
                :messages="messages['firstName']"
                :rules="maxCharRules"
                :value="applicant.firstName"
                dense
                filled
                height="50"
                hide-details="auto"
                :name="Math.random()"
                autocomplete="chrome-off"
                label="First Name"
                @blur="handleNameBlur('firstName', $event)"
                @input="updateApplicant('firstName', $event)"
              />
            </v-col>

            <v-col
              cols="12"
              md="4"
              lg="4"
              class="pt-0"
            >
              <label
                for="middlename"
                class="hidden"
              >Middle Name (Optional)</label>
              <v-text-field
                id="middlename"
                :messages="messages['middleName']"
                :value="applicant.middleName"
                :rules="maxCharRules"
                dense
                filled
                height="50"
                hide-details="auto"
                :name="Math.random()"
                autocomplete="chrome-off"
                label="Middle Name (Optional)"
                @blur="handleNameBlur('middleName', $event)"
                @input="updateApplicant('middleName', $event)"
              />
            </v-col>

            <v-col
              cols="12"
              md="4"
              lg="4"
              class="pt-0"
            >
              <label
                for="lastname"
                class="hidden"
              >Last Name</label>
              <v-text-field
                id="lastname"
                :messages="messages['lastName']"
                :rules="lastNameRules"
                :value="applicant.lastName"
                dense
                filled
                height="50"
                hide-details="auto"
                :name="Math.random()"
                autocomplete="chrome-off"
                label="Last Name"
                @blur="handleNameBlur('lastName', $event)"
                @input="updateApplicant('lastName', $event)"
              />
            </v-col>
          </v-row>

          <!--ADDDRESS MENU / STREET ADDRESS-->
          <v-row class="mt-2 mb-0">
            <v-col
              cols="12"
              class="py-0 my-0"
            >
              <v-menu
                v-model="showAddressMenu"
                bottom
                class="pa-2"
                dense
                max-width="600"
                offset-y
              >
                <!-- Using activator slot to avoid having to absolutely position v-menu. Visibility is controlled by
                "showAddressMenu" field, "on" function provided by slot is used only to supress error message. -->
                <!-- eslint-disable-next-line vue/no-unused-vars -->
                <template #activator="{ on }">
                  <v-text-field
                    id="line1"
                    ref="Line1"
                    :messages="messages['Line1']"
                    :rules="requiredRules"
                    :value="applicant.addrLine1"
                    dense
                    filled
                    height="50"
                    hide-details="auto"
                    :name="Math.random()"
                    autocomplete="chrome-off"
                    label="Street Address"
                    @blur="blurAddress1"
                    @input="updateApplicant('addrLine1', $event)"
                  />
                </template>
                <v-list
                  class="ma-0 pa-0"
                  style="border-radius: 0"
                >
                  <v-list-item
                    v-if="!getAddressSuggestions && applicant.addrLine1"
                    dense
                    class="pa-2"
                  >
                    <v-progress-circular
                      id="address-suggest-spinner"
                      color="orange"
                      indeterminate
                      size="25"
                    />
                    <span class="pl-2">Searching...</span>
                  </v-list-item>
                  <v-list-item
                    v-if="!getAddressSuggestions && !applicant.addrLine1"
                    class="pa-2"
                    dense
                  >
                    Start typing an address to get suggestions
                  </v-list-item>
                  <v-list-item
                    v-for="(address, i) of getAddressSuggestions"
                    :id="address.Id"
                    :key="address.Text + '-' + i"
                    :class="getClass(address.Id)"
                    dense
                    style="cursor: pointer"
                  >
                    <a
                      :ref="address.Id"
                      class="link-sm-dk-text"
                      href="#"
                      @click.prevent="fetchAddressDetails(address.Id)"
                      @focus="highlightedSuggestion = address.Id"
                    >
                      {{ address.Text + ', ' + address.Description }}
                    </a>
                  </v-list-item>

                  <v-divider class="mb-2" />

                  <v-list-item>
                    <v-container class="ma-0 pa-0 copy-small">
                      <v-row>
                        <v-col
                          class="ma-0 px-6 pb-4 text-right"
                          align-self="center"
                        >
                          <label
                            class="h5"
                            for="country2"
                          >Country</label>
                        </v-col>
                        <v-col
                          cols="5"
                          class="ma-0 pa-0"
                        >
                          <v-select
                            id="country2"
                            ref="Country2"
                            :items="countryOptions"
                            :menu-props="{ auto: true, eager: true }"
                            :value="applicant.countryTypeCd"
                            class="mb-1 copy-small mr-2"
                            dense
                            eager
                            filled
                            hide-details
                            name="country2"
                            @click.capture.stop
                            @input="updateApplicant('countryTypeCd', $event)"
                          />
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-col>
          </v-row>

          <!--ADDDRESS LINE 2-->
          <v-row class="mt-2 mb-0">
            <v-col
              cols="12"
              class="py-0 my-0"
            >
              <label
                for="line2"
                class="hidden"
              >Additional Street Address (Optional)</label>
              <v-text-field
                id="1ine2"
                ref="Line2"
                :messages="messages['Line2']"
                :rules="maxCharRules"
                :value="applicant.addrLine2"
                dense
                filled
                height="50"
                hide-details="auto"
                :name="Math.random()"
                autocomplete="chrome-off"
                label="Additional Street Address (Optional)"
                @blur="messages = {}"
                @focus="handleFocus('Line2', 'Street Address 2 (Optional)')"
                @input="updateApplicant('addrLine2', $event)"
              />
            </v-col>
          </v-row>

          <!--ADDDRESS LINE 3-->
          <v-row
            v-if="(applicant.addrLine2 || applicant.addrLine3) && !showAddressMenu"
            class="mt-2 mb-0"
          >
            <v-col
              cols="12"
              class="py-0 my-0"
            >
              <label
                for="line3"
                class="hidden"
              >Additional Street Address (Optional)</label>
              <v-text-field
                id="line3"
                ref="Line3"
                :messages="messages['Line3']"
                :rules="maxCharRules"
                :value="applicant.addrLine3"
                dense
                filled
                height="50"
                hide-details="auto"
                :name="Math.random()"
                autocomplete="chrome-off"
                label="Additional Street Address (Optional)"
                @blur="messages = {}"
                @focus="handleFocus('Line2', 'Street Address 3 (Optional)')"
                @input="updateApplicant('addrLine3', $event)"
              />
            </v-col>
          </v-row>

          <!--CITY, PROVINCE/STATE-->
          <v-row class="mt-2 mb-0">
            <v-col
              cols="12"
              md="6"
              lg="6"
              class="py-0 my-0"
            >
              <label
                for="city"
                class="hidden"
              >City</label>
              <v-text-field
                id="city"
                ref="City"
                :messages="messages['City']"
                :rules="requiredRules"
                :value="applicant.city"
                dense
                filled
                height="50"
                hide-details="auto"
                :name="Math.random()"
                autocomplete="chrome-off"
                label="City"
                @blur="messages = {}"
                @focus="handleFocus('City', 'City')"
                @input="updateApplicant('city', $event)"
              />
            </v-col>

            <v-col
              v-if="applicant.countryTypeCd === Location.CA"
              cols="12"
              md="6"
              lg="6"
              class="py-0 my-0"
              :class="{ 'pt-2': isMobile }"
            >
              <label
                for="province"
                class="hidden"
              >Province</label>
              <v-select
                id="province"
                ref="Province"
                :items="provinceOptions"
                :messages="messages['Province']"
                :rules="requiredRules"
                :value="applicant.stateProvinceCd"
                dense
                filled
                height="50"
                hide-details="auto"
                :name="Math.random()"
                autocomplete="chrome-off"
                label="Province"
                @input="updateApplicant('stateProvinceCd', $event)"
                @blur="messages = {}"
                @focus="handleFocus('Province', 'Province')"
              />
            </v-col>

            <v-col
              v-else-if="applicant.countryTypeCd === Location.US"
              cols="12"
              md="6"
              lg="6"
              class="py-0 my-0"
              :class="{ 'pt-2': isMobile }"
            >
              <label
                for="state"
                class="hidden"
              >State</label>
              <v-select
                id="state"
                ref="state"
                :items="UsaStateCodes"
                :messages="messages['State']"
                :rules="requiredRules"
                :value="applicant.stateProvinceCd"
                dense
                filled
                height="50"
                hide-details="auto"
                name="state"
                placeholder="State"
                @input="updateApplicant('stateProvinceCd', $event)"
                @blur="messages = {}"
                @focus="handleFocus('State', 'State')"
              />
            </v-col>

            <v-col
              v-else
              cols="12"
              md="6"
              lg="6"
              class="py-0 my-0"
            >
              <label
                for="state"
                class="hidden"
              >Province/State</label>
              <v-text-field
                id="state"
                ref="state"
                disabled
                :messages="messages['Province']"
                :rules="provStateRules"
                :value="applicant.stateProvinceCd"
                dense
                filled
                height="50"
                hide-details="auto"
                :name="Math.random()"
                autocomplete="chrome-off"
                label="N/A"
                @blur="messages = {}"
                @input="updateApplicant('stateProvinceCd', $event)"
              />
            </v-col>
          </v-row>

          <!--COUNTRY, POSTAL/ZIP CODE-->
          <v-row class="mt-2 mb-0">
            <v-col
              cols="12"
              md="6"
              lg="6"
              class="py-0 my-0"
            >
              <label
                for="country"
                class="hidden"
              >Country</label>
              <v-select
                id="country"
                ref="Country"
                :items="countryOptions"
                :menu-props="{eager: true, auto: true}"
                :rules="requiredRules"
                :value="applicant.countryTypeCd"
                cache-items
                dense
                eager
                filled
                height="50"
                hide-details="auto"
                name="country"
                placeholder="Country"
                @input="updateApplicant('countryTypeCd', $event)"
              />
            </v-col>

            <v-col
              cols="12"
              md="6"
              lg="6"
              class="py-0 my-0"
              :class="{ 'pt-2': isMobile }"
            >
              <label
                for="postalcode"
                class="hidden"
              >Postal/Zip Code</label>
              <v-text-field
                id="postalcode"
                :messages="messages['PostalCode']"
                :rules="requiredRules"
                :value="applicant.postalCd"
                dense
                filled
                height="50"
                hide-details="auto"
                :name="Math.random()"
                autocomplete="chrome-off"
                label="Postal/Zip Code"
                @blur="messages = {}"
                @focus="handleFocus('PostalCode', 'Postal / Zip Code')"
                @input="updateApplicant('postalCd', $event)"
              />
            </v-col>
          </v-row>

          <!--BUSINESS JURISDICTION-->
          <v-row
            v-if="(getLocation !== Location.BC) && showAllFields && getEditMode"
            class="mt-2 mb-0"
          >
            <v-col
              cols="12"
              md="6"
              lg="6"
              class="py-0 my-0"
            >
              <label
                for="xprojurisdiction"
                class="hidden"
              >Business Jurisdiction</label>
              <v-select
                id="xprojurisdiction"
                :messages="messages['xproJurisdiction']"
                :items="jurisdictionOptions"
                :rules="requiredRules"
                :value="xproJurisdiction"
                dense
                eager
                filled
                height="50"
                hide-details="auto"
                name="xprojurisdiction"
                placeholder="Business Jurisdiction"
                @blur="messages = {}"
                @focus="handleFocus('xproJurisdiction', 'Business xproJurisdiction')"
                @input="updateNrData('xproJurisdiction', $event)"
              />
            </v-col>

            <v-col
              cols="6"
              class="py-0 my-0"
            />
          </v-row>

          <!--ACTING ON OWN BEHALF-->
          <v-row class="mt-5 mb-0">
            <v-col
              cols="12"
              md="7"
              lg="7"
              class="py-0"
            >
              <v-checkbox
                v-model="actingOnOwnBehalf"
                hide-details
                label="I am completing this reservation on my own behalf"
                class="mt-2 pt-0"
              />
            </v-col>

            <ApplicantInfoNav @nextAction="nextAction()" />
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script lang="ts">
import { Component, Vue, Watch, Mixins } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import { SessionStorageKeys } from 'sbc-common-components/src/util/constants'
import ApplicantInfoNav from '@/components/common/applicant-info-nav.vue'
import { Location, NrState } from '@/enums'
import { ActionMixin } from '@/mixins'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { EmptyApplicant, NameRequestI } from '@/interfaces'
import { removeExcessSpaces } from '@/plugins/utilities'
import { CanJurisdictions, IntlJurisdictions, UsaStateCodes } from '@/list-data'
import AuthServices from '@/services/auth-services'

@Component({
  components: {
    ApplicantInfoNav
  }
})
export default class ApplicantInfo1 extends Mixins(ActionMixin) {
  // enums for template
  readonly Location = Location
  readonly UsaStateCodes = UsaStateCodes

  @Getter(useStore) getActingOnOwnBehalf!: boolean
  @Getter(useStore) getAddressSuggestions!: any[]
  @Getter(useStore) getDisplayedComponent!: string
  @Getter(useStore) getEditMode!: boolean
  @Getter(useStore) getLocation!: Location
  @Getter(useStore) getNr!: Partial<NameRequestI>
  @Getter(useStore) getNrData!: any
  @Getter(useStore) getNrState!: NrState
  @Getter(useStore) getSubmissionTabNumber!: number
  @Getter(useStore) getKeycloakRoles!: string[]
  @Getter(useStore) isMobile!: boolean
  @Getter(useStore) isRoleStaff!: boolean

  @Action(useStore) setActingOnOwnBehalf!: ActionBindingIF
  @Action(useStore) setCorpNum!: ActionBindingIF
  @Action(useStore) setNRData!: ActionBindingIF
  @Action(useStore) setSubmissionTabNumber!: ActionBindingIF
  @Action(useStore) setFolioNumber!: ActionBindingIF

  highlightedSuggestion: string = null
  isValid = false
  messages = {}
  provStateRules = [
    v => (typeof v === 'string') || 'Must be letters only',
    v => (!v || v.length <= 2) || 'Max 2 characters'
  ]
  lastNameRules = [
    v => !!v || 'Required field',
    v => (!v || v.length <= 50) || 'Cannot exceed 50 characters'
  ]
  maxCharRules = [
    v => (!v || v.length <= 50) || 'Cannot exceed 50 characters'
  ]
  requiredRules = [
    v => !!v || 'Required field',
    v => (v.length <= 50) || 'Cannot exceed 50 characters'
  ]
  showAddressMenu = false

  async mounted () {
    // add event listener when this component is mounted
    // eg, when user continues to send for review
    this.$el.addEventListener('keydown', this.handleKeydown)

    // proceed only if we have any roles (ie, logged in), and not staff
    if (this.getKeycloakRoles.length > 0 && !this.isRoleStaff) {
      // pre-populate submitting party name
      const userInfo = await AuthServices.fetchUserInfo().catch(() => null)
      if (userInfo) {
        this.setApplicantDetails([
          { name: 'firstName', value: userInfo.firstname || '' },
          { name: 'lastName', value: userInfo.lastname || '' }
        ])
      }

      // pre-populate submitting party address
      const currentAccount = sessionStorage.getItem(SessionStorageKeys.CurrentAccount)
      if (currentAccount) {
        const accountId = JSON.parse(currentAccount)?.id
        if (accountId) {
          const orgInfo = await AuthServices.fetchOrgInfo(accountId).catch(() => null)
          if (orgInfo) {
            const mailingAddress = orgInfo.mailingAddress
            if (mailingAddress.street) {
              this.setApplicantDetails([
                { name: 'addrLine1', value: mailingAddress.street || '' },
                { name: 'addrLine2', value: mailingAddress.streetAdditional || '' },
                { name: 'addrLine3', value: '' },
                { name: 'city', value: mailingAddress.city || '' },
                { name: 'stateProvinceCd', value: mailingAddress.region || '' },
                { name: 'countryTypeCd', value: mailingAddress.country || '' },
                { name: 'postalCd', value: mailingAddress.postalCode || '' }
              ])
            }
          }
        }
      }
    }
  }

  destroyed () {
    // remove the event listener when this component is destroyed
    // eg, when user clicks Start Search Over
    this.$el.removeEventListener('keydown', this.handleKeydown)
  }

  get isVisible (): boolean {
    const myComponent = (
      this.getDisplayedComponent === 'SubmissionTabs' ||
      this.getDisplayedComponent === 'ExistingRequestEdit'
    )
    const myTab = (this.getSubmissionTabNumber === 2)
    return (myComponent && myTab)
  }

  get actingOnOwnBehalf () {
    return this.getActingOnOwnBehalf
  }

  set actingOnOwnBehalf (value) {
    if (value) this.setFolioNumber('') // no folio number in case it is on own behalf
    this.setActingOnOwnBehalf(value)
  }

  get applicant () {
    return this.getApplicant || EmptyApplicant
  }

  get countryOptions () {
    return IntlJurisdictions
  }

  get countryTypeCd () {
    return this.getApplicant?.countryTypeCd || ''
  }

  get jurisdictionOptions () {
    // Jurisdiction conversion to uppercase is required to match the model to the values provided by the api.
    return (this.getLocation === Location.CA)
      ? CanJurisdictions.filter(jur => jur.value !== Location.BC)
        .map(jurisdiction => ({ value: jurisdiction.text.toUpperCase(), text: jurisdiction.text }))
      : IntlJurisdictions.filter(jur => jur.value !== Location.CA)
        .map(jurisdiction => ({ value: jurisdiction.text.toUpperCase(), text: jurisdiction.text }))
  }

  get provinceOptions () {
    return CanJurisdictions.filter(jurisdiction => jurisdiction.value !== Location.FD)
      .map(jurisdiction => ({ value: jurisdiction.value, text: jurisdiction.text }))
  }

  get showAllFields (): boolean {
    return (!this.getEditMode || this.getNrState === NrState.DRAFT)
  }

  get state (): NrState {
    if (this.getNr && this.getNrState) {
      return this.getNrState
    }
    return null
  }

  get xproJurisdiction () {
    return this.getNrData?.xproJurisdiction
  }

  /*
    In order to update the trimmed input value, function setApplicationDetails( {key, value}) is also called in @input,
    which looks duplicate. However, there is something going on in the store actions/mutate code
    that requires both the blur and input events to be handled in order for the input component to be reactive.
  */
  handleNameBlur (key, event): void {
    this.messages = {}
    let value = removeExcessSpaces(event.target.value)
    this.setApplicantDetails({ key, value })
  }

  blurAddress1 () {
    this.messages = {}
  }

  clearValidation () {
    if (this.$refs.step1 as any) {
      (this.$refs.step1 as any).resetValidation()
    }
  }

  getClass (Id) {
    if (this.highlightedSuggestion) {
      if (Id === this.highlightedSuggestion) {
        return 'highlight-list-item'
      }
    }
    return ''
  }

  handleFocus (id, message) {
    this.messages[id] = message
    if (id !== 'addrLine1') {
      this.showAddressMenu = false
    }
  }

  handleKeydown (event) {
    if (!this.showAddressMenu) {
      return event
    }
    if (this.showAddressMenu && event.key === 'Escape') {
      this.showAddressMenu = false
    }
    if (this.getAddressSuggestions?.[0] && this.showAddressMenu) {
      if (event.key === 'Tab') {
        event.preventDefault()
        if (!this.highlightedSuggestion) {
          let { Id } = this.getAddressSuggestions[0]
          this.highlightedSuggestion = Id
          let ref: any = this.$refs[Id][0]
          ref.focus()
          return
        }
        if (this.highlightedSuggestion === 'Country2') {
          let { Id } = this.getAddressSuggestions[0]
          let ref: any = this.$refs[Id][0]
          ref.focus()
          return
        }
        let index = this.getAddressSuggestions?.findIndex(suggestion => suggestion.Id === this.highlightedSuggestion)
        if (index === 2) {
          this.highlightedSuggestion = 'Country2'
          let ref: any = this.$refs.Country2
          ref.focus()
          return
        }
        let { Id } = this.getAddressSuggestions[index + 1]
        let ref: any = this.$refs[Id][0]
        ref.focus()
        return
      }
      if (event.key === 'Enter' && this.highlightedSuggestion && this.highlightedSuggestion !== 'Country2') {
        event.preventDefault()
        this.fetchAddressDetails(this.highlightedSuggestion)
        this.showAddressMenu = false
      }
      return event
    }
  }

  async updateApplicant (key, value) {
    this.clearValidation()
    this.setApplicantDetails({ key, value })
    if (key === 'addrLine1') {
      this.showAddressMenu = true
      await this.fetchAddressSuggestions({ key, value })
      return
    }
    if (this.showAddressMenu && key === 'countryTypeCd') {
      this.$nextTick(async () => {
        this.showAddressMenu = true
        let appKV = {
          key: 'addrLine1',
          value: this.getApplicant?.addrLine1
        }
        await this.fetchAddressSuggestions(appKV)
      })
      return
    }
    this.showAddressMenu = false
  }

  updateNrData (key, value) {
    this.setNRData({ key, value })
  }

  validate () {
    if (this.$refs.step1 as Vue) {
      (this.$refs.step1 as any).validate()
    }
  }

  @Watch('isValid')
  onValidChanged (val: boolean) {
    if (val) {
      this.$nextTick(() => {
        if (this.$el?.querySelector instanceof Function) {
          // add classname to button text (for more detail in breadcrumbs)
          const applicantBackBtn = this.$el.querySelector('.submit-back-btn > span')
          if (applicantBackBtn) applicantBackBtn.classList.add('applicant-back-btn')
          const applicantContinueBtn = this.$el.querySelector('.submit-continue-btn > span')
          if (applicantContinueBtn) applicantContinueBtn.classList.add('applicant-continue-btn')
        }
      })
    }
  }

  nextAction () {
    this.validate()
    if (this.isValid) {
      this.setSubmissionTabNumber(this.getSubmissionTabNumber + 1)
    }
  }

  @Watch('countryTypeCd')
  handleProvince (newVal, oldVal) {
    if (newVal !== oldVal) {
      this.setApplicantDetails({ key: 'stateProvinceCd', value: '' })
    }
  }

  @Watch('showAddressMenu')
  suppressMenu (newVal) {
    if (newVal) {
      this.clearValidation()
      return
    }
    this.highlightedSuggestion = null
    let ref: any = this.$refs.Line1
    ref.focus()
  }

  @Watch('xproJurisdiction')
  watchXproJurisdiction (newVal, oldVal) {
    if (newVal !== oldVal) {
      if (this.getEditMode && newVal === this.getNr?.xproJurisdiction) {
        this.setCorpNum(this.getNr?.corpNum)
        return
      }
      this.setCorpNum('')
    }
  }

  @Watch('isVisible')
  private onVisibleChanged (val: boolean) {
    if (val) {
      // add event listener when this component is displayed
      // eg, when user comes back from next tab
      this.$el.addEventListener('keydown', this.handleKeydown)
    } else {
      // remove the event listener when this component is hidden
      // eg, when user continues to next tab
      this.$el.removeEventListener('keydown', this.handleKeydown)
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/styles/theme.scss";

.highlight-list-item {
  background-color: $gray2;
}
</style>
