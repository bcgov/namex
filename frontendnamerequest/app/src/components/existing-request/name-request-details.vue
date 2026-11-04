<template>
  <div id="name-request-details">
    <v-row class="my-0">
      <v-col
        cols="auto"
        class="font-weight-bold h4 py-0"
      >
        Name Request Details
      </v-col>
    </v-row>

    <v-row class="pt-8 my-0">
      <v-col
        cols="12"
        class="py-0"
      >
        <dl class="pa-6 bg-light-gray">
          <dt>Request Type:</dt>
          <dd>{{ requestType }}</dd>

          <template v-if="isXpro">
            <dt>Home Jurisdiction:</dt>
            <dd>{{ homeJurisdiction }}</dd>
          </template>

          <template v-if="isConversion">
            <dt>Type of Business to Alter Into:</dt>
            <dd>{{ conversionTypeText }}</dd>
          </template>

          <template v-if="isAmalgamation || isNewBcBusiness">
            <dt>Type of New Business:</dt>
            <dd>{{ typeOfBusiness }}</dd>
          </template>

          <template v-else-if="isXpro">
            <dt>Type of Business in B.C.:</dt>
            <dd>{{ typeOfBusiness }}</dd>
          </template>

          <template v-else>
            <dt>Type of Business:</dt>
            <dd>{{ typeOfBusiness }}</dd>
          </template>

          <template v-if="corpNum">
            <dt>For Business:</dt>
            <dd>{{ corpNum }}</dd>
          </template>
        </dl>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Mixins } from 'vue-property-decorator'
import { Getter } from 'pinia-class'
import { useStore } from '@/store'
import { NameRequestI } from '@/interfaces'
import { NrRequestActionCodes } from '@/enums'
import { CommonMixin } from '@/mixins'
import { CanJurisdictions, ConversionTypes, IntlJurisdictions } from '@/list-data'

@Component({})
export default class NameRequestDetails extends Mixins(CommonMixin) {
  @Getter(useStore) getNr!: Partial<NameRequestI>
  @Getter(useStore) getRequestActionCd!: NrRequestActionCodes
  @Getter(useStore) isAmalgamation!: boolean
  @Getter(useStore) isConversion!: boolean
  @Getter(useStore) isNewBusiness!: boolean

  /** The request type of this NR. */
  get requestType (): string {
    return this.requestActionCdToText(this.getRequestActionCd, this.isXpro) || 'Unknown'
  }

  /** The home jurisdiction of the XPRO business. */
  get homeJurisdiction (): string {
    const xproJurisdiction = this.getNr.xproJurisdiction
    // first try to return Canada jurisdiction
    const can = CanJurisdictions.find(j => j.text.toUpperCase() === xproJurisdiction.toUpperCase())
    if (can) return can.text
    // try to return International jurisdiction
    const intl = IntlJurisdictions.find(j => j.text.toUpperCase() === xproJurisdiction.toUpperCase())
    if (intl) return intl.text
    // try to return the original value
    return xproJurisdiction || 'Unknown'
  }

  /** Whether this is an XPRO business. */
  get isXpro (): boolean {
    return this.isXproEntityType(this.getNr.entity_type_cd)
  }

  /** The legal type of the new business. */
  get conversionTypeText (): string {
    const ct = ConversionTypes.find(c => c.value === this.getNr.requestTypeCd)
    return ct?.text || 'Unknown'
  }

  /** Whether this NR is for a new BC (not XPRO) business. */
  get isNewBcBusiness (): boolean {
    return (this.isNewBusiness && !this.isXpro)
  }

  /** The type of business this NR is for. */
  get typeOfBusiness (): string {
    const cd = this.getNr.entity_type_cd
    return this.entityTypeCdToText(cd) || 'Unknown'
  }

  /** The corp num of the business being CNV/CHG/REH. */
  get corpNum (): string {
    return this.getNr.corpNum || null
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/theme.scss";

dl {
  line-height: 2rem;
}

dt {
  color: $gray9;
  font-weight: bold;
  float: left;
  clear: left;
  margin-right: 0.5rem;
}

dd {
  color: $gray7;
}
</style>
