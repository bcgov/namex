<template>
  <v-form
    id="send-to-examination-form"
    @keydown="validate"
  >
    <v-container
      id="send-to-examination-container"
      fluid
      class="pa-0"
    >
      <NameRequestDetails v-if="getEditMode" />

      <v-row
        v-if="getEditMode || isAssumedName"
        class="pt-8 my-0"
      >
        <v-col
          v-if="getEditMode"
          cols="auto"
          class="font-weight-bold h4 py-0"
        >
          Name Choices
        </v-col>
        <v-col
          v-else-if="isAssumedName"
          cols="auto"
          class="text-body-3 py-0"
        >
          Name in Home Jurisdiction: {{ getName }}
        </v-col>
      </v-row>

      <v-row class="pt-8 my-0">
        <v-col
          key="static-1"
          cols="12"
          md="2"
          lg="2"
          class="label-style align-self-start pt-0"
        >
          {{ choicesLabelsAndHints[0].label }}
        </v-col>
        <transition
          name="fade"
          mode="out-in"
        >
          <v-col
            :key="transitionKey(1)"
            class="ma-0 pa-0"
            :cols="isMobile ? 12 : 10"
          >
            <v-row
              v-if="getLocation === Location.BC"
              class="ma-0 pa-0"
            >
              <v-col
                :cols="(designationAtEnd && !isMobile) ? 8 : 12"
                :class="{ 'py-0' : !isMobile }"
              >
                <v-text-field
                  id="choice-1-text-field"
                  :error-messages="messages.name1"
                  :hide-details="hideDetails"
                  :value="nameChoices.name1"
                  filled
                  :label="choicesLabelsAndHints[0].hint"
                  :name="Math.random()"
                  @blur="handleBlur()"
                  @input="editChoices('name1', $event, true)"
                />
              </v-col>
              <v-col
                v-if="designationAtEnd"
                cols="12"
                md="4"
                lg="4"
                :class="{ 'py-0' : !isMobile }"
              >
                <v-tooltip
                  top
                  transition="fade-transition"
                  content-class="top-tooltip"
                  :disabled="isMobile"
                >
                  <template #activator="{ on }">
                    <div v-on="on">
                      <v-select
                        id="designation-1-select"
                        :error-messages="des1Message"
                        :hide-details="hideDetails"
                        :items="items"
                        :menu-props="menuProps"
                        :value="nameChoices.designation1"
                        filled
                        label="Designation"
                        @blur="handleBlur(); showDesignationErrors.des1 = true"
                        @input="editChoices('designation1', $event, true)"
                      />
                    </div>
                  </template>
                  <span>Your company name must include a designation.
                    There are no legal differences between these designations.
                    You can choose whichever you prefer.</span>
                </v-tooltip>
              </v-col>
            </v-row>
            <v-row
              v-else
              class="ma-0 pa-0"
            >
              <v-col
                :cols="isAssumedName ? 8 : 12"
                class="py-0"
              >
                <v-text-field
                  id="choice-1-text-field"
                  :error-messages="messages.name1"
                  :hide-details="hideDetails"
                  :value="xproNameWithoutConflict"
                  :filled="isAssumedName"
                  :class="{ 'read-only-mode': !isAssumedName }"
                  :label="choicesLabelsAndHints[0].hint"
                  :disabled="!isAssumedName"
                  :name="Math.random()"
                  @blur="handleBlur()"
                  @input="editChoices('name1', $event, true)"
                />
              </v-col>
              <v-col
                v-if="isAssumedName"
                cols="4"
                class="py-0"
              >
                <v-tooltip
                  top
                  transition="fade-transition"
                  content-class="top-tooltip"
                  :disabled="isMobile"
                >
                  <template #activator="{ on }">
                    <div v-on="on">
                      <v-select
                        id="designation-1-select"
                        :error-messages="des1Message"
                        :hide-details="hideDetails"
                        :items="items"
                        :menu-props="menuProps"
                        :value="nameChoices.designation1"
                        filled
                        label="Designation"
                        @blur="handleBlur(); showDesignationErrors.des1 = true"
                        @input="editChoices('designation1', $event, true)"
                      />
                    </div>
                  </template>
                  <span>Your company name must include a designation.
                    There are no legal differences between these designations.
                    You can choose whichever you prefer.</span>
                </v-tooltip>
              </v-col>
            </v-row>
          </v-col>
        </transition>
      </v-row>

      <v-row
        v-if="!getEditMode"
        class="pt-6 my-0 colour-text"
      >
        <v-col
          :cols="isMobile ? 0 : 2"
          class="py-0"
        />
        <v-col
          :cols="isMobile ? 12 : 10"
          class="py-0 text-body-3"
        >
          <span v-if="getLocation !== Location.BC">
            <span v-if="isAssumedName">
              You may provide up to two additional assumed names which will be considered at no further
              cost, in the order provided, if your first choice cannot be approved. Be sure to follow all
              <a
                :href="buildNameURL"
                target="_blank"
              >
                guidelines for how to build a name.
                <v-icon class="launch-icon">mdi-launch</v-icon>
              </a>
            </span>
            <span v-else-if="!showSecondAndThirdNameChoices">
              <div class="mt-1">
                The name of your business must be the same in BC and in your home jurisdiction.
              </div>
              <div class="mt-5">
                If, after review, your current name is not approved for use in BC you will need to change
                your business name in your home jurisdiction, and request your new name in BC as well.
              </div>
            </span>
            <span v-else>
              You may provide up to two additional assumed names which will be considered at no further cost, in
              the order provided, if the name in the home jurisdiction cannot be approved. Be sure to follow all
              <a
                :href="buildNameURL"
                target="_blank"
              >
                guidelines for how to build a name.
                <v-icon class="launch-icon">mdi-launch</v-icon>
              </a>
            </span>
          </span>
          <span v-else>
            You may provide up to two additional names which will be considered at no further cost, in
            the order provided, only if your first choice cannot be approved. Be sure to follow all
            <a
              :href="buildNameURL"
              target="_blank"
            >
              guidelines for how to build a name.
              <v-icon class="launch-icon">mdi-launch</v-icon>
            </a>
          </span>
        </v-col>
      </v-row>

      <v-row
        v-if="showSecondAndThirdNameChoices"
        class="pt-8 my-0"
      >
        <v-col
          key="static-2"
          cols="12"
          md="2"
          lg="2"
          class="label-style align-self-start pt-0"
        >
          {{ choicesLabelsAndHints[1].label }}
        </v-col>
        <transition
          name="fade"
          mode="out-in"
        >
          <v-col
            :key="transitionKey(2)"
            class="ma-0 pa-0"
            :cols="isMobile ? 12 : 10"
          >
            <v-row class="ma-0 pa-0">
              <v-col
                :cols="(designationAtEnd && !isMobile) ? 8: 12"
                :class="{'py-0' : !isMobile }"
              >
                <v-text-field
                  id="choice-2-text-field"
                  :error-messages="messages.name2"
                  :hide-details="hideDetails"
                  :value="nameChoices.name2"
                  filled
                  :label="choicesLabelsAndHints[1].hint"
                  :name="Math.random()"
                  @blur="handleBlur()"
                  @input="editChoices('name2', $event, true)"
                />
              </v-col>
              <v-col
                v-if="designationAtEnd"
                cols="12"
                md="4"
                lg="4"
                :class="{'py-0' : !isMobile }"
              >
                <v-tooltip
                  top
                  transition="fade-transition"
                  content-class="top-tooltip"
                  :disabled="isMobile"
                >
                  <template #activator="{ on }">
                    <div v-on="on">
                      <v-select
                        id="designation-2-select"
                        :error-messages="des2Message"
                        :hide-details="hideDetails"
                        :items="items"
                        :menu-props="menuProps"
                        :value="nameChoices.designation2"
                        filled
                        label="Designation"
                        @blur="handleBlur(); showDesignationErrors.des2 = true"
                        @input="editChoices('designation2', $event, true)"
                      />
                    </div>
                  </template>
                  <span>Your company name must include a designation.
                    There are no legal differences between these designations.
                    You can choose whichever you prefer.</span>
                </v-tooltip>
              </v-col>
            </v-row>
          </v-col>
        </transition>
      </v-row>

      <v-row
        v-if="showSecondAndThirdNameChoices"
        key="static-3"
        class="pt-8 my-0"
      >
        <v-col
          cols="12"
          md="2"
          lg="2"
          class="label-style align-self-start pt-0"
        >
          {{ choicesLabelsAndHints[2].label }}
        </v-col>
        <transition
          name="fade"
          mode="out-in"
        >
          <v-col
            :key="transitionKey(3)"
            class="ma-0 pa-0"
            :cols="isMobile ? 12 : 10"
          >
            <v-row class="ma-0 pa-0">
              <v-col
                :cols="(designationAtEnd && !isMobile) ? 8: 12"
                :class="{'py-0' : !isMobile }"
              >
                <v-text-field
                  id="choice-3-text-field"
                  :error-messages="messages.name3"
                  :hide-details="hideDetails"
                  :value="nameChoices.name3"
                  filled
                  :label="choicesLabelsAndHints[2].hint"
                  :name="Math.random()"
                  @blur="handleBlur()"
                  @input="editChoices('name3', $event)"
                />
              </v-col>
              <v-col
                v-if="designationAtEnd"
                cols="12"
                md="4"
                lg="4"
                :class="{'py-0' : !isMobile }"
              >
                <v-tooltip
                  top
                  transition="fade-transition"
                  content-class="top-tooltip"
                  :disabled="isMobile"
                >
                  <template #activator="{ on }">
                    <div v-on="on">
                      <v-select
                        id="designation-3-select"
                        :error-messages="des3Message"
                        :hide-details="hideDetails"
                        :items="items"
                        :value="nameChoices.designation3"
                        filled
                        label="Designation"
                        @blur="handleBlur(); showDesignationErrors.des3 = true"
                        @input="editChoices('designation3', $event, true)"
                      />
                    </div>
                  </template>
                  <span>Your company name must include a designation.
                    There are no legal differences between these designations.
                    You can choose whichever you prefer.</span>
                </v-tooltip>
              </v-col>
            </v-row>
          </v-col>
        </transition>
      </v-row>

      <v-row class="pt-8 my-0">
        <v-col
          cols="7"
          class="py-0"
        />
        <ApplicantInfoNav @nextAction="validateButton()" />
      </v-row>
    </v-container>
  </v-form>
</template>

<script lang="ts">
import { Component, Mixins, Watch } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import ApplicantInfoNav from '@/components/common/applicant-info-nav.vue'
import NameRequestDetails from '@/components/existing-request/name-request-details.vue'
import { NameChoicesIF, NameRequestI } from '@/interfaces'
import { sanitizeName } from '@/plugins'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { EntityTypes, Location } from '@/enums'
import { CommonMixin } from '@/mixins'
import { Designations, checkInvalidDesignation } from '@/list-data'

/**
 * This is the component that displays the name choices.
 * It also shows the name request details here when editing a NR.
 */
@Component({
  components: {
    ApplicantInfoNav,
    NameRequestDetails
  }
})
export default class NamesCapture extends Mixins(CommonMixin) {
  // enum for template
  readonly Location = Location

  @Getter(useStore) getDisplayedComponent!: string
  @Getter(useStore) getDesignation!: string
  @Getter(useStore) getEditMode!: boolean
  @Getter(useStore) getEntityTypeCd!: EntityTypes
  @Getter(useStore) getLocation!: Location
  @Getter(useStore) getName!: string
  @Getter(useStore) getNameChoices!: NameChoicesIF
  @Getter(useStore) getNr!: Partial<NameRequestI>
  @Getter(useStore) getSubmissionTabNumber!: number
  @Getter(useStore) isAssumedName!: boolean
  @Getter(useStore) isMobile!: boolean

  @Action(useStore) setDisplayedComponent!: ActionBindingIF
  @Action(useStore) setNameChoices!: ActionBindingIF
  @Action(useStore) setNameChoicesToInitialState!: ActionBindingIF
  @Action(useStore) setRequestAction!: ActionBindingIF
  @Action(useStore) setSubmissionTabComponent!: ActionBindingIF
  @Action(useStore) setSubmissionType!: ActionBindingIF
  @Action(useStore) startEditName!: ActionBindingIF

  readonly buildNameURL = 'https://www2.gov.bc.ca/gov/content?id=4A6A55FAD204494D9AF0B53BDC13A24F'

  hideDetails: boolean | 'auto' = true
  messages = {
    des1: '',
    des2: '',
    des3: '',
    name1: '',
    name2: '',
    name3: ''
  }
  menuProps = {
    disableKeys: false
  }
  showDesignationErrors = {
    des1: false,
    des2: false,
    des3: false
  }

  async mounted (): Promise<void> {
    // add event listener when this component is mounted
    // eg, when user continues to send for review
    this.$el.addEventListener('keydown', this.handleKeydown)

    this.setNameChoicesToInitialState(null)
    if (this.isAssumedName && !this.getEditMode) {
      await this.$nextTick() // FUTURE: remove if not needed
      this.hideDetails = true
      return
    }

    await this.$nextTick() // FUTURE: remove if not needed
    if (this.getEditMode) {
      this.populateNames()
      return
    }

    // if we get here it's a new name
    this.setSubmissionType('examination')
    if (this.getDesignation) this.setNameChoices({ key: 'designation1', value: this.getDesignation })
    this.setNameChoices({ key: 'name1', value: this.getName })

    this.scrollTo('namerequest-sbc-header')
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
    const myTab = (this.getSubmissionTabNumber === 1)
    return (myComponent && myTab)
  }

  get showSecondAndThirdNameChoices () {
    if (this.getLocation !== Location.BC) {
      if (this.getEntityTypeCd === EntityTypes.XLP ||
        this.getEntityTypeCd === EntityTypes.XLL ||
        this.getEntityTypeCd === EntityTypes.XCP ||
        this.getEntityTypeCd === EntityTypes.XSO) {
        return false
      }
    }
    return true
  }

  get autofocusField () {
    if (this.isAssumedName) {
      return 'name1'
    }
    let output = 'name2'
    if (this.designationAtEnd) {
      if (!this.messages.name1 && !this.messages.des1) {
        return output
      }
      if (this.messages.des1) {
        output = 'des1'
      }
      if (this.messages.name1) {
        output = 'name1'
      }
      return output
    }
    if (this.messages.name1) {
      output = 'name1'
    }
    return output
  }

  get des1Message (): string {
    if (this.showDesignationErrors.des1) {
      return this.messages.des1
    }
    return ''
  }

  get des2Message (): string {
    if (this.showDesignationErrors.des2) {
      return this.messages.des2
    }
    return ''
  }

  get des3Message (): string {
    if (this.showDesignationErrors.des3) {
      return this.messages.des3
    }
    return ''
  }

  get designationAtEnd () {
    if (this.getEntityTypeCd && Designations[this.getEntityTypeCd]) {
      return Designations[this.getEntityTypeCd].end
    }
    return false
  }

  get choicesLabelsAndHints () {
    if (this.getLocation === Location.BC) {
      return [
        {
          label: 'First Choice',
          hint: 'First Name Choice'
        },
        {
          label: 'Second Choice',
          hint: 'Second Name Choice (Optional)'
        },
        {
          label: 'Third Choice',
          hint: 'Third Name Choice (Optional)'
        }
      ]
    } else if (this.isAssumedName) {
      return [
        {
          label: 'Assumed Name First Choice',
          hint: 'Enter your first choice for an assumed name'
        },
        {
          label: 'Assumed Name Second Choice',
          hint: 'Enter your second choice for an assumed name (Optional)'
        },
        {
          label: 'Assumed Name Third Choice',
          hint: 'Enter your third choice for an assumed name (Optional)'
        }
      ]
    } else {
      return [
        {
          label: 'Name in Home Jurisdiction',
          hint: ''
        },
        {
          label: 'Assumed Name First Choice',
          hint: 'Enter your first choice for an assumed name (Optional)'
        },
        {
          label: 'Assumed Name Second Choice',
          hint: 'Enter your second choice for an assumed name (Optional)'
        }
      ]
    }
  }

  get entityPhraseChoices () {
    if (!this.getEntityTypeCd || !Designations[this.getEntityTypeCd]) {
      return []
    }
    let basePhrases = Designations[this.getEntityTypeCd].words
    // these are the inner phrases for the CCC and CP types.  Filtering out CR designations from CPs has no effect
    // and CCC designations are a mix of CR-type ending designations and CCC specific inner phrases so filter out
    // the CR designations for the purposes of this getter
    return basePhrases.filter(phrase => !Designations['CR'].words.includes(phrase))
  }

  get entityPhraseRequired (): boolean {
    return this.getEntityTypeCd && this.entityTypeText.length > 0
  }

  get entityPhraseText (): string {
    return this.entityPhraseChoices.join(', ')
  }

  // define the text for the name designation error message for the entity types that require it
  get entityTypeText (): string {
    switch (this.getEntityTypeCd) {
      case EntityTypes.SO: return 'Society'
      case EntityTypes.CC: return 'Community Contribution Company'
      case EntityTypes.CP: return 'Cooperative'

      // for other no name designation required entity types, return an empty string
      default: return ''
    }
  }

  get isValid (): boolean {
    const { nameChoices, messages, designationAtEnd, validatePhrases } = this
    const location = this.getLocation

    if (this.isAssumedName && this.getEditMode) {
      if (!nameChoices['name1']) {
        messages['name1'] = 'Please enter at least one name'
        return false
      }
      messages['name1'] = ''
      return true
    }

    if (this.isAssumedName) {
      if (!nameChoices['name1']) {
        if (!nameChoices['name2'] && !nameChoices['name3']) {
          return false
        }
        if (nameChoices['name2'] || nameChoices['name3']) {
          messages['name1'] = 'Please enter a first choice before any subsequent choices'
          return false
        }
      }
      if (designationAtEnd && !nameChoices.designation1) {
        return false
      }
      let outcome = true
      for (let choice of [1, 2, 3]) {
        if (nameChoices[`name${choice}`] === this.getName) {
          messages[`name${choice}`] = 'This is identical to the name you originally entered. Please enter a new name.'
          this.hideDetails = 'auto'
          outcome = false
        }
      }
      return outcome
    }

    function name1 () {
      messages.name1 = ''
      messages.des1 = ''

      validatePhrases('name1')
      if (location === Location.BC) {
        if (designationAtEnd && !nameChoices.designation1) {
          messages.des1 = 'Please choose a designation'
        }
      }
      if (messages.name1 || messages.des1) {
        return false
      }
      return true
    }

    function name2 () {
      messages.name2 = ''
      messages.des2 = ''

      if (!nameChoices.name2) {
        return true
      }
      validatePhrases('name2')
      if (nameChoices.name2 === nameChoices.name1) {
        messages.name2 = 'This is identical to your first name choice. Please enter a unique name.'
      }
      if (designationAtEnd && !nameChoices.designation2) {
        messages.des2 = 'Please choose a designation'
      }
      if (messages.name2 || messages.des2) {
        return false
      }
      return true
    }

    function name3 () {
      messages.name3 = ''
      messages.des3 = ''
      if (!nameChoices.name3) {
        return true
      }
      validatePhrases('name3')
      if (nameChoices.name3 === nameChoices.name1) {
        messages.name3 = 'This is identical to your first name choice. Please enter a unique name.'
      }
      if (nameChoices.name3 === nameChoices.name2) {
        messages.name3 = 'This is identical to your second name choice. Please enter a unique name.'
      }
      if (designationAtEnd && !nameChoices.designation3) {
        messages.des3 = 'Please choose a designation'
      }
      if (messages.name3 || messages.des3) {
        return false
      }
      return true
    }

    function validateNamesInputOrder () {
      // clean up messages
      messages.name1 = ''
      messages.des1 = ''
      messages.name2 = ''
      messages.des2 = ''
      messages.name3 = ''
      messages.des3 = ''

      if (!nameChoices.name1) {
        if (nameChoices.name2 || nameChoices.name3) {
          messages.name1 = 'Please enter a first choice before any subsequent choices'
          return false
        } else {
          messages.name1 = 'Please enter at least one name'
          return false
        }
      }
      if (nameChoices.name3 && !nameChoices.name2) {
        messages.name3 = 'Please choose a second name before entering a third name'
        return false
      }
      return true
    }

    if (!validateNamesInputOrder()) {
      return false
    }

    let step1 = name1()
    let step2 = name2()
    let step3 = name3()

    // Validate designations for all name choices
    const validDesignation1 = this.validateDesignation('name1')
    const validDesignation2 = this.validateDesignation('name2')
    const validDesignation3 = this.validateDesignation('name3')

    if (this.getEditMode) {
      let outcome = true

      if (!name1() || !name2() || !name3() || !validDesignation1 || !validDesignation2 || !validDesignation3) {
        if (!validDesignation1) {
          messages.name1 = checkInvalidDesignation(this.getEntityTypeCd.toString(), this.nameChoices['name1'])
        }
        if (!validDesignation2) {
          messages.name2 = checkInvalidDesignation(this.getEntityTypeCd.toString(), this.nameChoices['name2'])
        }
        if (!validDesignation3) {
          messages.name3 = checkInvalidDesignation(this.getEntityTypeCd.toString(), this.nameChoices['name3'])
        }
        if (messages.name1 || messages.name2 || messages.name3) {
          outcome = false
        }
      } else {
        for (let choice of [1, 2, 3]) {
          if (nameChoices[`name${choice}`] && designationAtEnd) {
            if (!nameChoices[`designation${choice}`]) {
              if (location === Location.BC || this.isAssumedName) {
                messages[`des${choice}`] = 'Please choose a designation'
                this.showDesignationErrors[`des${choice}`] = true
                outcome = false
              }
            } else {
              this.messages[`des${choice}`] = ''
            }
          }
        }
      }
      if (!outcome) {
        this.hideDetails = 'auto'
      }
      return outcome
    }

    if (!validDesignation1 || !validDesignation2 || !validDesignation3) {
      return false
    }

    this.$nextTick(function () {
      if (!(step1 && step2 && step3)) {
        this.hideDetails = 'auto'
      }
    })
    return (step1 && step2 && step3)
  }

  get items (): string[] {
    let output: string[] = Designations[this.getEntityTypeCd].words
    if (this.getEntityTypeCd === EntityTypes.CC) {
      output = Designations['CR'].words
    }
    return output
  }

  get nameChoices (): NameChoicesIF {
    return this.getNameChoices
  }

  get xproNameWithoutConflict () {
    var name = this.nameChoices.name1
    if (!this.isAssumedName && this.nameChoices.designation1) {
      name = `${name} ${this.nameChoices.designation1}`
    }
    return name
  }

  editChoices (key, value, userInitiated = false) {
    if (userInitiated) {
      this.hideDetails = true
      for (let key in this.messages) {
        this.messages[key] = ''
      }
    }
    this.setNameChoices({ key, value })
  }

  handleBlur () {
    for (let key in this.nameChoices) {
      let value = this.nameChoices[key] ? sanitizeName(this.nameChoices[key]) : ''
      this.editChoices(key, value)
    }
    this.validate()
  }

  handleKeydown (event) {
    if (event.key === 'Enter') {
      this.menuProps.disableKeys = true
      this.validateButton()
    }
  }

  populateNames () {
    let nr = this.getNr
    for (let name of nr.names) {
      let { choice } = name
      if (name.designation) {
        this.setNameChoices({ key: `designation${choice}`, value: name.designation })
      } else {
        this.setNameChoices({ key: `designation${choice}`, value: '' })
      }
      this.setNameChoices({ key: `name${choice}`, value: name.name })
    }
    const { nameChoices } = this
    if (nr && nr.names && Array.isArray(nr.names)) {
      for (let choice of [1, 2, 3]) {
        if (nr.names.find(name => name.choice === choice)) {
          let { name } = nr.names.find(name => name.choice === choice)
          if (name.designation && name.name) {
            this.setNameChoices({ key: `name${choice}`, value: name.name })
            this.setNameChoices({ key: `designation${choice}`, value: name.designation })
            continue
          }
          if (this.designationAtEnd) {
            for (let item of this.items) {
              if ([' LTD', ' INC', ' CORP'].some(des => name.endsWith(des))) {
                name = name + '.'
              }
              if (item) {
                if (name.endsWith(item)) {
                  this.setNameChoices({ key: `designation${choice}`, value: item })
                  let value = name.replace(item, '').trim()
                  this.setNameChoices({ key: `name${choice}`, value })
                }
              }
            }
            if (!nameChoices[`name${choice}`]) {
              this.setNameChoices({ key: `name${choice}`, value: name })
            }
          } else {
            let value = nameChoices[`name${choice}`].replace(nameChoices[`designation${choice}`], '').trim()
            this.setNameChoices({ key: `name${choice}`, value: value })
          }
        }
        if (this.designationAtEnd) {
          if (nameChoices[`name${choice}`] && nameChoices[`designation${choice}`]) {
            if (nameChoices[`name${choice}`].endsWith(' ' + nameChoices[`designation${choice}`])) {
              let newName = nameChoices[`name${choice}`].replace(nameChoices[`designation${choice}`], '').trim()
              this.setNameChoices({ key: `name${choice}`, value: newName })
            }
          }
        }
      }
    }
  }

  showNextTab () {
    this.setSubmissionTabComponent('ApplicantInfo1')
  }

  transitionKey (i) {
    if (this.designationAtEnd) {
      return `transition-state-1-${i}`
    }
    return `transition-state-2-${i}`
  }

  validate (next = false) {
    if (!this.isValid) {
      this.hideDetails = 'auto'
      this.menuProps.disableKeys = false
      return
    }
    this.hideDetails = true
    if (next) {
      this.showNextTab()
    }
  }

  validateButton () {
    for (let key in this.showDesignationErrors) {
      this.showDesignationErrors[key] = true
    }
    this.startEditName(null)
    this.validate(true)
  }

  validatePhrases (choice: string) {
    if (this.entityPhraseRequired) {
      const name = this.nameChoices[choice].toUpperCase()
      if (this.entityPhraseChoices.every(phrase => {
        phrase = phrase.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&')
        return (name.search(new RegExp('(\\s)' + phrase + '(\\s|$)')) === -1)
      })) {
        this.messages[choice] = `A ${this.entityTypeText} name must include (but not start with)
          one of the following phrases: ${this.entityPhraseText}`
      }
      if (this.entityPhraseChoices.some(phrase => name.startsWith(phrase))) {
        this.messages[choice] = `A ${this.entityTypeText} name must not begin with one of the
          following phrases: ${this.entityPhraseText}`
      }
    }
  }

  validateDesignation (choice: string): boolean {
    const invalidDesignationMsg = checkInvalidDesignation(this.getEntityTypeCd.toString(), this.nameChoices[choice])
    if (invalidDesignationMsg) {
      this.messages[choice] = invalidDesignationMsg
      return false
    }
    return true
  }

  @Watch('isValid')
  onValidChanged (val: boolean) {
    if (val) {
      this.$nextTick(() => {
        if (this.$el?.querySelector instanceof Function) {
          // add classname to button text (for more detail in breadcrumbs)
          const choicesContinueBtn = this.$el.querySelector('.submit-continue-btn > span')
          if (choicesContinueBtn) choicesContinueBtn.classList.add('choices-continue-btn')
        }
      })
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

<style lang="scss" scoped>
@import "@/assets/styles/theme.scss";

.label-style {
  font-size: $px-16;
  font-weight: bold;
  color: $gray9;
}

.launch-icon {
  display: inline-block;
  font-size: $px-14 !important;
  color: $app-blue !important;
}

::v-deep .v-messages__message {
  line-height: 14px !important;
}

::v-deep .read-only-mode .v-input__slot:not(.v-input--checkbox .v-input__slot) {
  background-color: transparent !important;
}

::v-deep .theme--light.v-input--is-disabled input, .theme--light.v-input--is-disabled textarea {
  color: $gray9 !important;
}
</style>
