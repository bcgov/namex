<template>
  <v-dialog
    v-model="showModal"
    persistent
    max-width="45rem"
  >
    <v-card>
      <v-card-title class="d-flex justify-space-between mt-n3">
        <div>Exit</div>
        <v-btn
          icon
          large
          class="dialog-close"
          @click="hideModal()"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text class="copy-normal pt-8">
        This will clear all of the information entered including your name choices,
        and return you to the search screen.
      </v-card-text>
      <v-card-actions class="justify-center pt-6">
        <v-btn
          class="px-6"
          @click="exit()"
        >
          Exit
        </v-btn>
        <v-btn
          class="button-blue px-4"
          @click="hideModal()"
        >
          Cancel
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import { DisplayedComponentMixin } from '@/mixins'
import { ActionBindingIF } from '@/interfaces/store-interfaces'

@Component({})
export default class ExitDialog extends DisplayedComponentMixin {
  @Getter(useStore) getExitModalVisible!: boolean
  @Action(useStore) setExitModalVisible!: ActionBindingIF

  get showModal () {
    return this.getExitModalVisible
  }

  set showModal (value: boolean) {
  }

  hideModal () {
    this.setExitModalVisible(false)
  }

  exit () {
    this.hideModal()
    this.cancelAndResetState()
  }
}
</script>
