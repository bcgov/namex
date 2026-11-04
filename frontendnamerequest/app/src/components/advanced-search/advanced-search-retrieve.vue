<template>
  <!-- Advanced Search Retrieve Form -->
  <v-form
    id="advanced-nr-search-form"
    ref="advancedSearchRetrieveForm"
    v-model="isValid"
  >
    <!-- Error Message -->
    <div
      v-if="errorMessage"
      class="copy-normal error-message mt-n2"
      v-html="errorMessage"
    />

    <!-- Phone input -->
    <v-row
      class="mt-6"
      no-gutters
    >
      <v-col>
        <v-text-field
          id="phone-number-text-field"
          v-model="phoneNumber"
          filled
          persistent-hint
          class="copy-normal"
          label="Applicant's Phone Number"
          hint="Example: 555-555-5555"
          :rules="phoneRules"
          @input="handleExistingRequestSearch('phoneNumber', $event)"
        />
      </v-col>
    </v-row>

    <v-row>
      <v-col class="copy-normal font-weight-bold ml-4 py-0">
        or
      </v-col>
    </v-row>

    <!-- Email input -->
    <v-row>
      <v-col>
        <v-text-field
          id="email-address-text-field"
          v-model="emailAddress"
          filled
          persistent-hint
          class="copy-normal"
          label="Applicant's Notification Email"
          hint="Example: name@email.com"
          :rules="emailRules"
          @input="handleExistingRequestSearch('emailAddress', $event)"
        />
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang='ts'>
import { Component, Emit, Prop, Vue, Watch } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import AdvancedSearchDates from '@/components/advanced-search/advanced-search-dates.vue'
import { FormType, NameRequestI } from '@/interfaces'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import NamexServices from '@/services/namex-services'

@Component({
  components: {
    AdvancedSearchDates
  }
})
export default class AdvancedSearchRetrieve extends Vue {
  // Refs
  $refs!: {
    advancedSearchRetrieveForm: FormType
  }

  /** Prompt the form to pass up the form data. */
  @Prop() readonly promptSubmit: boolean

  /** Advanced Search tab state. */
  @Prop() readonly advSearchTabState: boolean

  @Getter(useStore) getNr!: Partial<NameRequestI>

  @Action(useStore) setExistingRequestSearch!: ActionBindingIF
  @Action(useStore) setNameRequest!: ActionBindingIF
  @Action(useStore) setDisplayedComponent!: ActionBindingIF

  // Local properties
  private isValid = false
  private phoneNumber = ''
  private emailAddress = ''
  private errorMessage = ''

  /** Validation rules for Applicant phone and email. */
  private phoneRules = []
  private emailRules = []

  /** Apply the field rules to request search inputs. */
  private applyRules (): void {
    this.phoneRules = (this.phoneNumber || !this.emailAddress)
      ? [
        v => !!v || 'Please enter a phone number',
        v => (v?.length <= 30) || 'Cannot exceed 30 characters'
      ]
      : []

    this.emailRules = (!this.phoneNumber || this.emailAddress)
      ? [
        v => !!v || 'Please enter an email',
        v => (/.+@.+\..+/.test(v)) || 'A valid email is required'
      ]
      : []
  }

  /** Apply rules dynamically and await form validation. */
  private async validateForm (): Promise<void> {
    this.applyRules()
    await this.$refs.advancedSearchRetrieveForm.validate()
  }

  /** Clear field level validations. */
  private async clearValidations (): Promise<void> {
    await this.$refs.advancedSearchRetrieveForm.resetValidation()
    this.phoneRules = []
    this.emailRules = []
    this.errorMessage = ''
  }

  /** Update store values with search parameters.
   * @param key The store key value (ie.. phoneNumber or emailAddress).
   * @param value The search parameter for the associated key.
   */
  private handleExistingRequestSearch (key: string, value: string) {
    this.clearValidations()
    this.setExistingRequestSearch({ key, value })
  }

  /** Validate form, submit request and handle NR response. */
  @Watch('promptSubmit')
  private async handleSubmit (): Promise<void> {
    await this.validateForm()

    if (this.isValid) {
      this.$root.$emit('showSpinner', true)
      const request = await NamexServices.getNameRequest(false)

      if (!request) {
        this.errorMessage = `No records were found that match the information you entered.<br>
        Please verify the Applicant’s phone number or email and try again..`
      } else {
        this.emitClose()
        this.setNameRequest(request)
        this.setDisplayedComponent('ExistingRequestDisplay')
      }
      this.$root.$emit('showSpinner', false)
    }
  }

  /** Clear form. */
  @Watch('advSearchTabState')
  private clearForm (): void {
    this.clearValidations()
    this.phoneNumber = ''
    this.emailAddress = ''
  }

  @Emit('closeDialog')
  private emitClose () : void {}
}
</script>
<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';

#find-nr-btn {
  color: $app-blue;
  font-size: $px-14;
}

#clear-date-btn {
  cursor: pointer;
}

::v-deep .v-icon {
  color: $app-blue;
}
</style>
