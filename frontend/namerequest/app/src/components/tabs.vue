<template>
  <v-container id="tabs-landing-comp">
    <v-tabs
      v-model="tabNumber"
      active-class="active-tab"
      style="border-radius: 4px 4px 0 0"
      hide-slider
      height="64"
      centered
      grow
    >
      <v-tab
        id="new-tab"
        :ripple="false"
        class="upper-border"
        :class="{ 'mt-1': tabNumber === 1 }"
        tabindex="0"
      >
        <v-icon
          v-if="!isMobile"
          class="mr-3"
        >
          mdi-domain
        </v-icon>
        <span :class="[tabNumber === 0 ? 'h5' : 'h5-lt', { 'mobile-font' : isMobile }]">Get a Business Name or Start a
          Numbered Business</span>
      </v-tab>

      <v-tab
        id="existing-tab"
        :ripple="false"
        class="upper-border"
        :class="{ 'mt-1': tabNumber === 0 }"
        tabindex="1"
      >
        <v-icon
          v-if="!isMobile"
          class="mr-3"
        >
          mdi-file-document-edit-outline
        </v-icon>
        <span :class="[tabNumber === 1 ? 'h5' : 'h5-lt', { 'mobile-font' : isMobile }]">Manage My Name Request</span>
      </v-tab>

      <v-tabs-items
        v-model="tabNumber"
        class="rounded-b tab-items"
        touchless
      >
        <v-tab-item>
          <Search />
          <LinkRow />
        </v-tab-item>

        <v-tab-item>
          <ExistingRequestSearch />
        </v-tab-item>
      </v-tabs-items>
    </v-tabs>
  </v-container>
</template>

<script lang="ts">
import { Component, Mixins, Watch } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import { CommonMixin } from '@/mixins'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import Search from '@/components/new-request/search.vue'
import ExistingRequestSearch from './existing-request/existing-request-search.vue'
import LinkRow from '@/components/common/link-row.vue'

@Component({
  components: {
    ExistingRequestSearch,
    LinkRow,
    Search
  }
})
export default class Tabs extends Mixins(CommonMixin) {
  @Getter(useStore) getTabNumber!: number
  @Getter(useStore) isMobile!: boolean

  @Action(useStore) setTabNumber!: ActionBindingIF

  get tabNumber () {
    return this.getTabNumber
  }

  set tabNumber (tab: number) {
    this.setTabNumber(tab)
  }

  @Watch('tabNumber')
  private scrollToTop () {
    this.scrollTo('namerequest-sbc-header')
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';

.mobile-font {
  font-size: $px-14;
}

#tabs-landing-comp {
  max-width: 1140px !important;
  padding: 0 !important;
}

#new-tab, #existing-tab {
  min-height: 64px;
  background-color: $BCgovBlue5;
}

#new-tab {
  width: 67%;
}

#existing-tab {
  width: 33%;
}

.upper-border {
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
  min-height: 58px;
  max-height: 58px;
  margin: 0 2.5px;
}

::v-deep .v-tab:before {
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

::v-deep .theme--light.v-tabs > .v-tabs-bar{
  background-color: transparent;
}

::v-deep .theme--light.v-tabs > .v-tabs-bar .v-tab:not(.v-tab--active) > .v-icon {
  color: white;
  transition: none !important;
}
</style>
