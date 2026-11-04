<template>
  <div id="existing-request-search">
    <!-- Advanced Search Dialog -->
    <advanced-search
      attach="#existing-request-search"
      :dialog="advancedSearchDialog"
      @closeDialog="advancedSearchDialog = false"
    />

    <v-row no-gutters>
      <!-- Help Content -->
      <v-col
        v-if="!isMobile"
        cols="12"
        md="3"
        lg="3"
        class="existing-request-info copy-small"
      >
        <SearchHelpContent />
      </v-col>

      <!-- Existing Request Search -->
      <v-col
        cols="12"
        md="9"
        lg="9"
      >
        <v-form
          ref="existingNrForm"
          v-model="isValid"
          lazy-validation
          class="pa-10"
          @submit="handleSubmit()"
        >
          <!-- FIRST LINE -->
          <v-row no-gutters>
            <v-col
              v-if="!isMobile"
              cols="1"
              class="max-width"
            />
            <v-col
              cols="11"
              class="h6"
            >
              To manage an existing Name Request, enter your NR Number and either the Applicant’s Phone Number or Email:
            </v-col>
          </v-row>

          <!-- SECOND LINE -->
          <v-row
            v-if="errorMessage"
            class="mt-4"
            no-gutters
          >
            <v-col
              v-if="!isMobile"
              cols="1"
              class="max-width"
            />
            <v-col
              cols="11"
              class="error-message copy-small"
              v-html="errorMessage"
            />
          </v-row>

          <!-- THIRD LINE -->
          <v-row
            class="mt-4"
            no-gutters
            align="center"
          >
            <v-col
              v-if="!isMobile"
              cols="1"
              class="max-width"
            >
              <img
                src="@/assets/images/number1.svg"
                width="34"
                height="34"
              >
            </v-col>
            <v-col class="max-height">
              <v-text-field
                id="nr-num-text-field"
                :rules="nrRules"
                :value="getExistingRequestSearch.nrNum"
                class="copy-normal"
                filled
                label="NR Number"
                hint="Example: NR 1234567"
                persistent-hint
                validate-on-blur
                @input="handleExistingRequestSearch('nrNum', $event)"
              />
            </v-col>
          </v-row>

          <!-- FOURTH LINE -->
          <v-row
            class="mt-6"
            no-gutters
            align="center"
          >
            <v-col
              v-if="!isMobile"
              cols="1"
              class="max-width"
            >
              <img
                src="@/assets/images/number2.svg"
                width="34"
                height="34"
              >
            </v-col>
            <v-col class="max-height">
              <v-text-field
                id="phone-number-text-field"
                :rules="phoneRules"
                :value="getExistingRequestSearch.phoneNumber"
                class="copy-normal"
                filled
                label="Applicant's Phone Number"
                hint="Example: 555-555-5555"
                persistent-hint
                validate-on-blur
                @input="handleExistingRequestSearch('phoneNumber', $event)"
              />
            </v-col>
            <v-col
              cols="12"
              md="auto"
              lg="auto"
              class="copy-normal text-center shrink mx-4 mt-6 mb-4"
            >
              or
            </v-col>
            <v-col class="max-height">
              <v-text-field
                id="email-address-text-field"
                :rules="emailRules"
                :value="getExistingRequestSearch.emailAddress"
                class="copy-normal"
                filled
                label="Applicant's Notification Email"
                hint="Example: name@email.com"
                persistent-hint
                validate-on-blur
                @input="handleExistingRequestSearch('emailAddress', $event)"
              />
            </v-col>
          </v-row>

          <!-- FIFTH LINE -->
          <v-row
            class="mt-9"
            no-gutters
          >
            <v-col class="text-center">
              <v-btn
                id="retrieve-name-btn"
                :class="{ 'mobile-btn' : isMobile }"
                @click="handleSubmit()"
              >
                Retrieve Name Request
              </v-btn>
            </v-col>
          </v-row>

          <!-- SIXTH LINE - show this only when a user has a token -->
          <v-row
            v-if="isAuthenticated"
            class="mt-3"
            no-gutters
          >
            <v-col class="text-center">
              <v-btn
                id="advanced-search-btn"
                class="button-text"
                text
                @click="advancedSearchDialog = true"
              >
                I don't know my NR Number
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-col>

      <!-- Help Content -->
      <v-col
        v-if="isMobile"
        cols="12"
        md="3"
        lg="3"
        class="existing-request-info copy-small"
      >
        <SearchHelpContent />
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import AdvancedSearch from '@/components/dialogs/advanced-search.vue'
import SearchHelpContent from '@/components/existing-request/search-help-content.vue'
import { FormType, NameRequestI, ExistingRequestSearchI } from '@/interfaces'
import { ActionBindingIF } from '@/interfaces/store-interfaces'

@Component({
  components: {
    AdvancedSearch,
    SearchHelpContent
  }
})
export default class ExistingRequestSearch extends Vue {
  // Refs
  $refs!: {
    existingNrForm: FormType
  }

  @Getter(useStore) isAuthenticated!: boolean
  @Getter(useStore) getNr!: Partial<NameRequestI>
  @Getter(useStore) getExistingRequestSearch!: ExistingRequestSearchI
  @Getter(useStore) isMobile!: boolean

  @Action(useStore) findNameRequest!: ActionBindingIF
  @Action(useStore) setExistingRequestSearch!: ActionBindingIF
  @Action(useStore) setNameRequest!: ActionBindingIF

  errorMessage = ''
  isValid = false
  advancedSearchDialog = false

  // eslint-disable-next-line no-useless-escape
  private NR_REGEX = /^(NR\ ?L?|L?)?([\d]{6,8})$/

  mounted () {
    this.$nextTick(() => {
      if (this.$el?.querySelector instanceof Function) {
        // add classname to button text (for more detail in breadcrumbs)
        const retrieveNrBtn = this.$el.querySelector('#retrieve-name-btn > span')
        if (retrieveNrBtn) retrieveNrBtn.classList.add('retrieve-nr-btn')
      }
    })

    if (this.getNr?.failed) {
      this.errorMessage = this.getNr.text
      this.setNameRequest({})
      return
    }

    for (let key of ['emailAddress', 'phoneNumber']) {
      this.setExistingRequestSearch({ key, value: '' })
    }
  }

  nrRules = [
    v => this.NR_REGEX.test(v) || 'Please enter a valid NR number'
  ]
  emailRules = []
  phoneRules = []

  async handleSubmit (): Promise<void> {
    this.applyRules()
    this.$refs.existingNrForm.validate()
    await this.$nextTick()

    if (this.isValid) {
      await this.findNameRequest(null)
      if (this.getNr?.failed) {
        // capture error text and then clear out the NR data
        this.errorMessage = this.getNr.text
        this.setNameRequest({})
      }
    }
  }

  /** Apply the field rules to request search inputs. */
  private applyRules (): void {
    const { emailAddress, phoneNumber } = this.getExistingRequestSearch

    this.phoneRules = (phoneNumber || !emailAddress)
      ? [
        v => !!v || 'Please enter a phone number',
        v => (v.length <= 30) || 'Cannot exceed 30 characters'
      ]
      : []

    this.emailRules = (!phoneNumber || emailAddress)
      ? [
        v => !!v || 'Please enter an email',
        v => (/.+@.+\..+/.test(v)) || 'A valid email is required'
      ]
      : []
  }

  handleExistingRequestSearch (key: string, value: string) {
    // uppercase the NR number
    if (key === 'nrNum') value = value.toUpperCase()

    this.$refs.existingNrForm.resetValidation()
    this.setExistingRequestSearch({ key, value })
    this.errorMessage = ''
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';

.existing-request-info {
  background-color: $gray1;
  width: 100%;
  position: relative !important;
}

/* Helper info column pointer */
.existing-request-info:after{
  content: "";
  position:absolute;
  top:5.75rem;
  left:100%;
  border-top: 18px solid transparent !important;
  border-bottom: 18px solid transparent !important;
  border-left: 14px solid $gray1 !important;
}

.col.max-width {
  max-width: 3rem;
}

.col.max-height {
  max-height: 60px;
}

#retrieve-name-btn {
  min-height: 45px !important;
  padding: 0 30px !important;
  font-size: $px-16 !important;
}

.mobile-btn {
  width: 17rem !important;
}
</style>
