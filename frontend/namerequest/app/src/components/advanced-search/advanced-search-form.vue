<template>
  <!-- Advanced Search Form -->
  <v-form
    id="advanced-nr-search-form"
    ref="advancedSearchForm"
    v-model="isValid"
    lazy-validation
  >
    <AdvancedSearchDates
      :dialog="dateDialog"
      @addDates="addDates($event)"
      @closeDialog="dateDialog = false"
    />

    <v-row no-gutters>
      <v-col>
        <span class="title-bold-16">Requested Business Name</span>
        <v-text-field
          v-model="compName"
          filled
          class="mt-2"
          label="Requested Business Name"
        />
      </v-col>
    </v-row>

    <v-row
      no-gutters
      class="mt-n2"
    >
      <v-col>
        <span class="title-bold-16">Applicant Name</span>
        <v-row class="my-1">
          <v-col
            cols="12"
            md="6"
            lg="6"
          >
            <v-text-field
              v-model="applicantFirstName"
              filled
              label="First Name"
            />
          </v-col>
          <v-col
            cols="12"
            md="6"
            lg="6"
          >
            <v-text-field
              v-model="applicantLastName"
              filled
              label="Last Name"
              :rules="applicantLastNameRules"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <v-row
      no-gutters
      class="mt-n4"
    >
      <v-col>
        <span class="title-bold-16 mr-4">Submitted Date Range</span>
        <span
          v-if="hasAppliedDates"
          id="clear-date-btn"
          class="text-body-3 app-blue"
          @click="clearDates()"
        >
          Clear <v-icon small>mdi-close</v-icon>
        </span>
        <v-row class="my-1">
          <v-col
            cols="12"
            md="6"
            lg="6"
          >
            <v-text-field
              v-model="startDate"
              filled
              label="Start Date"
              hint="YYYY-MM-DD"
              persistent-hint
              append-icon="mdi-calendar"
              @click="dateDialog = true"
              @click:append="dateDialog = true"
              @keydown="$event.preventDefault()"
            />
          </v-col>
          <v-col
            cols="12"
            md="6"
            lg="6"
          >
            <v-text-field
              v-model="endDate"
              filled
              label="End Date"
              hint="YYYY-MM-DD"
              persistent-hint
              append-icon="mdi-calendar"
              @click="dateDialog = true"
              @click:append="dateDialog = true"
              @keydown="$event.preventDefault()"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang='ts'>
import { Component, Emit, Prop, Vue, Watch } from 'vue-property-decorator'
import AdvancedSearchDates from '@/components/advanced-search/advanced-search-dates.vue'

// Interfaces
import { AdvancedSearchI, FormType, StartEndDatesI } from '@/interfaces'

@Component({
  components: {
    AdvancedSearchDates
  }
})
export default class AdvancedSearchForm extends Vue {
  // Refs
  $refs!: {
    advancedSearchForm: FormType
  }

  /** Prompt the form to pass up the form data. */
  @Prop() readonly promptSubmit: boolean

  /** Advanced search dialog state. */
  @Prop() readonly advSearchDialogState: boolean

  // Local Properties
  isValid = false
  dateDialog = false

  // Local model
  compName = ''
  applicantFirstName = ''
  applicantLastName = ''
  startDate = ''
  endDate = ''

  /** Validation rules for Applicant last name. */
  applicantLastNameRules = []

  /** Is true when start and End dates are applied. */
  get hasAppliedDates (): boolean {
    return !!this.startDate && !!this.endDate
  }

  /** True when the form is validating Names. */
  private get hasAppliedNameRules (): boolean {
    return this.applicantLastNameRules.length > 0
  }

  /** Is true when the minimum search criteria is met. */
  private get hasMinimumSearchCriteria (): boolean {
    return !!this.compName || !!this.applicantLastName || (!!this.startDate && !!this.endDate)
  }

  /** Apply the date selections to local model. */
  addDates (dates: StartEndDatesI): void {
    this.startDate = dates.startDate
    this.endDate = dates.endDate
  }

  /** Apply rules and validate form. */
  private async isValidForm (): Promise<boolean> {
    if (this.applicantFirstName) {
      this.applicantLastNameRules = [
        v => !!v || 'Last name is required'
      ]
    }
    await this.$refs.advancedSearchForm.validate()

    this.emitInvalid()
    return this.hasMinimumSearchCriteria && this.isValid
  }

  /** Clear local dates. */
  clearDates (): void {
    this.startDate = ''
    this.endDate = ''
  }

  @Watch('applicantFirstName')
  private clearApplicantRules (): void {
    if (!this.applicantFirstName) this.applicantLastNameRules = []
  }

  /** Clear form. */
  @Watch('advSearchDialogState')
  private clearForm (): void {
    this.compName = ''
    this.applicantFirstName = ''
    this.applicantLastName = ''
    this.clearDates()
  }

  /** Emit form validity when the form is submitted or minimum requirements change thereafter. */
  @Watch('hasMinimumSearchCriteria')
  @Emit('isInvalid')
  private emitInvalid (): boolean {
    if (this.hasAppliedNameRules) return false

    return !this.hasMinimumSearchCriteria
  }

  /** Emit submission data to parent if form passes validation. */
  @Watch('promptSubmit')
  @Emit('submitForm')
  private async emitSubmit () : Promise<AdvancedSearchI> {
    if (await this.isValidForm()) {
      return {
        compName: this.compName,
        firstName: this.applicantFirstName,
        lastName: this.applicantLastName,
        submittedStartDate: this.startDate,
        submittedEndDate: this.endDate
      }
    } return null
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
