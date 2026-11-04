<template>
  <v-col
    id="company-type"
    :cols="cols"
    :md="md"
  >
    <header
      v-if="!hideCompanyTypeSelection"
      class="h6"
    >
      Select a company type:
    </header>

    <v-radio-group
      v-if="!hideCompanyTypeSelection"
      class="mt-0 pt-6"
      hide-details
      mandatory
      row
      :value="getSearchCompanyType"
      @change="setSearchCompanyType($event)"
    >
      <v-radio
        id="named-company-radio"
        label="Named Company"
        :value="CompanyTypes.NAMED_COMPANY"
      />
      <v-radio
        id="numbered-company-radio"
        label="Numbered Company"
        :value="CompanyTypes.NUMBERED_COMPANY"
      />
    </v-radio-group>
  </v-col>
</template>

<script lang="ts">
import { Component, Mixins, Prop } from 'vue-property-decorator'
import { SearchMixin } from '@/mixins'

@Component({})
export default class CompanyType extends Mixins(SearchMixin) {
  @Prop({ default: '12' }) readonly cols!: string
  @Prop({ default: '6' }) readonly md!: string

  mounted () : void {
    if (this.hideCompanyTypeSelection) {
      this.setSearchCompanyType(this.CompanyTypes.NAMED_COMPANY)
    }
  }

  get hideCompanyTypeSelection () : boolean {
    return this.isChangeName && this.isNumberedCompanyName(this.getSearchBusiness?.legalName ?? '')
  }

  isNumberedCompanyName (name: string) : boolean {
    const numberedCompanyPattern = /^\d{7} B\.C\. LTD\.$/
    return numberedCompanyPattern.test(name)
  }
}
</script>

<style lang="scss" scoped>
::v-deep {
  // override radio group background color
  .v-input--radio-group .v-input__control .v-input__slot {
    background-color: white !important;
  }
}
</style>
