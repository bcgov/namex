<template>
  <v-container
    fluid
    class="white rounded copy-normal pa-10"
  >
    <v-row
      justify="space-between"
      class="submission-tabs-top"
      no-gutters
    >
      <slot name="container-header" />

      <v-col
        v-if="displayedComponent !== 'Success'"
        cols="auto"
        class="py-0"
      >
        <button
          id="back-to-search-btn"
          class="modal-activator link-std-sans-ul"
          @click="backToSearch()"
        >
          <span class="link-std-sans-ul">
            <template v-if="showExit">
              Exit
              <v-icon class="dialog-close">mdi-close</v-icon>
            </template>
            <template v-else-if="getEditMode">
              <v-icon class="mr-n1 mini-back-arrow">mdi-chevron-left</v-icon>
              Return
            </template>
            <template v-else>
              <v-icon class="mr-n1 mini-back-arrow">mdi-chevron-left</v-icon>
              Start Over
            </template>
          </span>
        </button>
      </v-col>
    </v-row>

    <slot name="content" />
  </v-container>
</template>

<script lang="ts">
import { Component, Mixins } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import { DisplayedComponentMixin } from '@/mixins'
import { ActionBindingIF } from '@/interfaces/store-interfaces'

@Component({})
export default class MainContainer extends Mixins(DisplayedComponentMixin) {
  @Getter(useStore) getEditMode!: boolean
  @Getter(useStore) getSubmissionTabNumber!: number
  @Getter(useStore) isMobile!: boolean

  @Action(useStore) setExitModalVisible!: ActionBindingIF
  @Action(useStore) setExitIncompletePaymentVisible!: ActionBindingIF

  componentName = ''

  private mounted () {
    this.$nextTick(() => {
      if (this.$el?.querySelector instanceof Function) {
        // add classname to button text (for more detail in breadcrumbs)
        if (this.showExit) {
          const exitBtn = this.$el.querySelector('#back-to-search-btn > span')
          if (exitBtn) exitBtn.classList.add('exit-btn')
        } else if (this.getEditMode) {
          const returnBtn = this.$el.querySelector('#back-to-search-btn > span')
          if (returnBtn) returnBtn.classList.add('return-btn')
        } else {
          const startSearchOverBtn = this.$el.querySelector('#back-to-search-btn > span')
          if (startSearchOverBtn) startSearchOverBtn.classList.add('start-search-over-btn')
        }
      }
    })
  }

  get showExit (): boolean {
    return [2, 3].includes(this.getSubmissionTabNumber) ||
      this.getDisplayedComponent === 'ExistingRequestDisplay'
  }

  backToSearch () {
    if ([2, 3].includes(this.getSubmissionTabNumber) && !this.getEditMode &&
      this.getDisplayedComponent !== 'ExistingRequestDisplay') {
      this.setExitModalVisible(true)
    } else if (this.getDisplayedComponent === 'ExistingRequestDisplay' && this.isIncompletePayment) {
      this.setExitIncompletePaymentVisible(true)
    } else {
      this.cancelAndResetState()
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/theme.scss";

#back-to-search-btn:focus {
  outline: 0;
}

.mdi-close,
.mini-back-arrow {
  top: -1px !important;
  color: $app-blue !important;
}
</style>
