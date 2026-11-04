<template>
  <v-col
    id="business-lookup-fetch"
    :cols="cols"
    :md="md"
  >
    <template v-if="!getSearchBusiness">
      <BusinessFetch
        v-if="isRestoration"
        @business="onBusiness($event)"
      />
      <template v-else>
        <BusinessLookup
          v-if="isAuthenticated"
          :searchStatus="lookupActiveOrHistorical"
          @business="onBusiness($event)"
        />
        <BusinessFetch
          v-else
          @business="onBusiness($event)"
        />
      </template>
    </template>
    <v-form
      v-else
      ref="businessLookupTextFieldForm"
    >
      <v-text-field
        append-icon="mdi-close"
        readonly
        filled
        :label="label"
        :value="getSearchBusiness.legalName"
        :rules="rules"
        :hint="hint"
        @click:append="onBusiness(null)"
        @keyup.delete="onBusiness(null)"
        @keydown.enter.native.prevent
      />
    </v-form>
  </v-col>
</template>

<script lang="ts">
import { Component, Mixins, Prop, Vue } from 'vue-property-decorator'
import BusinessFetch from '@/components/new-request/business-fetch.vue'
import BusinessLookup from '@/components/new-request/business-lookup.vue'
import SocietiesInfo from '@/components/dialogs/societies-info-dialog.vue'
import { BusinessSearchIF, FormType } from '@/interfaces'
import { CorpTypeCd, CompanyTypes, EntityStates, Location } from '@/enums'
import { CommonMixin, SearchMixin } from '@/mixins'

@Component({
  components: { BusinessFetch, BusinessLookup, SocietiesInfo }
})
export default class BusinessLookupFetch extends Mixins(CommonMixin, SearchMixin) {
  @Prop({ default: '12' }) readonly cols!: string
  @Prop({ default: '6' }) readonly md!: string

  // Refs
  $refs!: {
    businessLookupTextFieldForm: FormType
    selectBusinessTypeRef: FormType
  }

  get rules (): any {
    return [
      () => {
        if (this.isConversion) {
          return this.isAlterable || 'This business cannot alter their business type'
        } else if (this.isRestoration) {
          return this.isRestorable || 'This business cannot be reactivated'
        } else if (this.isChangeName) {
          return this.isNameChangeable || 'This business cannot change their business name'
        }
        return true
      }]
  }

  get label (): string {
    if (this.isAuthenticated) {
      if (this.lookupActiveOrHistorical === EntityStates.HISTORICAL) {
        return 'Find a historical business'
      } else {
        return 'Find an existing business'
      }
    } else {
      if (this.lookupActiveOrHistorical === EntityStates.HISTORICAL) {
        return 'Fetch a historical business'
      } else {
        return 'Fetch an existing business'
      }
    }
  }

  get hint (): string {
    if (this.isAuthenticated) {
      return 'Search by name, incorporation or registration number of existing business'
    } else {
      return 'Enter registration number of existing business'
    }
  }

  /** Search businesses with business lookup depending on the Action selected. */
  get lookupActiveOrHistorical (): string {
    return this.isRestoration ? EntityStates.HISTORICAL : EntityStates.ACTIVE
  }

  /** Event handled for business lookup/fetch. */
  async onBusiness (business: BusinessSearchIF): Promise<void> {
    this.setSearchBusiness(business)
    this.entity_type_cd = this.getSearchBusiness?.legalType || null
    this.setCorpNum(business?.identifier || null)
    this.setEntityTypeCd(this.entity_type_cd)
    this.setName('')
    this.setSearchCompanyType('')

    // Waiting for DOM update to be able to access the Ref. Trigger form validation.
    // Need to do that because the ref is in a conditional.
    await Vue.nextTick()
    if (this.getSearchBusiness) this.$refs.businessLookupTextFieldForm.validate()

    if (this.isConversion) {
      if (this.getSearchBusiness) {
        // set the from business for alteration (conversion)
        this.setOriginEntityTypeCd(this.getSearchBusiness.legalType)
        // check if business is in Lear and set store value of isLearBusiness flag
        await this.checkBusinessInLear(this.getSearchBusiness.identifier)
      } else {
        // clear all related fields when clearing business search/fetch for alter
        this.setConversionType(null)
        this.setOriginEntityTypeCd(null)
        this.setSearchCompanyType(null)
      }
    }

    if (this.isRestoration) {
      // Check if not XPRO and BC restorable
      if (!this.isSelectedXproAndRestorable && this.isBcRestorable) {
        this.setLocation(Location.BC)
        const corpType = this.getSearchBusiness?.legalType as unknown as CorpTypeCd || null
        this.setEntityTypeCd(this.corpTypeToEntityType(corpType))
      } else if (this.isSelectedXproAndRestorable) { // Check if XPRO and restorable
        this.setLocation(Location.CA)
        const corpType = this.getSearchBusiness?.legalType as unknown as CorpTypeCd || null
        this.setEntityTypeCd(this.corpTypeToEntityType(corpType) || this.getSearchBusiness?.legalType || null)
      } else {
        this.setEntityTypeCd(null)
      }

      // check if business is in Lear and set store value of isLearBusiness flag
      await this.checkBusinessInLear(this.getSearchBusiness?.identifier)
    }

    if (this.isChangeName) {
      if (this.getSearchBusiness) {
        if (this.isBcBenCccUlc) {
          this.setLocation(Location.BC)
          const corpType = this.getSearchBusiness.legalType as unknown as CorpTypeCd
          this.setEntityTypeCd(this.corpTypeToEntityType(corpType))
        } else {
          this.setSearchCompanyType(CompanyTypes.NAMED_COMPANY)
          this.setLocation(Location.BC)
          const corpType = this.getSearchBusiness.legalType as unknown as CorpTypeCd
          this.setEntityTypeCd(this.corpTypeToEntityType(corpType) || this.getSearchBusiness.legalType)
        }

        if (this.isChangeNameXpro) {
          this.setLocation(Location.CA)
          const corpType = this.getSearchBusiness.legalType as unknown as CorpTypeCd
          this.setEntityTypeCd(this.corpTypeToEntityType(corpType) || this.getSearchBusiness.legalType)
        }

        // check if business is in Lear and set store value of isLearBusiness flag
        await this.checkBusinessInLear(this.getSearchBusiness.identifier)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';

// make the business lookup close button always blue
::v-deep #business-lookup button.mdi-close {
  color: $app-blue;
}
</style>
