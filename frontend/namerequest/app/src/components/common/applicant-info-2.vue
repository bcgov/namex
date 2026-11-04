<template>
  <v-form
    id="applicant-info-2-form"
    ref="step2"
    v-model="isValid"
  >
    <v-container
      id="applicant-info-2"
      fluid
      class="pa-0 mt-6"
    >
      <v-row>
        <v-col
          cols="12"
          md="2"
          lg="2"
          class="h6 align-self-start"
        >
          Contact Info
        </v-col>

        <!--EMAIL ADDRESS-->
        <v-col
          cols="12"
          md="5"
          lg="5"
        >
          <v-text-field
            id="emailAddress"
            :messages="messages['email']"
            :rules="emailRules"
            :validate-on-blur="true"
            :value="getApplicant.emailAddress"
            filled
            hide-details="auto"
            :name="Math.random()"
            autocomplete="chrome-off"
            label="Email Address (for notifications)"
            @blur="messages = {}"
            @input="updateApplicant('emailAddress', $event)"
          />
        </v-col>
        <v-col
          cols="5"
          class="py-0"
        />
      </v-row>

      <v-row class="mt-0">
        <v-col
          cols="12"
          md="2"
          lg="2"
        />

        <!--PHONE NUMBER-->
        <v-col
          cols="12"
          md="5"
          lg="5"
        >
          <v-text-field
            id="phoneNumber"
            :messages="messages['phone']"
            :value="getApplicant.phoneNumber"
            type="tel"
            :rules="phoneRules"
            :name="Math.random()"
            autocomplete="chrome-off"
            filled
            hide-details="auto"
            label="Phone Number"
            @blur="messages = {}"
            @input="updateApplicant('phoneNumber', $event.trim())"
          />
        </v-col>

        <!--FAX NUMBER-->
        <v-col
          cols="12"
          md="5"
          lg="5"
        >
          <v-text-field
            id="faxNumber"
            :messages="messages['fax']"
            :value="getApplicant.faxNumber"
            :rules="faxRules"
            :name="Math.random()"
            autocomplete="chrome-off"
            filled
            hide-details="auto"
            label="Fax Number (Optional)"
            @blur="messages = {}"
            @input="updateApplicant('faxNumber', $event)"
          />
        </v-col>
      </v-row>

      <v-row v-if="showAllFields">
        <v-col
          cols="12"
          md="2"
          lg="2"
          class="h6"
        >
          About Your Business
        </v-col>

        <!--NATURE OF BUSINESS-->
        <v-col
          cols="12"
          md="5"
          lg="5"
          align-self="start"
        >
          <v-tooltip
            top
            content-class="top-tooltip"
            transition="fade-transition"
            :disabled="isMobile"
          >
            <template #activator="{ on }">
              <div v-on="on">
                <v-textarea
                  id="natureBusinessInfo"
                  :messages="messages['nature']"
                  :rules="businessNatureRules"
                  :value="getNrData.natureBusinessInfo"
                  name="natureBusinessInfo"
                  filled
                  hide-details="auto"
                  label="Nature of Business"
                  no-resize
                  rows="3"
                  @blur="messages = {}"
                  @input="updateNrData('natureBusinessInfo', $event)"
                />
              </div>
            </template>
            <span>
              Nature of business information collected is for name review purposes only.
              What is entered here does not limit the business activities of your company.
            </span>
          </v-tooltip>
        </v-col>

        <!--ADDITIONAL INFORMATION-->
        <v-col
          cols="12"
          md="5"
          lg="5"
          align-self="start"
        >
          <v-tooltip
            top
            content-class="top-tooltip"
            transition="fade-transition"
            :disabled="isMobile"
          >
            <template #activator="{ on }">
              <div v-on="on">
                <v-textarea
                  id="additionalInfo"
                  :messages="messages['additional']"
                  :value="getNrData.additionalInfo"
                  :rules="additionalInfoRules"
                  name="additionalInfo"
                  filled
                  hide-details="auto"
                  label="Additional Information (Optional)"
                  no-resize
                  rows="3"
                  @blur="messages = {}"
                  @input="updateNrData('additionalInfo', $event)"
                />
              </div>
            </template>
            <span>
              Enter information you think Registries staff should know to help them review your
              name such as details regarding previous name requests, related business, etc.
            </span>
          </v-tooltip>
        </v-col>
        <v-col
          cols="12"
          md="2"
          lg="2"
        />

        <!--TRADEMARK-->
        <v-col
          cols="12"
          md="5"
          lg="5"
        >
          <v-tooltip
            top
            content-class="top-tooltip"
            transition="fade-transition"
            :disabled="isMobile"
          >
            <template #activator="{ on }">
              <div v-on="on">
                <v-text-field
                  id="tradeMark"
                  :messages="messages['tradeMark']"
                  :value="getNrData.tradeMark"
                  :rules="trademarkRules"
                  :name="Math.random()"
                  autocomplete="chrome-off"
                  filled
                  hide-details="auto"
                  label="Registered Canadian Trademark (Optional)"
                  @blur="messages = {}"
                  @input="updateNrData('tradeMark', $event)"
                />
              </div>
            </template>
            <span>
              If your name is a registered trademark in Canada, enter your trademark name and registration number.
            </span>
          </v-tooltip>
        </v-col>
      </v-row>

      <v-row class="align-center mt-2 mb-0">
        <v-col
          cols="12"
          md="2"
          lg="2"
        />

        <!--PRIORITY REQUEST-->
        <v-col
          cols="12"
          md="5"
          lg="5"
        >
          <v-tooltip
            top
            content-class="top-tooltip"
            transition="fade-transition"
            :disabled="isMobile"
          >
            <template #activator="{ on }">
              <div v-on="on">
                <v-checkbox
                  v-if="getShowPriorityRequest"
                  v-model="priorityRequest"
                  hide-details
                  class="pre-wrap mt-0 pt-0"
                  :disabled="!enablePriorityCheckbox"
                >
                  <template #label>
                    Make this a Priority Request <b>($100.00)</b>
                  </template>
                </v-checkbox>
              </div>
            </template>
            <span v-if="enablePriorityCheckbox">
              Priority name requests are typically reviewed within {{ getPriorityWaitTime }} business days.
            </span>
            <span v-else>
              Due to the on-going labour dispute between the government and its employees,
              priority filings are temporarily disabled.
            </span>
          </v-tooltip>
        </v-col>

        <ApplicantInfoNav @nextAction="nextAction()" />
      </v-row>
    </v-container>
  </v-form>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import ApplicantInfoNav from '@/components/common/applicant-info-nav.vue'
import { ApplicantI } from '@/interfaces'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { NrState } from '@/enums'
import { GetFeatureFlag } from '@/plugins'

@Component({
  components: {
    ApplicantInfoNav
  }
})
export default class ApplicantInfo2 extends Vue {
  @Getter(useStore) getApplicant!: ApplicantI
  @Getter(useStore) getEditMode!: boolean
  @Getter(useStore) getNrData!: any
  @Getter(useStore) getNrState!: NrState
  @Getter(useStore) getPriorityRequest!: boolean
  @Getter(useStore) getPriorityWaitTime!: string | number
  @Getter(useStore) getShowPriorityRequest!: boolean
  @Getter(useStore) isMobile!: boolean

  @Action(useStore) setApplicantDetails: ActionBindingIF
  @Action(useStore) setIsLoadingSubmission!: ActionBindingIF
  @Action(useStore) setNRData!: ActionBindingIF
  @Action(useStore) setPriorityRequest!: ActionBindingIF
  @Action(useStore) submit!: ActionBindingIF

  additionalInfoRules = [
    v => (!v || v.length <= 120) || 'Cannot exceed 120 characters'
  ]
  businessNatureRules = [
    v => !!v || 'Required field',
    v => (!v || v.length <= 1000) || 'Cannot exceed 1000 characters'
  ]
  emailRules = [
    (v: string) => !!v || 'Required field',
    (v: string) => {
      // eslint-disable-next-line max-len
      const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      return pattern.test(v) || 'Not a valid email'
    },
    (v: string) => (!v || v.length <= 75) || 'Cannot exceed 75 characters'
  ]
  phoneRules = [
    v => !!v || 'Required field',
    v => (!v || v.length <= 30) || 'Cannot exceed 30 characters'
  ]
  faxRules = [
    v => (!v || v.length <= 30) || 'Cannot exceed 30 characters'
  ]
  trademarkRules = [
    v => (!v || v.length <= 100) || 'Cannot exceed 100 characters'
  ]
  error = false
  isValid = false
  loading = false
  messages = {}

  /** Whether priority checkbox should be enabled. */
  get enablePriorityCheckbox (): boolean {
    return !!GetFeatureFlag('enable-priority-checkbox')
  }

  @Watch('xproJurisdiction')
  async hanldeJurisdiction (newVal, oldVal) {
    if (newVal !== oldVal) {
      await this.$nextTick()
      this.validate()
    }
  }

  get priorityRequest (): boolean {
    return this.getPriorityRequest
  }

  set priorityRequest (value: boolean) {
    this.setPriorityRequest(value)
  }

  get showAllFields (): boolean {
    return (!this.getEditMode || this.getNrState === NrState.DRAFT)
  }

  get xproJurisdiction () {
    return (this.getNrData || {}).xproJurisdiction
  }

  setError (error) {
    this.error = error
  }

  updateApplicant (key, value) {
    this.setApplicantDetails({ key, value })
  }

  updateNrData (key, value) {
    this.setNRData({ key, value })
  }

  validate (): boolean {
    return (this.$refs.step2 && (this.$refs.step2 as any).validate())
  }

  @Watch('isValid')
  onValidChanged (val: boolean) {
    if (val) {
      this.$nextTick(() => {
        if (this.$el?.querySelector instanceof Function) {
          // add classname to button text (for more detail in breadcrumbs)
          const selfReviewBackBtn = this.$el.querySelector('.submit-back-btn > span')
          if (selfReviewBackBtn) selfReviewBackBtn.classList.add('self-review-back-btn')
          const selfReviewConfirmBtn = this.$el.querySelector('.submit-continue-btn > span')
          if (selfReviewConfirmBtn) selfReviewConfirmBtn.classList.add('self-review-confirm-btn')
        }
      })
    }
  }

  async nextAction () {
    this.setIsLoadingSubmission(true)
    this.validate()
    if (this.isValid) await this.submit(null)
    // hang on to the loading state for a bit
    // to prevent users clicking button again while next component displays
    setTimeout(() => this.setIsLoadingSubmission(false), 1000)
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/theme";

::v-deep .v-textarea textarea {
  line-height: 1.375rem !important;
  font-size: $px-14 !important;
}

// disabled checkbox label
::v-deep .v-input--is-disabled label {
  color: $disabled-action !important;
}
</style>
