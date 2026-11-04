<template>
  <v-col
    id="designation"
    :cols="cols"
    :md="md"
  >
    <v-select
      filled
      hide-details="auto"
      label="Select a Designation"
      :error-messages="getErrors.includes('designation') ? 'Please enter a designation' : ''"
      :items="designationOptions"
      :menu-props="{ bottom: true, offsetY: true}"
      :readonly="!getEntityTypeCd"
      :value="getDesignation"
      @input="setDesignation($event)"
      @change="setClearErrors()"
    />
  </v-col>
</template>

<script lang="ts">
import { Component, Mixins, Prop } from 'vue-property-decorator'
import { CommonMixin, SearchMixin } from '@/mixins'
import { Designations } from '@/list-data'
import { EntityTypes } from '@/enums'

@Component({})
export default class Designation extends Mixins(CommonMixin, SearchMixin) {
  @Prop() readonly cols!: string
  @Prop() readonly md!: string

  get designationOptions (): Array<string> {
    let output = Designations[this.getEntityTypeCd]?.words as string[]
    if (this.getEntityTypeCd === EntityTypes.CC) {
      output = Designations[EntityTypes.CR].words
    }
    return output
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

  .v-select__selection--disabled {
    color: $gray9 !important;
  }

  .theme--light.v-list-item:not(.v-list-item--active):not(.v-list-item--disabled) {
    color: $gray7 !important;
  }
}
</style>
