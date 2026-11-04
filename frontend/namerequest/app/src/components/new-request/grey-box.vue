<template>
  <v-container
    :key="option.type + '-' + i + '-container-'"
    class="no-gutters"
    :class="optionClasses"
  >
    <v-row
      no-gutters
      class="ma-0 pa-0"
    >
      <v-col cols="12">
        <span
          v-if="issue.setup.length > 1"
          class="title-bold-14"
        >Option {{ i + 1 }}:</span>
        <span class="ml-1 title-bold-16">{{ option.header }}</span>
      </v-col>
      <template v-if="issueType === 'user_cancelled'">
        <v-col
          class="copy-small colour-p-blue-text"
          cols="12"
        >
          <p
            v-if="option.line1"
            v-html="option.line1"
          />
          <p
            v-if="option.line2"
            v-html="option.line2"
          />
        </v-col>
        <v-col
          v-if="option.type === 'cancel_to_examiner'"
          cols="12"
          class="text-center"
        >
          <ReserveSubmit
            setup="examine"
            class="reserve-submit-btn"
            style="display: inline"
          />
        </v-col>
        <v-col
          v-else
          cols="12"
          class="text-center"
        >
          <v-btn @click="cancelAnalyzeName('Tabs')">
            Start Over
          </v-btn>
        </v-col>
      </template>
      <template v-else>
        <transition
          :name="i === 0 ? 'fade' : '' "
          mode="out-in"
        >
          <v-row
            :key="`${changesInBaseName}-${designationIsFixed}-key-${i}`"
            align-content="start"
            class="copy-small colour-p-blue-text"
          >
            <!-- Header, Line 1 and Line 2-->
            <v-col
              v-if="changesInBaseName && isDesignationIssueType && i === 0"
              class="copy-small colour-p-blue-text"
              cols="12"
            >
              You have altered the base text of your name.  You must
              either change it back or click the magnifying glass to run a new search for your edited name.
            </v-col>
            <v-col
              v-else-if="!isDesignationIssueType || !designationIsFixed"
              class="copy-small colour-p-blue-text"
              cols="12"
            >
              <p
                v-if="option.line1"
                class="ma-0 pa-0"
                v-html="option.line1"
              />
              <p
                v-if="option.line2"
                class="ma-0 pa-0 pt-2 mb-n1"
                v-html="option.line2"
              />
            </v-col>

            <!-- NAME/DESIGNATION-MANIPULATING OPTION BOXES -->
            <template v-if="isDesignationIssueType">
              <transition
                name="fade"
                mode="out-in"
              >
                <v-col
                  v-if="designationIsFixed && !changesInBaseName && !isLastIndex"
                  key="designation-error-col"
                  class="text-center designation-error-col"
                >
                  This issue has been resolved.  You are ready to review the next issue.
                </v-col>
                <v-col
                  v-if="!designationIsFixed && !changesInBaseName && i === 0"
                  key="designation-error-col"
                  class="text-center designation-error-col"
                >
                  <template v-if="Array.isArray(designations) && designations.length > 0">
                    <div class="pa-0">
                      <button
                        v-for="(des, d) in designations"
                        :id="'designation-btn-'+d"
                        :key="'designation-'+d"
                        class="link-sm ma-0 pa-0"
                        tag="div"
                        @click.once.prevent="changeDesignation(des)"
                      >
                        <span :class="d > 0 ? 'ml-1' : '' ">
                          {{ des }}{{ (d !== issue.designations.length - 1) ? ',' : '' }}
                        </span>
                      </button>
                    </div>
                  </template>
                  <template v-if="option.type === 'change designation at the end'">
                    <v-btn
                      id="move-designation-btn"
                      @click="moveDesignation"
                    >
                      Move Designation
                    </v-btn>
                  </template>
                </v-col>
                <v-col
                  v-if="designationIsFixed && i === 0 && issueIndex + 1 === issueLength"
                  key="designation-fixed-col"
                  class="text-center"
                >
                  <ReserveSubmit
                    class="reserve-submit-btn"
                    style="display: inline"
                    :setup="reserveSubmitConfig"
                  />
                </v-col>
              </transition>
            </template>

            <!-- CHANGE_ENTITY_TYPE OPTION BOX -->
            <template v-if="option.type === 'change_entity_type'">
              <v-col class="text-center">
                <v-btn @click="cancelAnalyzeName('Tabs')">
                  Start Search Over
                </v-btn>
              </v-col>
            </template>
            <!-- ASSUMED NAME OPTION BOX -->
            <template v-else-if="option.type === 'assumed_name'">
              <v-col
                v-if="isAssumedNameEntityType"
                :id="option.type + '-button-checkbox-col'"
                class="grey-box-checkbox-button text-center"
              >
                <transition
                  name="fade"
                  mode="out-in"
                >
                  <v-checkbox
                    v-if="showCheckBoxOrButton === 'checkbox'"
                    id="assume-name-checkbox"
                    :key="option.type+'-checkbox'"
                    v-model="boxIsChecked"
                    :error="showError"
                    :label="checkBoxLabel"
                    :ripple="false"
                    :hide-details="true"
                    class="py-0 my-0"
                  />
                  <ReserveSubmit
                    v-if="isLastIndex && showCheckBoxOrButton === 'button'"
                    id="reserve-submit-comp"
                    :key="option.type+'-reserve-submit'"
                    setup="assumed"
                  />
                </transition>
              </v-col>
            </template>
            <!-- ALL OTHER TYPES OF OPTION BOXES -->
            <template v-else>
              <v-col
                v-if="i !== 0 || isSendForReview(option.header)"
                :id="option.type + '-button-checkbox-col'"
                class="grey-box-checkbox-button mt-2 pa-0 text-center"
              >
                <transition
                  name="fade"
                  mode="out-in"
                >
                  <v-checkbox
                    v-if="showCheckBoxOrButton === 'checkbox'"
                    id="provide-consent-checkbox"
                    :key="option.type+'-checkbox'"
                    v-model="boxIsChecked"
                    :error="showError"
                    :label="checkBoxLabel"
                    :ripple="false"
                    :hide-details="true"
                    class="py-0 my-0"
                  />
                  <ReserveSubmit
                    v-if="showCheckBoxOrButton === 'button'"
                    :key="option.type+'-reserve-submit'"
                    :setup="reserveSubmitConfig"
                  />
                </transition>
              </v-col>
            </template>
          </v-row>
        </transition>
      </template>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import ReserveSubmit from '@/components/new-request/submit-request/reserve-submit.vue'
import { AnalysisJSONI, OptionI } from '@/interfaces'
import { replaceWord } from '@/plugins'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { EntityTypes } from '@/enums'
import { AllDesignationsList, Designations } from '@/list-data'

@Component({
  components: { ReserveSubmit }
})
export default class GreyBox extends Vue {
  @Prop(Boolean)
  readonly changesInBaseName: boolean

  @Prop(Boolean)
  readonly designationIsFixed: boolean

  @Prop(String)
  readonly finalName: string

  @Prop(Number)
  readonly i: number

  @Prop(Number)
  readonly issueIndex: number

  @Prop(Object)
  readonly option: OptionI

  @Prop(String)
  readonly originalName: string

  @Getter(useStore) getAnalysisJSON!: AnalysisJSONI
  @Getter(useStore) getDesignationIssueTypes!: string[]
  @Getter(useStore) getEntityTypeCd!: EntityTypes
  @Getter(useStore) getName!: string
  @Getter(useStore) getRequestExaminationOrProvideConsent!: boolean

  @Action(useStore) cancelAnalyzeName!: ActionBindingIF
  @Action(useStore) setName!: ActionBindingIF
  @Action(useStore) setRequestExaminationOrProvideConsent!: ActionBindingIF
  @Action(useStore) setShowActualInput!: ActionBindingIF

  clickedDesignation = ''
  originalNameBase = ''
  showError = false
  showLastStepButtons = {
    assumed_name: false,
    conflict_self_consent: false,
    obtain_consent: false,
    send_to_examiner: false
  }
  types = ['send_to_examiner', 'obtain_consent', 'conflict_self_consent', 'assumed_name']

  mounted () {
    this.$root.$on('start-search-again', () => {
      Object.keys(this.showLastStepButtons).forEach(key => {
        this.showLastStepButtons[key] = false
      })
    })
    let { originalName } = this
    if (this.issueType === 'designation_mismatch' || this.issueType === 'designation_misplaced') {
      this.originalNameBase = this.removeMismatchedDesignations(originalName)
      return
    }
    if (this.issueType === 'end_designation_more_than_once') {
      for (let word of this.nameActionWords) {
        originalName = replaceWord(originalName, word)
      }
      this.originalNameBase = originalName
      return
    }
    for (let word of AllDesignationsList) {
      originalName = replaceWord(originalName, word)
    }
    this.originalNameBase = originalName
  }

  get isAssumedNameEntityType () {
    return (
      this.getEntityTypeCd !== EntityTypes.XLP &&
      this.getEntityTypeCd !== EntityTypes.XLL &&
      this.getEntityTypeCd !== EntityTypes.XCP &&
      this.getEntityTypeCd !== EntityTypes.XSO
    )
  }

  get allDesignationsStripped () {
    return this.stripAllDesignations(this.originalName)
  }

  get boxIsChecked () {
    let { type } = this.option
    return this.requestExaminationOrProvideConsent[this.issueIndex][type]
  }

  set boxIsChecked (value) {
    for (let type of this.types) {
      this.setRequestExaminationOrProvideConsent({
        value: false,
        type,
        index: this.issueIndex
      })
    }
    if (this.issueIndex === this.issueLength - 1) {
      for (let type of this.types) {
        this.showLastStepButtons[type] = false
      }
      this.showLastStepButtons[this.option.type] = true
    }
    this.setRequestExaminationOrProvideConsent({
      value,
      type: this.option.type,
      index: this.issueIndex
    })
  }

  get checkBoxLabel () {
    switch (this.option.type) {
      case 'send_to_examiner':
        return 'I want to send my name for review'
      case 'obtain_consent':
      case 'conflict_self_consent':
        return 'I will submit written consent to the BC Business Registry'
      case 'assumed_name':
        return 'I want to assume a name in BC'
      default:
        return ''
    }
  }

  get designations () {
    if (this.issue && this.issue.designations) {
      return this.issue.designations
    }
    return null
  }

  get isDesignationIssueType () {
    if (this.getDesignationIssueTypes.includes(this.issueType)) {
      return true
    }
    return false
  }

  get isLastIndex () {
    return (this.issueIndex === this.lastIndex)
  }

  get issue (): any {
    return this.getAnalysisJSON.issues[this.issueIndex]
  }

  get issueLength () {
    if (Array.isArray(this.getAnalysisJSON.issues)) {
      return this.getAnalysisJSON.issues.length
    }
    return 1
  }

  get issueType () {
    if (this.issue && this.issue.issue_type) {
      return this.issue.issue_type
    }
    return ''
  }

  isSendForReview (header: string): boolean {
    return (header === 'Send for Review')
  }

  get lastIndex () {
    return this.issueLength - 1
  }

  get multipleMismatchedDesignations () {
    if (this.issueType === 'designation_mismatch') {
      if (Array.isArray(this.nameActions) && this.nameActions.length > 1) {
        return this.nameActions.map(action => (
          { word: action.word.toUpperCase(), index: action.index }
        ))
      }
    }
    return false
  }

  get name () {
    return this.getName
  }

  set name (name) {
    this.setName(name)
    this.$root.$emit('updatecontents', name)
  }

  get nameActions (): any {
    if (this.issue && Array.isArray(this.issue.name_actions)) {
      return this.issue.name_actions
    }
    return []
  }

  get nameActionWords () {
    if (Array.isArray(this.nameActions) && this.nameActions.length > 0) {
      return this.nameActions.map(action => action.word.toUpperCase())
    }
    return []
  }

  get optionClasses () {
    let { i } = this
    if (this.issue && Array.isArray(this.issue.setup)) {
      switch (this.issue.setup.length) {
        case 1:
          return 'square-card-x1'
        case 2:
          if (i === 1) {
            return 'square-card-x2 ml-3'
          }
          return 'square-card-x2'
        case 3:
          if (i === 1) {
            return 'square-card-x3 mx-3'
          }
          return 'square-card-x3'
        default:
          return ''
      }
    }
    return ''
  }

  get requestExaminationOrProvideConsent () {
    return this.getRequestExaminationOrProvideConsent
  }

  get reserveSubmitConfig () {
    if (this.issueLength === 1) {
      if (this.option.type === 'send_to_examiner') {
        return 'examine'
      }
      if (['obtain_consent', 'conflict_self_consent'].includes(this.option.type)) {
        return 'consent'
      }
      return ''
    }
    if (this.isLastIndex) {
      let priorIndexes = () => {
        let output = []
        let i = this.issueIndex
        while (i > 0) {
          i--
          output.push(i)
        }
        return output
      }

      if (priorIndexes().some(index => this.requestExaminationOrProvideConsent[index].send_to_examiner)) {
        return 'examine'
      }
      if (this.option.type === 'send_to_examiner') {
        return 'examine'
      }
      if (priorIndexes().some(index => this.requestExaminationOrProvideConsent[index].obtain_consent ||
      this.requestExaminationOrProvideConsent[index].conflict_self_consent)) {
        return 'consent'
      }
      if (['conflict_self_consent', 'obtain_consent'].includes(this.option.type)) {
        return 'consent'
      }
    }
    return ''
  }

  get showCheckBoxOrButton (): string {
    let { type } = this.option
    if (['obtain_consent', 'conflict_self_consent'].includes(type)) {
      if (this.requestExaminationOrProvideConsent[this.issueIndex].send_to_examiner) {
        return 'checkbox'
      }
    }
    if (type === 'send_to_examiner') {
      if (['obtain_consent', 'conflict_self_consent'].some(
        issue => this.requestExaminationOrProvideConsent[this.issueIndex][issue]
      )) {
        return 'checkbox'
      }
    }
    if (this.issueIndex + 1 === this.issueLength) {
      switch (type) {
        case 'cancel_to_examiner':
        case 'cancel_to_start':
          return 'button'
        case 'send_to_examiner':
          if (this.boxIsChecked) {
            return 'button'
          }
          return 'checkbox'
        case 'obtain_consent':
          if (this.boxIsChecked) {
            return 'button'
          }
          return 'checkbox'
        case 'conflict_self_consent':
          if (this.boxIsChecked) {
            return 'button'
          }
          return 'checkbox'
        case 'assumed_name':
          if (this.boxIsChecked) {
            return 'button'
          }
          return 'checkbox'
        default:
          return 'checkbox'
      }
    }
    return 'checkbox'
  }

  get word () {
    if (this.issue && Array.isArray(this.issue.name_actions)) {
      if (this.issue.name_actions[0] && this.issue.name_actions[0].word) {
        return this.issue.name_actions[0].word.toUpperCase()
      }
    }
    if (this.clickedDesignation) {
      return this.clickedDesignation
    }
    return ''
  }

  changeDesignation (designation) {
    this.setShowActualInput(true)
    designation = designation.toUpperCase()
    this.clickedDesignation = designation
    if (this.issueType === 'designation_mismatch') {
      let { allDesignationsStripped } = this
      if (this.nameActionWords.length > 0) {
        for (let word of this.nameActionWords) {
          allDesignationsStripped = replaceWord(allDesignationsStripped, word)
        }
      }
      this.name = allDesignationsStripped + ' ' + designation
      return
    }
    if (this.issueType === 'end_designation_more_than_once') {
      this.name = this.originalNameBase + ' ' + designation
      return
    }
    if (this.issueType === 'designation_non_existent') {
      this.name = this.originalName + ' ' + designation
      return
    }
    if (this.multipleMismatchedDesignations) {
      this.name = this.removeMismatchedDesignations(this.originalName) + ' ' + designation
    }
  }

  extractInnerDesignation (name, designation = null) {
    let { words } = Designations[this.getEntityTypeCd]
    if (!designation) {
      for (let word of words) {
        name = replaceWord(name, word)
      }
    } else if (designation) {
      name = replaceWord(name, designation)
    }
    return name
  }

  moveDesignation () {
    this.setShowActualInput(true)
    let baseName: string
    if (this.originalNameBase) {
      baseName = this.originalNameBase
    } else {
      baseName = this.extractInnerDesignation(this.originalName, this.word)
    }
    this.name = baseName + ' ' + this.word
  }

  removeMismatchedDesignations (name, designation = null) {
    if (designation) {
      return replaceWord(name, designation)
    }
    if (this.nameActionWords.length > 0) {
      for (let word of this.nameActionWords) {
        name = replaceWord(name, word)
      }
      return name
    }
    if (Array.isArray(this.designations)) {
      let index = this.designations.findIndex(des => name.endsWith(' ' + des))
      if (index >= 0) {
        let designation = this.designations[index]
        name = replaceWord(name, designation)
      }
    }
    return name
  }

  stripAllDesignations (name) {
    for (let word of AllDesignationsList) {
      name = replaceWord(name, word)
    }
    return name
  }
}
</script>
