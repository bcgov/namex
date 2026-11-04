<template>
  <v-container
    id="name-check-main-container"
    class="white pa-0 rounded"
  >
    <name-check-issues-dialog
      attach="#app"
      :display="showNameCheckIssuesDialog"
      :options="dialogOptions"
      @proceed="dialogSubmit($event)"
    />
    <v-row
      class="pl-10 pt-6"
      no-gutters
    >
      <v-col
        cols="11"
        class="h6 py-0 mt-1"
      >
        You are searching for a name for a
        {{ entityText === ' BC Corporation' && location === ' BC' ? '' : ' ' + location }}
        {{ entityText }}
      </v-col>
    </v-row>
    <v-row
      class="px-10 pt-6"
      no-gutters
    >
      <v-col
        :class="{'pr-8': isXproFlow}"
        cols="12"
        lg="7"
      >
        <NameInput
          :hint="nameInputHint"
          :isReadOnly="isXproFlow"
        />
      </v-col>
      <v-col
        v-if="showDesignationSelect"
        :class="{'pl-3': !isMobile}"
        cols="12"
        lg="3"
      >
        <v-select
          v-model="designation"
          filled
          :items="designationOptions"
          label="Select a Designation"
          style="line-height: 20px;"
        />
      </v-col>
      <v-col
        v-if="!isXproFlow"
        class="pl-3 pt-3"
        cols="1"
      >
        <v-btn
          id="search-name-btn"
          class="outlined px-5 py-4"
          :class="{'mobile-wide-btn': isMobile}"
          outlined
          @click="checkAgain()"
        >
          <v-icon
            left
            size="1.5rem"
          >
            mdi-magnify
          </v-icon>
          Check this Name
        </v-btn>
      </v-col>
    </v-row>
    <v-container
      id="name-check-lower-container"
      class="rounded copy-normal mt-5 pa-0 name-check"
    >
      <v-row
        v-if="hasNameLengthError"
        no-gutters
        justify="center"
        class="pt-8"
      >
        <v-col
          id="name-check-header"
          cols="auto"
        >
          <b>Showing Results for:</b>
        </v-col>
      </v-row>
      <v-row
        v-if="hasNameLengthError"
        no-gutters
        justify="center"
      >
        <v-col
          id="name-check-title"
          cols="auto"
        >
          <b>{{ originalName }}</b>
        </v-col>
      </v-row>
      <v-row
        v-if="hasNameLengthError"
        id="name-check-verdict"
        class="white mt-7 pa-2"
        no-gutters
        align="center"
      >
        <v-progress-circular
          v-if="loadingStructureCheck"
          color="primary"
          indeterminate
          size="30"
          width="3"
        />
        <v-icon
          v-else
          class="check-tab-icon pl-2"
          :color="tabIconVerdict.color"
          size="2rem"
        >
          {{ tabIconVerdict.icon }}
        </v-icon>
        <span class="pl-2">
          {{ nameCheckVerdict }}
        </span>
      </v-row>
      <v-container
        v-if="(hasIssuesConflictAlert || hasIssuesConflictCaution ||
          hasIssuesStructureAlert || hasIssuesStructureCaution ||
          loadingStructureCheck) && hasNameLengthError"
        id="name-check-tabs-container"
        class="ma-0 pt-7"
      >
        <v-tabs
          id="name-check-tabs"
          v-model="checks"
          no-gutters
          :active-class="isXproFlow? 'active-tab no-border-top' : 'active-tab'"
          centered
          grow
          height="7rem"
          hide-slider
          style="border-radius: 4px 4px 0 0;"
        >
          <v-tab
            v-if="!isXproFlow"
            id="structure-tab"
            href="#structure-check"
            class="upper-border px-0 pt-3"
            :ripple="false"
          >
            <div style="width: 100%;">
              <name-check-tab-content
                :loading="loadingStructureCheck"
                :subtitle="subTitleStructure"
                :tabIcon="tabIconStructure.icon"
                :title="'Name Structure Check'"
              />
              <div
                v-if="checks === 'conflicts-check'"
                id="box-shadow-filler-unactive-tab"
              />
            </div>
          </v-tab>
          <v-tab
            id="conflicts-tab"
            href="#conflicts-check"
            class="upper-border px-0 pt-3"
            :ripple="false"
          >
            <div style="width: 100%;">
              <name-check-tab-content
                :loading="isAnalyzeConflictsPending"
                :subtitle="subTitleConflict"
                :tabIcon="tabIconConflict.icon"
                :title="'Similar Name Check'"
              />
              <div
                v-if="checks === 'structure-check'"
                id="box-shadow-filler-unactive-tab"
              />
            </div>
          </v-tab>
        </v-tabs>
        <div id="box-shadow-filler-tab-item" />
        <v-tabs-items
          v-model="checks"
          class="rounded-b tab-items pa-5 pt-6"
          :class="checks === 'structure-check' ? 'rounded-top-right' : 'rounded-top-left'"
          touchless
        >
          <v-tab-item value="structure-check">
            <v-row
              no-gutters
              class="pr-16 pb-6 name-check-info-text"
              :class="{'pl-12': !isMobile}"
            >
              <v-col cols="auto">
                <v-icon>mdi-information-outline</v-icon>
              </v-col>
              <v-col class="pl-2">
                <span v-html="infoTextTab" />
              </v-col>
            </v-row>
            <NameCheckConflicts
              :items="itemsStructure"
              @clear-error="clearError"
              @retry="retry"
            />
          </v-tab-item>
          <v-tab-item value="conflicts-check">
            <v-row
              no-gutters
              class="pr-16 pb-7 name-check-info-text"
              :class="{'pl-12': !isMobile}"
            >
              <v-col cols="auto">
                <v-icon>mdi-information-outline</v-icon>
              </v-col>
              <v-col class="pl-2">
                <p
                  class="ma-0"
                  v-html="infoTextTab"
                />
                <div v-if="!isXproFlow">
                  <p class="ma-0 pt-2">
                    <a
                      class="txt-link"
                      text
                      @click="expandHelpTxt = !expandHelpTxt"
                    >
                      {{ expandBtnTxt }}
                    </a>
                  </p>
                  <div v-if="expandHelpTxt">
                    <p class="ma-0 pt-7">
                      The Similar Name Check searches the Corporate Register only;
                      it may not find ALL similarly named businesses. This register
                      includes the names of corporations incorporated or registered
                      extraprovincially in British Columbia. It does not include names
                      of British Columbia firms, trademarks or corporations registered
                      outside British Columbia.
                    </p>
                    <p class="ma-0 pt-7">
                      Do not commit to any name before it is reviewed by staff.
                    </p>
                    <p class="ma-0 pt-7">
                      If you want to ensure your name is not used outside of British
                      Columbia, you could also access the Trademarks database at
                      <a
                        class="txt-link"
                        :href="tradeMarkDBLink"
                        target="_blank"
                      >
                        <span>www.strategis.ic.gc.ca</span>
                      </a>
                      &nbsp;
                      <a
                        :href="tradeMarkDBLink"
                        style="text-decoration: none;"
                        target="_blank"
                      >
                        <v-icon
                          color="primary"
                          small
                        >mdi-open-in-new</v-icon>
                      </a>
                      , or you may wish to search other
                      jurisdictions in Canada. Most public business and trademark
                      registers in Canada are reflected in the NUANS database, which may
                      be searched for a fee through private search firms.
                    </p>
                    <p class="ma-0 pt-7">
                      You should also research your desired name by searching the internet,
                      social media, and relevant internet domain names if these are
                      considerations for your business.
                    </p>
                  </div>
                </div>
              </v-col>
            </v-row>
            <NameCheckConflicts
              :items="itemsConflict"
              @clear-error="clearError"
              @retry="retry"
            />
          </v-tab-item>
        </v-tabs-items>
      </v-container>
      <v-row
        v-if="hasNameLengthError"
        no-gutters
        class="pt-3 name-check-info-text-no-border"
      >
        <v-col cols="auto">
          <v-icon>mdi-information-outline</v-icon>
        </v-col>
        <v-col class="pl-2">
          <span>{{ bottomText }}</span>
        </v-col>
      </v-row>
      <v-row
        no-gutters
        class="pa-10 pt-5"
      >
        <v-col>
          <v-btn
            id="name-check-start-over-btn"
            class="outlined"
            outlined
            @click="back()"
          >
            Start Over
          </v-btn>
        </v-col>
        <v-col>
          <v-btn
            v-if="hasNameLengthError"
            id="name-check-submit-btn"
            class="float-right"
            @click="dialogCheck()"
          >
            Submit this Name for Review
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import NameCheckIssuesDialog from '@/components/dialogs/name-check-issues.vue'
import MainContainer from '@/components/new-request/main-container.vue'
import NameCheckConflicts from '@/components/new-request/name-check/name-check-conflicts.vue'
import NameCheckTabContent from '@/components/new-request/name-check/name-check-tab-content.vue'
import NameInput from '@/components/new-request/name-input.vue'
import QuickSearchNames from '@/components/new-request/name-check/quick-search-names.vue'
import { EntityTypes, NameCheckErrorType } from '@/enums'
import { ConditionalInstructionI, DialogOptionsI, NameCheckErrorI, NameCheckItemIF } from '@/interfaces'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { baseItemsConflicts, baseItemsStructure } from './resources'
import { Designations } from '@/list-data'

@Component({
  components: {
    MainContainer,
    NameCheckConflicts,
    NameCheckIssuesDialog,
    NameCheckTabContent,
    NameInput,
    QuickSearchNames
  }
})
export default class NameCheck extends Vue {
  @Getter(useStore) getConflictsConditional!: Array<string>
  @Getter(useStore) getConflictsConditionalInstructions!: Array<ConditionalInstructionI>
  @Getter(useStore) getConflictsExact!: Array<string>
  @Getter(useStore) getConflictsRestricted!: Array<string>
  @Getter(useStore) getConflictsSimilar!: Array<string>
  @Getter(useStore) getDesignation!: string
  @Getter(useStore) getDesignationsCheckUse!: Array<string>
  @Getter(useStore) getDesignationsMismatched!: Array<string>
  @Getter(useStore) getDesignationsMisplaced!: Array<string>
  @Getter(useStore) getEntityTextFromValue!: string
  @Getter(useStore) getEntityTypeCd!: EntityTypes
  @Getter(useStore) getErrors!: string[]
  @Getter(useStore) getFullName!: string
  @Getter(useStore) getLocationText!: string
  @Getter(useStore) getNameCheckErrors!: NameCheckErrorI
  @Getter(useStore) getNumbersCheckUse!: Array<string>
  @Getter(useStore) getSpecialCharacters!: Array<string>
  @Getter(useStore) isAnalyzeConflictsPending!: boolean
  @Getter(useStore) isAnalyzeDesignationPending!: boolean
  @Getter(useStore) isAnalyzeStructurePending!: boolean
  @Getter(useStore) isMissingDescriptive!: boolean
  @Getter(useStore) isMissingDesignation!: boolean
  @Getter(useStore) isMissingDistinctive!: boolean
  @Getter(useStore) isMobile!: boolean
  @Getter(useStore) isXproFlow!: boolean

  @Action(useStore) getNameAnalysis!: ActionBindingIF
  @Action(useStore) nameCheckClearError!: ActionBindingIF
  @Action(useStore) setActiveComponent!: ActionBindingIF
  @Action(useStore) setDesignation!: ActionBindingIF
  @Action(useStore) startAnalyzeName!: ActionBindingIF
  @Action(useStore) startQuickSearch!: ActionBindingIF

  config = {
    modules: {
      toolbar: false
    },
    placeholder: '',
    scrollingContainer: true
  }

  checks: string = null
  dialogOptions: DialogOptionsI = {
    acceptText: 'Submit this name for review',
    cancelText: 'Return to Results',
    icon: '',
    iconColor: '',
    title: 'Name has outstanding issues',
    text: [
      'Your name has outstanding issues. Please return ' +
      'to review the name check results to ensure your ' +
      'name has the best chance of being approved.',
      'If you have reviewed the results and would still ' +
      'like to proceed, please continue to submit your name ' +
      'for final review by our staff.'
    ]
  }
  expandHelpTxt = false
  originalName = ''
  showNameCheckIssuesDialog = false
  readonly tradeMarkDBLink = 'http://www.strategis.ic.gc.ca'

  mounted () {
    this.originalName = this.getFullName?.toUpperCase() || ''
  }

  @Watch('getFullName')
  private updateName (value: string): void {
    this.originalName = value?.toUpperCase() || ''
  }

  get bottomText (): string {
    if (!this.isXproFlow) {
      if (
        this.hasIssuesConflictAlert ||
        this.hasIssuesConflictCaution ||
        this.hasIssuesStructureAlert ||
        this.hasIssuesStructureCaution ||
        this.loadingStructureCheck
      ) {
        return 'If you wish to proceed with your name choice at any ' +
               'point you can submit your name for review. You will be able ' +
               'to enter up to three name choices as part of the name request ' +
               'submission process.'
      }
      return 'Your name has passed initial name structure and similar name checks. ' +
             'Name availability is not guaranteed until it has been reviewed by staff. ' +
             'If you wish to proceed with your name choice you can submit your name ' +
             'for review. You will be able to enter up to three name choices as part ' +
             'of the name request submission process.'
    }
    // xpro
    if (this.hasIssuesConflictAlert || this.hasIssuesConflictCaution || this.isAnalyzeConflictsPending) {
      return 'You will be able to enter up to two Assumed Name choices as part ' +
             'of the name request submission process.'
    }
    return 'Your name has passed initial similar name checks. Name ' +
           'availability is not guaranteed until it has been reviewed by staff. ' +
           'If you wish to proceed with your name choice you can submit your name ' +
           'for review. You will be able to enter up to two Assumed Name choices as ' +
           'part of the name request submission process.'
  }
  get conflictsConditional (): Array<string> {
    return this.getConflictsConditional
  }
  get conflictsConditionalInstructions (): Array<ConditionalInstructionI> {
    return this.getConflictsConditionalInstructions
  }
  get conflictsExact (): Array<string> {
    return this.getConflictsExact
  }
  get conflictsExactNum (): number {
    return this.conflictsExact.length
  }
  get conflictsRestricted (): Array<string> {
    return this.getConflictsRestricted
  }
  get conflictsSimilar (): Array<string> {
    return this.getConflictsSimilar
  }
  get conflictsSimilarNum (): number {
    return this.conflictsSimilar.length
  }
  get designation (): string {
    return this.getDesignation
  }
  set designation (value: string) {
    this.setDesignation(value)
  }
  get designationOptions (): Array<string> {
    let output: string[] = Designations[this.getEntityTypeCd]?.words
    if (this.getEntityTypeCd === EntityTypes.CC) {
      output = Designations[EntityTypes.CR].words
    }
    return output
  }
  get designationsCheckUse (): Array<string> {
    return this.getDesignationsCheckUse
  }
  get designationsMismatched (): Array<string> {
    return this.getDesignationsMismatched
  }
  get designationsMisplaced (): Array<string> {
    return this.getDesignationsMisplaced
  }
  get entityText (): string {
    return this.getEntityTextFromValue
  }
  get expandBtnTxt (): string {
    if (this.expandHelpTxt) return 'Read less about this check'
    return 'Read more about this check'
  }
  get hasConflictsConditional (): boolean {
    return this.conflictsConditional?.length > 0
  }
  get hasConflictsRestricted (): boolean {
    return this.conflictsRestricted?.length > 0
  }
  get hasDesignationsCheckUse (): boolean {
    return this.designationsCheckUse?.length > 0
  }
  get hasDesignationsMismatched (): boolean {
    return this.designationsMismatched?.length > 0
  }
  get hasDesignationsMisplaced (): boolean {
    return this.designationsMisplaced?.length > 0
  }
  get hasErrorsConflictsExact (): boolean {
    return this.getNameCheckErrors[NameCheckErrorType.ERROR_EXACT]
  }
  get hasErrorsConflictsRestricted (): boolean {
    // handles conflictsConditional too (they are from the same api call)
    return this.getNameCheckErrors[NameCheckErrorType.ERROR_RESTRICTED]
  }
  get hasErrorsConflictsSimilar (): boolean {
    return this.getNameCheckErrors[NameCheckErrorType.ERROR_SIMILAR]
  }
  get hasErrorsdesignations (): boolean {
    return this.getNameCheckErrors[NameCheckErrorType.ERROR_DESIGNATION]
  }
  get hasErrorsStructure (): boolean {
    // descriptive/distinctive
    return this.getNameCheckErrors[NameCheckErrorType.ERROR_STRUCTURE]
  }
  get hasIssuesConflictAlert (): boolean {
    return (
      this.conflictsExact?.length > 0 ||
      this.hasErrorsConflictsExact ||
      this.hasErrorsConflictsSimilar)
  }
  get hasIssuesConflictCaution (): boolean {
    return this.conflictsSimilar?.length > 0
  }
  get hasNameLengthError (): boolean {
    if (this.getErrors.includes('length')) {
      return false
    } else {
      return true
    }
  }
  get hasIssuesStructureAlert (): boolean {
    return (
      this.hasConflictsRestricted ||
      this.isMissingDesignation ||
      this.hasDesignationsMismatched ||
      this.hasDesignationsMisplaced ||
      this.hasDesignationsCheckUse ||
      this.hasSpecialCharacters ||
      this.hasErrorsConflictsRestricted ||
      this.hasErrorsdesignations ||
      this.hasErrorsStructure)
  }
  get hasIssuesStructureCaution (): boolean {
    return (
      this.hasConflictsConditional ||
      this.isMissingDistinctive ||
      this.isMissingDescriptive)
  }
  get hasNumbersCheckUse (): boolean {
    return this.getNumbersCheckUse?.length > 0
  }
  get hasSpecialCharacters (): boolean {
    return this.specialCharacters?.length > 0
  }
  get infoTextTab (): string {
    if (this.checks === 'structure-check') {
      if (this.hasIssuesStructureAlert || this.hasIssuesStructureCaution) {
        return 'This Name Structure Check helps you build a name according to the naming ' +
               'rules. We recommend resolving any name structure issues for the best chance ' +
               'of your name being approved. You can edit your name above and recheck it. ' +
               'Read helpful tips below on how to resolve each issue.'
      }
      return 'This name structure check helps you build a name according to the naming rules.'
    } else {
      if (!this.isXproFlow) {
        return 'The Similar Name Check helps you find existing BC corporations or name requests that may be ' +
               'using a similar name. The check is not exhaustive and does not guarantee name ' +
               'availability. For the best chance of having your name approved, ensure that ' +
               'your name is unique.'
      }
      return 'Extraprovincial companies must use the name in their home ' +
             'jurisdiction, unless the exact name is already in use in BC. ' +
             'Please note that the Similar Name Check is not exhaustive ' +
             'and does not guarantee name availability.'
    }
  }
  get loadingStructureCheck (): boolean {
    return this.isAnalyzeDesignationPending || this.isAnalyzeStructurePending || this.isAnalyzeConflictsPending
  }
  get nameCheckVerdict (): string {
    if (this.loadingStructureCheck || this.isAnalyzeConflictsPending) {
      return 'Verifying Results ...'
    }
    if (this.tabIconVerdict.icon === 'mdi-check-circle') {
      return 'Ready for Review'
    }
    return 'Attention Required'
  }
  get itemsConflict (): Array<NameCheckItemIF> {
    let items = []
    if (this.hasErrorsConflictsExact) {
      items.push(baseItemsConflicts.errorExact)
    }
    if (this.hasErrorsConflictsSimilar) {
      items.push(baseItemsConflicts.errorSimilar)
    }
    if (this.conflictsExact?.length > 0) {
      let newItem = this.isXproFlow
        ? { ...baseItemsConflicts.exactMatchXpro }
        : { ...baseItemsConflicts.exactMatch }
      newItem.expandedList = this.conflictsExact
      newItem.count = this.conflictsExactNum
      items.push(newItem)
    }
    if (this.conflictsSimilar?.length > 0) {
      let newItem = (
        this.isXproFlow ? { ...baseItemsConflicts.similarMatchXpro } : { ...baseItemsConflicts.similarMatch }
      )
      newItem.expandedList = this.conflictsSimilar
      newItem.count = this.conflictsSimilarNum
      items.push(newItem)
    }

    if (items.length === 0 && !this.isAnalyzeConflictsPending) {
      items.push(baseItemsConflicts.noIssues)
    } else if (items.length === 0) {
      items.push(baseItemsConflicts.loading)
      items.push(baseItemsConflicts.loading)
    } else if (this.isAnalyzeConflictsPending) {
      items.push(baseItemsConflicts.loading)
    }
    return items
  }
  get itemsStructure (): Array<NameCheckItemIF> {
    let items = []
    if (this.hasErrorsdesignations) {
      items.push(baseItemsStructure.errorDesignation)
    }
    if (this.hasErrorsConflictsRestricted) {
      items.push(baseItemsStructure.errorRestricted)
    }
    if (this.hasErrorsStructure) {
      items.push(baseItemsStructure.errorStructure)
    }
    if (this.hasConflictsRestricted) {
      let newItem = baseItemsStructure.restricted
      newItem.words = this.conflictsRestricted
      items.push(newItem)
    }
    if (this.hasSpecialCharacters) {
      let newItem = baseItemsStructure.specialCharacters
      newItem.words = this.specialCharacters
      items.push(newItem)
    }
    if (this.hasDesignationsCheckUse) {
      let newItem = baseItemsStructure.designationsCheckUse
      const propEntities = [
        EntityTypes.DBA,
        EntityTypes.FR,
        EntityTypes.GP,
        EntityTypes.LL,
        EntityTypes.LP,
        EntityTypes.XLL,
        EntityTypes.XLP
      ]
      if (propEntities.includes(this.getEntityTypeCd)) {
        newItem = baseItemsStructure.designationsCheckUseProp
      } else if ([EntityTypes.CP, EntityTypes.XCP].includes(this.getEntityTypeCd)) {
        newItem = baseItemsStructure.designationsCheckUseCP
      } else if (this.getEntityTypeCd === EntityTypes.CC) {
        newItem = baseItemsStructure.designationsCheckUseCCC
      }
      newItem.words = this.designationsCheckUse
      items.push(newItem)
    }
    if (this.hasDesignationsMismatched) {
      let newItem = baseItemsStructure.designationsMismatched
      newItem.words = this.designationsMismatched
      items.push(newItem)
    }
    if (this.hasDesignationsMisplaced) {
      let newItem = baseItemsStructure.designationsMisplaced
      newItem.words = this.designationsMisplaced
      items.push(newItem)
    }
    if (this.hasNumbersCheckUse) {
      let newItem = baseItemsStructure.numbersCheckUse
      newItem.words = this.getNumbersCheckUse
      items.push(newItem)
    }
    if (this.isMissingDesignation) {
      let newItem = baseItemsStructure.designationsMissing
      if ([EntityTypes.CP, EntityTypes.XCP].includes(this.getEntityTypeCd)) {
        newItem = baseItemsStructure.designationsMissingCP
      } else if (this.getEntityTypeCd === EntityTypes.CC) {
        newItem = baseItemsStructure.designationsMissingCCC
      }
      items.push(newItem)
    }
    if (this.hasConflictsConditional) {
      let newItem = baseItemsStructure.conflictsConditional
      newItem.words = this.conflictsConditional
      // add condition text
      let instructions = ''
      const info = this.conflictsConditionalInstructions
      for (let i in info) {
        // add newlines
        if (instructions) instructions = instructions + '<br><br>'
        instructions = instructions + `<b>${info[i].word}:</b> ${info[i].instructions}`
      }
      newItem.expandedInfo2 = instructions
      items.push(newItem)
    }
    if (this.isMissingDescriptive) {
      items.push(baseItemsStructure.descriptiveMissing)
    }
    if (this.isMissingDistinctive) {
      let newItem = baseItemsStructure.distinctiveMissing
      items.push(newItem)
    }
    if (items.length === 0 && !this.loadingStructureCheck) {
      items.push(baseItemsStructure.noIssues)
    } else if (items.length === 0) {
      items.push(baseItemsStructure.loading)
      items.push(baseItemsStructure.loading)
    } else if (this.loadingStructureCheck) {
      items.push(baseItemsStructure.loading)
    }
    return items
  }
  get location (): string {
    return this.getLocationText
  }
  get nameInputHint (): string {
    if (this.isXproFlow) {
      return 'Your name in your home jurisdiction cannot be edited'
    }
    return 'You can edit your name here and check it again'
  }
  get showDesignationSelect (): boolean {
    return (Designations[this.getEntityTypeCd]?.end || false) && !this.isXproFlow
  }
  get specialCharacters (): Array<string> {
    return this.getSpecialCharacters
  }
  get subTitleConflict (): string {
    if (!this.hasIssuesConflictAlert && !this.hasIssuesConflictCaution) return 'OK'
    let message = ''
    if (this.conflictsExactNum > 0) message += `<b>${this.conflictsExactNum}</b> exact matches`
    else if (this.hasIssuesConflictAlert) return 'Possible issues found'
    if (this.hasIssuesConflictCaution && message) message += `, <b>${this.conflictsSimilarNum}</b> similar names`
    else if (this.hasIssuesConflictCaution) message += `<b>${this.conflictsSimilarNum}</b> similar names`
    // 0 conflicts
    return `${message} found`
  }
  get subTitleStructure (): string {
    const issues = [
      this.hasConflictsConditional,
      this.hasConflictsRestricted,
      this.hasDesignationsCheckUse,
      this.hasDesignationsMismatched,
      this.hasDesignationsMisplaced,
      this.hasSpecialCharacters,
      this.isMissingDescriptive,
      this.isMissingDesignation,
      this.isMissingDistinctive,
      this.hasErrorsdesignations,
      this.hasErrorsConflictsRestricted,
      this.hasErrorsStructure
    ].filter(function (issue) { return issue })
    if (issues.length > 0) {
      return `<b>${issues.length}</b> possible issues found`
    }
    return 'OK'
  }
  get tabIconConflict (): { color: string, icon: string } {
    if (this.hasIssuesConflictAlert) return { color: null, icon: 'mdi-alert-octagon' }
    else if (this.hasIssuesConflictCaution) return { color: null, icon: 'mdi-alert' }
    return { color: null, icon: 'mdi-check' }
  }
  get tabIconStructure (): { color: string, icon: string } {
    if (this.hasIssuesStructureAlert) {
      return { color: null, icon: 'mdi-alert-octagon' }
    }
    if (this.hasIssuesStructureCaution) {
      return { color: null, icon: 'mdi-alert' }
    }
    return { color: null, icon: 'mdi-check' }
  }
  get tabIconVerdict (): { color: string, icon: string } {
    if (this.hasIssuesStructureAlert || this.hasIssuesConflictAlert) {
      return { color: 'red darken-2', icon: 'mdi-alert-octagon' }
    }
    if (this.hasIssuesConflictCaution || this.hasIssuesStructureCaution) {
      return { color: 'caution', icon: 'mdi-alert' }
    }
    return { color: 'green darken-2', icon: 'mdi-check-circle' }
  }
  back () {
    this.setActiveComponent('Tabs')
  }
  checkAgain () {
    this.startAnalyzeName(null)
  }
  clearError (errorType: NameCheckErrorType) {
    this.nameCheckClearError(errorType)
  }
  dialogCheck () {
    const hasMajorIssues = this.hasIssuesConflictAlert || this.hasIssuesStructureAlert
    // only show dialog for non xpro
    if (hasMajorIssues && !this.isXproFlow) {
      this.dialogOptions.icon = this.tabIconVerdict.icon
      this.dialogOptions.iconColor = this.tabIconVerdict.color
      this.showNameCheckIssuesDialog = true
      return
    }
    this.submit()
  }
  dialogSubmit (proceed: boolean) {
    this.showNameCheckIssuesDialog = false
    if (proceed) this.submit()
  }
  retry (errorType: NameCheckErrorType) {
    if ([NameCheckErrorType.ERROR_DESIGNATION, NameCheckErrorType.ERROR_STRUCTURE].includes(errorType)) {
      this.clearError(errorType)
      this.getNameAnalysis({ xpro: false, designationOnly: errorType === NameCheckErrorType.ERROR_DESIGNATION })
    } else {
      const checks = {
        exact: errorType === NameCheckErrorType.ERROR_EXACT,
        restricted: errorType === NameCheckErrorType.ERROR_RESTRICTED,
        similar: errorType === NameCheckErrorType.ERROR_SIMILAR
      }
      this.clearError(errorType)
      this.startQuickSearch(checks)
    }
  }
  submit () {
    this.setActiveComponent('NamesCapture')
  }

  @Watch('isAnalyzeConflictsPending')
  private closeHelpText (val: boolean) {
    // if new similar name search starts => close
    if (val) {
      this.expandHelpTxt = false
    }
  }
  @Watch('isAnalyzeStructurePending')
  private setDefaultTab (val: boolean) {
    // if new structure analysis starts => go to structure tab
    if (val) {
      this.checks = 'structure-check'
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';
#box-shadow-filler-tab-item {
  box-shadow: 0px 3px 6px 2px rgb(172, 171, 171);
  margin-left: 4px;
  margin-right: 4px;
}
#box-shadow-filler-unactive-tab {
  box-shadow: 0 10px 30px 5px $gray9;
  margin-left: 5px;
  margin-right: 5px;
}
#conflicts-tab {
  background-color: $app-blue;
  width: 10rem;
  margin: 13px 15px 0 5px;
}
#name-check-header {
  font-size: $px-16;
  color: $gray9;
  text-align: center;
}
#name-check-lower-container {
  background-color: $gray1;
  max-width: none;
}
#name-check-main-container {
  max-width: none;
}
#name-check-name-input {
  padding: 2rem !important;
}
#name-check-start-over-btn {
  background-color: $gray1 !important;

  @media only screen and (max-width: 600px) {
    width: 100%;
  }
}
#name-check-submit-btn {
  font-size: $px-14 !important;
  font-weight: bold;

  @media only screen and (max-width: 600px) {
    margin-top: 10px !important;
    width: 100%;
  }}
#name-check-tabs {
  background-color: $gray1 !important;
}
#name-check-tabs-container {
  background-color: $gray1;
  max-width: none;
  padding-right: 38px;
  padding-left: 38px;

  @media only screen and (max-width: 600px) {
    padding-left: 0;
    padding-right: 0;
  }
}
#name-check-title {
  font-size: $px-24;
  color: $gray9;
  text-align: center;
  padding-top: 0.3125rem;
}
#name-check-verdict {
  border-radius: 10rem;
  margin-left: auto;
  margin-right: auto;
  text-align: center;
  width: 14rem;
}
#search-name-btn {
  font-size: $px-14 !important;
}
#structure-tab {
  background-color: $app-blue;
  width: 10rem;
  margin: 13px 5px 0 15px;
}
.active-tab {
  margin: 5px 5px 0 !important;
  border-top: 8px solid $app-blue;
  box-shadow: 0px 2px 5px 1px rgb(172, 171, 171);
}
.active-tab.no-border-top {
  border-top: none;
}
.mobile-wide-btn {
  width: 260px;
}
.name-check-info-text {
  color: $gray7;
  font-size: $px-14;
  line-height: 1.375rem;
}
.name-check-info-text-no-border {
  color: $gray7;
  font-size:$px-14;
  line-height: 1.375rem;
  padding-left: 118px;
  padding-right: 130px;

  @media only screen and (max-width: 600px) {
    padding-left: 10px;
    padding-right: 10px;
  }
}
.rounded-top-left {
  border-top-left-radius: 4px;
}
.rounded-top-right {
  border-top-right-radius: 4px;
}
.tab-items {
  box-shadow: 0px 7px 5px 1px rgb(172, 171, 171);
  margin: 0 5px 5px;
}
.txt-link {
  color: $app-blue;
  text-decoration: underline;
}
.upper-border {
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
  margin: 0 2.5px;
}
::v-deep .v-tab:before {
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}
::v-deep .theme--light.v-tabs > .v-tabs-bar {
  background-color: transparent !important;
  transition: none !important;
}

/* override the grayed out text to make it accessible */
::v-deep .theme--light.v-input--is-disabled input, .theme--light.v-input--is-disabled textarea {
  background-color: white;
  color: $gray9;
}

::v-deep .theme--light.v-tabs > .v-tabs-bar .v-tab:not(.v-tab--active) > .v-icon {
  color: white;
  transition: none !important;
}
</style>
