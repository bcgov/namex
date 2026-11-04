<template>
  <v-text-field
    id="name-input-component"
    ref="nameInputRef"
    v-model="searchValue"
    :error-messages="message"
    autocomplete="chrome-off"
    :filled="!isReadOnly"
    :rules="getRules"
    :label="label"
    :class="{ 'read-only-mode': isReadOnly }"
    :disabled="isReadOnly"
    :hint="hint"
    hide-details="auto"
    persistent-hint
    @input="setClearErrors()"
    @blur="handleBlur()"
    @keydown.enter="handleSubmit($event)"
  />
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch, Emit } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { sanitizeName } from '@/plugins'
import { DFLT_MIN_LENGTH, DFLT_MAX_LENGTH, MRAS_MIN_LENGTH, MRAS_MAX_LENGTH }
  from '@/components/new-request/constants'
import { checkInvalidDesignation } from '@/list-data/designations'

@Component({})
export default class NameInput extends Vue {
  /** Whether to perform MRAS search. */
  @Prop({ default: false }) readonly isMrasSearch!: boolean

  /** Whether this component is read-only (eg, on name check page). */
  @Prop({ default: false }) readonly isReadOnly!: boolean

  /** Hint to show (eg, on name check page). */
  @Prop({ default: null }) readonly hint!: string

  @Getter(useStore) getCorpSearch!: string
  @Getter(useStore) getErrors!: string[]
  @Getter(useStore) getHasNoCorpNum!: boolean
  @Getter(useStore) getName!: string
  @Getter(useStore) isMrasJurisdiction!: boolean
  @Getter(useStore) isXproFlow!: boolean
  @Getter(useStore) getEntityTypeCd!: string

  @Action(useStore) setClearErrors!: () => void
  @Action(useStore) setCorpSearch!: ActionBindingIF
  @Action(useStore) setName!: ActionBindingIF
  @Action(useStore) setMrasSearchInfoModalVisible!: ActionBindingIF
  @Action(useStore) startAnalyzeName!: ActionBindingIF

  readonly defaultRules = [
    v => (!v || v.length >= DFLT_MIN_LENGTH) || `Must be at least ${DFLT_MIN_LENGTH} characters`,
    v => (!v || v.length <= DFLT_MAX_LENGTH) || `Cannot exceed ${DFLT_MAX_LENGTH} characters`
  ]

  nameInputComponent = null

  mounted (): void {
    // ref is only valid after component is mounted
    this.nameInputComponent = this.$refs['nameInputRef']
  }

  get getRules (): any[] {
    if (this.searchValue) {
      if (this.isMrasSearch) {
        return this.mrasRules
      }
      if (this.isXproFlow) {
        return this.xproRules
      }
    }
    return this.defaultRules
  }

  /** The array of validation rules for the MRAS corp num. */
  get mrasRules (): any[] {
    return [
      v => (/^[0-9a-zA-Z-]+$/.test(v) || 'A corporate number is required'),
      v => (!v || v.length >= MRAS_MIN_LENGTH) || `Must be at least ${MRAS_MIN_LENGTH} characters`,
      v => (!v || v.length <= MRAS_MAX_LENGTH) || `Cannot exceed ${MRAS_MAX_LENGTH} characters`
    ]
  }

  get xproRules (): any[] {
    return [
      v => (!v || v.length >= MRAS_MIN_LENGTH) || `Must be at least ${MRAS_MIN_LENGTH} characters`,
      v => (!v || v.length <= MRAS_MAX_LENGTH) || `Cannot exceed ${MRAS_MAX_LENGTH} characters`
    ]
  }

  /** Local validator when input is a MRAS corp num. */
  get isCorpNumValid (): boolean {
    if (this.isMrasSearch) return this.nameInputComponent?.valid || false
    return true
  }

  get label (): string {
    if (this.isReadOnly && (this.isMrasSearch || !this.isXproFlow)) return '' // should never happen

    if (this.isReadOnly && this.isXproFlow) return 'Name in home jurisdiction'

    if (this.isXproFlow) {
      if (this.isMrasJurisdiction && !this.getHasNoCorpNum) {
        return 'Enter the corporate number assigned by the home jurisdiction'
      } else {
        return 'Business\'s full legal name in home jurisdiction'
      }
    }

    return 'Enter a name to request'
  }

  get message (): string[] {
    if (this.getErrors.includes('name')) {
      if (this.isXproFlow) {
        if (this.isMrasJurisdiction && !this.getHasNoCorpNum) {
          return ['Please enter a corporation number to search for']
        } else {
          return ['Please enter the business\'s full legal name in home jurisdiction']
        }
      }
      return ['Please enter a name for the business']
    }

    if (this.getErrors.includes('min_length')) {
      return ['Please enter a longer name']
    }

    if (this.getErrors.includes('max_length')) {
      let maxCharacters = DFLT_MAX_LENGTH
      if (this.isXproFlow) {
        maxCharacters = MRAS_MAX_LENGTH
      }

      return [`Cannot exceed ${maxCharacters} characters`]
    }

    const invalidDesignationMsg = checkInvalidDesignation(this.getEntityTypeCd, this.searchValue)
    if (invalidDesignationMsg) {
      return [invalidDesignationMsg]
    }

    return null
  }

  get searchValue (): string {
    return this.isMrasSearch ? this.getCorpSearch : this.getName
  }

  set searchValue (value: string) {
    this.isMrasSearch ? this.setCorpSearch(value) : this.setName(value)
  }

  handleBlur (): void {
    // The leading and trailing spaces need to be removed when name input finished,
    // using sanitizeName() which has was used in name-capture to do the work.
    this.searchValue = sanitizeName(this.searchValue)
  }

  async handleSubmit (event: KeyboardEvent) {
    if (event.key === 'Enter' && this.isCorpNumValid) {
      event.preventDefault()
      if (this.searchValue) {
        // hide modal and perform name analysis
        this.setMrasSearchInfoModalVisible(false)
        this.$root.$emit('showSpinner', true)
        await this.startAnalyzeName(null)
        this.$root.$emit('showSpinner', false)
      }
      return
    }
    return event
  }

  @Watch('isCorpNumValid')
  @Emit() private emitCorpNumValidity () {
    return this.isCorpNumValid
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';

.search-tooltip {
  max-width: 100px;
  text-align: center;
  padding: 10px !important;
}

::v-deep .read-only-mode .v-input__slot:not(.v-input--checkbox .v-input__slot) {
  background-color: transparent !important;
}

::v-deep .theme--light.v-input--is-disabled input, .theme--light.v-input--is-disabled textarea {
  color: $gray9 !important;
}
</style>
