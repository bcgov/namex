<template>
  <v-col
    id="jurisdiction"
    :cols="cols"
    :md="md"
  >
    <NestedSelect
      label="Select your home jurisdiction"
      :menuItems="jurisdictionOptions"
      :error-messages="getErrors.includes('jurisdiction') ? 'Please select a jurisdiction' : ''"
      :value="getSearchJurisdiction"
      @change="setClearErrors(); onJurisdictionChange($event)"
    />
  </v-col>
</template>

<script lang="ts">
import { Component, Mixins, Prop } from 'vue-property-decorator'
import NestedSelect from '@/components/common/nested-select.vue'
import { CorpTypeCd, Location } from '@/enums'
import { SearchMixin } from '@/mixins'
import { CanJurisdictions, IntlJurisdictions } from '@/list-data'

@Component({
  components: { NestedSelect }
})
export default class Jurisdiction extends Mixins(SearchMixin) {
  @Prop({ default: '12' }) readonly cols!: string
  @Prop({ default: '6' }) readonly md!: string

  get jurisdictionOptions (): Array<any> {
    const array = [] as Array<any>

    // add in Canadian jurisdictions (not including BC)
    array.push({ isHeader: true, group: 0, text: 'Canadian' })
    CanJurisdictions
      .filter(jur => jur.value !== Location.BC)
      .forEach(jur => array.push({
        group: 0,
        text: jur.text,
        value: jur.value,
        separator: (jur.value === Location.FD)
      }))

    // add in International jurisdictions (not including CA)
    array.push({ isHeader: true, group: 1, text: 'International' })
    IntlJurisdictions
      .filter(jur => jur.value !== Location.CA)
      .forEach(jur => array.push({
        group: 1,
        text: jur.text,
        value: jur.value,
        separator: false
      }))

    return array
  }

  /** Called when Jurisdiction menu item is changed. */
  onJurisdictionChange (jurisdiction: any): void {
    this.setSearchJurisdiction(jurisdiction)
    this.setLocation(jurisdiction.group === 0 ? Location.CA : Location.IN)
    this.setJurisdictionCd(jurisdiction.value)

    // if a business was previously selected, reset the entity type
    if (this.getSearchBusiness) {
      const corpType = this.getSearchBusiness.legalType as unknown as CorpTypeCd
      this.setEntityTypeCd(this.corpTypeToEntityType(corpType) || this.getSearchBusiness.legalType)
    }
    this.setCorpSearch('')
  }
}
</script>
