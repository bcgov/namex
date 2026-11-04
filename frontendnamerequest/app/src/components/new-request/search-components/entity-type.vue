<template>
  <v-col
    id="entity-type"
    :cols="cols"
    :md="md"
  >
    <v-tooltip
      top
      content-class="top-tooltip"
      :disabled="!isConversion || !entityConversionText || isMobile"
      transition="fade-transition"
    >
      <template #activator="scope">
        <div v-on="scope.on">
          <v-select
            id="entity-type-options-select"
            ref="selectBusinessTypeRef"
            :label="isConversion ? 'Select type of business to alter into' : 'Select type of business in B.C.'"
            :error-messages="getErrors.includes('entity_type_cd') ? 'Please select a business type' : ''"
            :items="entityTypeOptions"
            :menu-props="{ bottom: true, offsetY: true}"
            hide-details="auto"
            filled
            :value="isConversion ? getOriginEntityTypeCd : entity_type_cd"
            @change="setClearErrors(); entity_type_cd = $event"
          >
            <template #item="{ item }">
              <v-tooltip
                :right="isScreenLg"
                :left="!isScreenLg"
                :disabled="!item.blurbs || isMobile"
                :content-class="!isScreenLg ? 'left-tooltip' : ''"
                transition="fade-transition"
              >
                <template #activator="scope2">
                  <span
                    class="list-item"
                    :class="{ 'last-select-item': item.value === 'INFO' }"
                    v-on="scope2.on"
                  >{{ item.text }}</span>
                </template>

                <div
                  v-for="(blurb, index) in entityBlurbs(item.value)"
                  :key="`blurb-${index}`"
                >
                  <span :class="{ 'tooltip-bullet': index !== 0}">
                    {{ blurb }}
                  </span>
                </div>
              </v-tooltip>
            </template>
          </v-select>
        </div>
      </template>

      <span>{{ entityConversionText }}</span>
    </v-tooltip>
  </v-col>
</template>

<script lang="ts">
import { Component, Mixins, Prop, Watch } from 'vue-property-decorator'
import { FormType } from '@/interfaces'
import { EntityTypes, NrRequestTypeCodes } from '@/enums'
import { ConversionTypes } from '@/list-data'
import { SearchMixin } from '@/mixins'

@Component({})
export default class EntityType extends Mixins(SearchMixin) {
  @Prop({ default: '12' }) readonly cols!: string
  @Prop({ default: '6' }) readonly md!: string

  // Refs
  $refs!: {
    selectBusinessTypeRef: FormType
  }

  // FUTURE: clean up return type
  entityBlurbs (entityType: EntityTypes | NrRequestTypeCodes): string | string[] | string[][] {
    return this.getEntityBlurbs.find(type => type.value === entityType)?.blurbs
  }

  get entityTypeOptions () {
    return (this.isConversion ? this.getConversionTypeOptions : this.getEntityTypeOptions)
  }

  get entityConversionText () {
    // convert NrRequestTypeCodes -> EntityTypes
    return ConversionTypes.find(conversion => conversion.value === this.getConversionType)?.text
  }

  // FUTURE: move this into setter?
  @Watch('getEntityTypeCd')
  private clearDesignation () {
    this.setDesignation('')
    this.setSearchCompanyType('')
    // clear "Select a Business Type" field when "View all business types" is selected
    if (!this.getEntityTypeCd || this.getEntityTypeCd === EntityTypes.INFO) {
      this.$refs.selectBusinessTypeRef && this.$refs.selectBusinessTypeRef.reset()
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';

.v-list {
  padding: 0;
}

.list-item {
  width: 100%;
  padding: 8px;
}

.last-select-item {
  border-top: 1px solid $gray3;
  padding: 20px 8px !important;
}

// set content colour when hovering over list items
.v-list-item:hover .v-list-item__content,
.list-item:hover {
  color: $app-blue !important;
}

// Vuetify overrides
::v-deep {
  .v-select:not(.v-select--is-multi).v-text-field--single-line .v-select__selections{
    line-height: 2;
  }

  .v-select__selections {
    line-height: 20px !important;
  }

  .v-input--is-disabled .v-input__icon {
    display: none !important;
  }

  .v-select__selection--disabled {
    color: $gray9 !important;
  }

  // reduce checkbox height when there are no error messages
  .v-messages:not(.error--text) {
    margin-bottom: -22px;
  }

  .theme--light.v-list-item:not(.v-list-item--active):not(.v-list-item--disabled) {
    color: $gray7 !important;
  }
}
</style>
