<template>
  <v-col
    id="request-action"
    :cols="cols"
    :md="md"
  >
    <v-tooltip
      top
      content-class="top-tooltip"
      transition="fade-transition"
      :disabled="!showRequestActionTooltip || isMobile"
    >
      <template #activator="scope">
        <div v-on="scope.on">
          <NestedSelect
            id="request-action-select"
            label="Action"
            :menuItems="RequestActions"
            :errorMessages="getErrors.includes('request_action_cd') ? 'Please select an action' : ''"
            :value="getSearchRequest"
            maxHeight="333"
            @change="setClearErrors(); onRequestActionChange($event)"
          />
        </div>
      </template>

      <span v-if="getSearchRequest">{{ getSearchRequest.text }}</span>
    </v-tooltip>
  </v-col>
</template>

<script lang="ts">
import { Component, Mixins, Prop, Vue, Watch } from 'vue-property-decorator'
import NestedSelect from '@/components/common/nested-select.vue'
import { SearchMixin } from '@/mixins'
import { RequestActionsI } from '@/interfaces'
import { Location } from '@/enums'

@Component({
  components: { NestedSelect }
})
export default class RequestAction extends Mixins(SearchMixin) {
  @Prop({ default: '12' }) readonly cols!: string
  @Prop({ default: '6' }) readonly md!: string

  /** Whether to show the Request Action tooltip. */
  showRequestActionTooltip = false

  /** Called when Request Action menu item is changed. */
  async onRequestActionChange (request: RequestActionsI): Promise<void> {
    this.setSearchRequest(request)

    this.setRequestAction(this.getSearchRequest?.value || null)

    // clear previous state
    this.setSearchBusiness(null)
    this.setSearchJurisdiction(null)
    this.setLocation(null)
    this.setJurisdictionCd(null)
    if (this.entity_type_cd) this.entity_type_cd = null
    this.setSearchCompanyType(null)
    this.setCorpNum(null)
    this.setName('')

    // wait for updates
    await Vue.nextTick()

    if (this.isNewBusiness) {
      this.setExtendedRequestType(this.getSearchRequest)
    }

    if (this.isNewBcBusiness || this.isContinuationIn || this.isConversion) {
      // set default location for requests where there is only one location option
      this.setLocation(Location.BC)
    } else if (this.isAmalgamation) {
      // set initial location for amalgamation - will be overridden later if xpro
      this.setLocation(Location.BC)
    } else if (this.isAssumed && this.getLocation === Location.BC) {
      this.setLocation(Location.CA)
    }

    // calculate whether to show tooltip
    // (after waiting for DOM update)
    await Vue.nextTick()
    const el = document.querySelector('#request-action-select .v-select__selection') as any
    const offsetWidth = el?.offsetWidth as number
    const scrollWidth = el?.scrollWidth as number
    this.showRequestActionTooltip = (offsetWidth < scrollWidth)
  }

  /** Resets fields when returned to the Tabs component */
  @Watch('getDisplayedComponent')
  watchDisplayedComponent (displayedComponent: string) {
    if (displayedComponent === 'Tabs') {
      this.onRequestActionChange(null as RequestActionsI)
    }
  }
}
</script>
