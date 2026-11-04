<template>
  <v-dialog
    id="advanced-search-dialog"
    v-model="dialog"
    max-width="55rem"
    persistent
    :attach="attach"
  >
    <v-card :class="{'retrieve-card-height': isTabRetrieve, 'tab-card-height': !isTabRetrieve}">
      <v-btn
        icon
        large
        class="dialog-close"
        @click="emitClose()"
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>

      <v-tabs id="advanced-search-tabs">
        <v-tabs-items
          v-model="advSearchTab"
          touchless
        >
          <!-- Advanced Search Form -->
          <v-tab-item class="set-height-tab mb-2">
            <v-card-title>
              <span>Find an Existing Name Request</span>
            </v-card-title>

            <v-card-text class="copy-normal py-4">
              Find an existing Name Request by searching for <strong>one or more</strong> of the following criteria:
            </v-card-text>

            <!-- Validation error message -->
            <div class="my-n2">
              <span
                v-if="invalidSearch"
                class="copy-small error-message"
              >Enter at least one search criteria</span>
              <br v-else> <!-- Preserve Spacing when no errors present -->
            </div>

            <AdvancedSearchForm
              class="mt-4"
              :promptSubmit="toggleSearchSubmit"
              :advSearchDialogState="dialog"
              @isInvalid="invalidSearch = $event"
              @submitForm="submitForm($event)"
              @closeDialog="emitClose()"
            />
          </v-tab-item>

          <!-- Advanced Search Table -->
          <v-tab-item class="set-height-tab mb-2">
            <v-card-title>
              Name Requests Found <span class="searchResultCounter pl-2">({{ searchResultCount }})</span>
            </v-card-title>

            <v-card-text class="copy-normal pt-5">
              Select the Name Request you would like to retrieve. To access the detailed summary screen, <br> you will
              need the email address of phone number of the Applicant.
            </v-card-text>

            <AdvancedSearchTable
              class="mt-6"
              :nameRequestResults="nameRequestResults"
              :isApplicantNameSearch="isApplicantNameSearch"
              @selectNameRequest="advSearchTab = AdvancedSearchTabs.ADVANCED_SEARCH_RETRIEVE"
            />
          </v-tab-item>

          <!-- Advanced Search Retrieve Form -->
          <v-tab-item>
            <v-card-title>
              <span>Retrieve Name Request</span>
            </v-card-title>

            <v-card-text class="copy-normal pt-5">
              To view the details and status of this Name Request, please enter the <strong>email address or phone
                number</strong> of the Applicant.
            </v-card-text>

            <AdvancedSearchRetrieve
              class="mt-6"
              :promptSubmit="toggleRetrieveSubmit"
              :advSearchTabState="advSearchTab"
              @closeDialog="emitClose()"
            />
          </v-tab-item>

          <!-- Too Many Results -->
          <v-tab-item>
            <v-card-text class="copy-normal results-text mt-7 py-4">
              <h3>Too Many Name Requests Found</h3>
              <span class="my-6">Your search returned more than 1000 results.</span>
              <span class="mb-4">Please return to the previous screen and narrow your search by selecting more than
                one search criteria and/or reducing your date range.</span>
            </v-card-text>
          </v-tab-item>

          <!-- No Results Found -->
          <v-tab-item>
            <v-card-text class="copy-normal results-text mt-6 py-6">
              <h3>No Name Requests Found</h3>
              <span class="my-6">Your search returned no results.</span>
              <span class="mb-4">Please return to the previous screen and try your search again.</span>
            </v-card-text>
          </v-tab-item>
        </v-tabs-items>
      </v-tabs>

      <v-card-actions
        id="advanced-search-actions"
        class="justify-center pa-0"
      >
        <v-row no-gutters>
          <v-col>
            <v-btn
              id="adv-search-btn-1"
              class="mr-2"
              :class="[{ 'button-blue': isTabResultsTable || isTabRetrieve }, isMobile ? 'mobile-btn' : 'float-right']"
              text
              outlined
              @click="advSearchBtn1Actions()"
            >
              <span :class="isTabSearchForm ? 'pl-2' : 'pr-2'">
                <v-icon v-if="!isTabSearchForm">mdi-chevron-left</v-icon>
                {{ advSearchBtn1Text }}
                <v-icon v-if="isTabSearchForm">mdi-chevron-right</v-icon>
              </span>
            </v-btn>
          </v-col>
          <v-col>
            <v-btn
              id="adv-search-btn-2"
              :class="[{ 'button-blue' : !isTabRetrieve }, { 'mobile-btn' : isMobile }]"
              text
              outlined
              @click="advSearchBtn2Actions()"
            >
              <span class="px-3">
                {{ advSearchBtn2Text }}<v-icon v-if="isTabRetrieve">mdi-chevron-right</v-icon>
              </span>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang='ts'>
import { Component, Emit, Prop, Watch, Vue } from 'vue-property-decorator'
import NamexServices from '@/services/namex-services'
import { Getter } from 'pinia-class'
import { useStore } from '@/store'
import { AdvancedSearchForm, AdvancedSearchRetrieve, AdvancedSearchTable } from '@/components/advanced-search'
import { AdvancedSearchI } from '@/interfaces/models'
import { AdvancedSearchTabs } from '@/enums'

@Component({
  components: {
    AdvancedSearchForm,
    AdvancedSearchRetrieve,
    AdvancedSearchTable
  }
})
export default class AdvancedSearch extends Vue {
  // enum for template
  readonly AdvancedSearchTabs = AdvancedSearchTabs

  /** Prop to display the dialog. */
  @Prop() readonly dialog: boolean

  /** Prop to provide attachment selector. */
  @Prop() readonly attach: string

  @Getter(useStore) isMobile!: boolean

  // Local Properties
  private advSearchTab = 0
  private toggleSearchSubmit = false
  private toggleRetrieveSubmit = false
  private invalidSearch = false
  private searchResultCount = 0
  private nameRequestResults = []
  private isApplicantNameSearch = false

  /** The current action button text dependant on tab state. */
  private get advSearchBtn1Text (): string {
    switch (this.advSearchTab) {
      case AdvancedSearchTabs.ADVANCED_SEARCH_FORM: return 'Find Name Request'
      case AdvancedSearchTabs.ADVANCED_SEARCH_TABLE: return `Back`
      default: return 'Back'
    }
  }

  /** The current cancel button text dependant on tab state. */
  private get advSearchBtn2Text (): string {
    switch (this.advSearchTab) {
      case AdvancedSearchTabs.ADVANCED_SEARCH_FORM: return 'Cancel'
      case AdvancedSearchTabs.ADVANCED_SEARCH_TABLE: return `Exit`
      case AdvancedSearchTabs.ADVANCED_SEARCH_RETRIEVE: return `Retrieve Name Request`
      default: return 'Exit'
    }
  }

  /** Is true when NR retrieval is the current tab. */
  private get isTabSearchForm (): boolean {
    return this.advSearchTab === AdvancedSearchTabs.ADVANCED_SEARCH_FORM
  }

  /** Is true when NR retrieval is the current tab. */
  private get isTabResultsTable (): boolean {
    return this.advSearchTab === AdvancedSearchTabs.ADVANCED_SEARCH_TABLE
  }

  /** Is true when NR retrieval is the current tab. */
  private get isTabRetrieve (): boolean {
    return this.advSearchTab === AdvancedSearchTabs.ADVANCED_SEARCH_RETRIEVE
  }

  /** Advanced search btn 1 actions. */
  private advSearchBtn1Actions (): void {
    switch (this.advSearchTab) {
      case AdvancedSearchTabs.ADVANCED_SEARCH_FORM: this.toggleSearchSubmit = !this.toggleSearchSubmit
        break
      case AdvancedSearchTabs.ADVANCED_SEARCH_TABLE: this.advSearchTab--
        break
      case AdvancedSearchTabs.ADVANCED_SEARCH_RETRIEVE: this.advSearchTab--
        break
      default: this.advSearchTab = AdvancedSearchTabs.ADVANCED_SEARCH_FORM
    }
  }

  /** Advanced search btn 2 actions. */
  private advSearchBtn2Actions (): void {
    switch (this.advSearchTab) {
      case AdvancedSearchTabs.ADVANCED_SEARCH_RETRIEVE: this.toggleRetrieveSubmit = !this.toggleRetrieveSubmit
        break
      default: this.emitClose()
    }
  }

  /** Handle the response data from an Advanced Name Request search.
   * @param formData The form data to provide the search query parameters.
   */
  private async searchHandler (formData: AdvancedSearchI): Promise<void> {
    // Fetch search results count
    let results = await NamexServices.searchNameRequests(formData, true, true)
    this.searchResultCount = results.response.numFound

    // Fetch the Name Requests when the count is 1000 or less.
    if (this.searchResultCount <= 1000) {
      results = await NamexServices.searchNameRequests(formData, true)
      this.nameRequestResults = results.nameRequests[0]
    }

    // Navigate to the appropriate tab based on search results
    switch (true) {
      case (this.searchResultCount > 1000): this.advSearchTab = AdvancedSearchTabs.ADVANCED_SEARCH_INVALID
        break
      case (this.searchResultCount > 0): this.advSearchTab = AdvancedSearchTabs.ADVANCED_SEARCH_TABLE
        break
      default: this.advSearchTab = AdvancedSearchTabs.ADVANCED_SEARCH_NO_RESULTS
    }
  }

  /** Validate criteria and submit form for request. */
  private async submitForm (formData: AdvancedSearchI): Promise<void> {
    // Validate minimum search criteria
    if (!formData) return

    // Set flag if the search criteria contains Applicant Name
    this.isApplicantNameSearch = !!formData.lastName
    // Set loading state and perform a search for the potential NR Match count.
    this.$root.$emit('showSpinner', true)
    await this.searchHandler(formData)
    this.$root.$emit('showSpinner', false)
  }

  @Watch('dialog')
  @Watch('advSearchTab')
  private formReset (): void {
    this.invalidSearch = false
  }

  @Emit('closeDialog')
  private emitClose (): void {
    this.advSearchTab = 0
    this.invalidSearch = false
    this.toggleSearchSubmit = false
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';
.tab-card-height {
  min-height: 36rem;
}

.retrieve-card-height {
  max-height: 32rem;
}

.set-height-tab {
  min-height: 29rem;
}

#advanced-search-actions {
  .v-btn {
    min-width: 100px !important;
  }
}

.searchResultCounter {
  font-weight: normal;
}

.results-text {
  height: 18rem;
  padding-left: 80px !important;
  padding-right: 80px !important;
  text-align: center;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
}

.mobile-btn {
  width: 16rem;
  margin-top: 10px
}

::v-deep .v-tabs > .v-tabs-bar {
  display: none;
}

::v-deep .v-btn:not(.dialog-close) .v-icon.v-icon {
  font-size: $px-20 !important;
}

::v-deep .v-btn__content {
  line-height: inherit;
}
</style>
