<template>
  <v-row
    id="link-row"
    class="links-row text-body-4 px-2 my-0"
    :class="{ 'links-row-mobile' : isMobile }"
  >
    <v-col
      cols="12"
      md="4"
      lg="4"
    >
      <a
        class="nr-required-activator"
        :class="{ 'no-selector-link' : !entitySelectorUrl }"
        @click="activateNRRModal()"
      >
        <v-icon color="primary">mdi-help-circle-outline</v-icon>&nbsp;Check if you need a Name Request
      </a>
    </v-col>
    <v-col
      cols="12"
      md="4"
      lg="4"
    >
      <a
        class="name-build-link"
        :class="{ 'no-selector-link' : !entitySelectorUrl }"
        href="#"
        onclick="return false;"
        @click="scrollTo('name-build-info')"
      >
        <v-icon color="primary">mdi-help-circle-outline</v-icon>&nbsp;Learn how to build a name
      </a>
    </v-col>
    <v-col
      cols="12"
      md="4"
      lg="4"
    >
      <a
        v-if="entitySelectorUrl"
        class="entity-selector-link"
        :href="entitySelectorUrl"
        target="_blank"
      >
        <v-icon color="primary">mdi-help-circle-outline</v-icon>&nbsp;Help me choose a business type
        <v-icon
          color="primary"
          x-small
        >mdi-open-in-new</v-icon>
      </a>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Mixins } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import { CommonMixin } from '@/mixins'
import { ActionBindingIF } from '@/interfaces/store-interfaces'

@Component({})
export default class LinkRow extends Mixins(CommonMixin) {
  @Action(useStore) setNrRequiredModalVisible!: ActionBindingIF

  @Getter(useStore) isMobile!: boolean

  /** The Entity Selector Tool URL. */
  get entitySelectorUrl (): string {
    return sessionStorage.getItem('ENTITY_SELECTOR_URL')
  }

  activateNRRModal () {
    this.setNrRequiredModalVisible(true)
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';

.links-row {
  background-color: $gray1;
  text-align: center;

  :hover {
    background-color: $app-lt-blue;
  }

  a {
    width: 33%;
    text-decoration: none;
  }

  .no-selector-link {
    width: 50% !important;
  }

  .middle-link {
    border-left: 1px solid #DEE2E6;
    border-right: 1px solid #DEE2E6;
  }
}

.links-row-mobile {
  text-align: start;
  a {
    padding-left: 30px;
  }
}
</style>
