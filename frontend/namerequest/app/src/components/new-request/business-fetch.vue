<template>
  <!-- once in Summary state, need to re-mount to reuse this component -->
  <div
    v-if="state !== States.SUMMARY"
    id="business-fetch"
  >
    <v-text-field
      v-model.trim="searchField"
      append-icon="mdi-magnify"
      autocomplete="chrome-off"
      autofocus
      filled
      hide-details="auto"
      :hint="hint"
      label="Find an existing business"
      persistent-hint
      :error-messages="errorMessages"
      :loading="state === States.SEARCHING"
      :name="Math.random()"
      :readonly="state === States.SEARCHING"
      @click:append="search()"
      @input="reset()"
      @keydown.tab.exact="search()"
      @keyup.enter="search()"
    />
  </div>
</template>

<script lang="ts">
import { Component, Emit, Vue } from 'vue-property-decorator'
import { Action } from 'pinia-class'
import { useStore } from '@/store'
import { BusinessSearchIF } from '@/interfaces'
import { SearchStates as States } from '@/enums'

//
// See PPR's BusinessSearchAutocomplete.vue for a Composition API example.
//
@Component({})
export default class BusinessFetch extends Vue {
  // enum for template
  readonly States = States

  // Store action
  @Action(useStore) searchBusiness!: (corpNum: string) => Promise<BusinessSearchIF>

  readonly hint = 'Enter the incorporation or registration number (e.g. BC1234567)'

  /** V-model for search field. */
  searchField = ''

  /** For custom error messages. */
  errorMessages = [] as Array<string>

  /** State of this component. */
  state = States.INITIAL

  /** Validates the search field, sets any error messages, and returns validity. */
  private validate (): boolean {
    if (!this.searchField) {
      this.errorMessages = ['Required field']
    } else if (!/^[a-zA-Z]{1,3}( |)\d{7}$/i.test(this.searchField)) {
      this.errorMessages = ['Invalid format for incorporation or registration number']
    } else {
      this.errorMessages = []
    }
    return (this.errorMessages.length === 0)
  }

  /** Clears errors and resets state. Called whenever users changes input. */
  reset (): void {
    this.errorMessages = []
    this.state = States.INITIAL
  }

  /** Searches for business and emits business search object. Called by various events. */
  @Emit('business')
  async search (): Promise<BusinessSearchIF> {
    // safety check
    if (this.state !== States.INITIAL) return

    // validate search field
    const valid = this.validate()
    if (!valid) return

    try {
      // perform search
      this.state = States.SEARCHING
      this.searchField = this.searchField.replace(' ', '').toUpperCase()
      const result = await this.searchBusiness(this.searchField)

      // return result
      if (result) {
        this.state = States.SUMMARY
        return result
      }
    } catch (error) {
      // show actual error message
      this.state = States.INITIAL
      this.errorMessages = [(error as Error).message || 'Business not found']
    }
  }
}
</script>
