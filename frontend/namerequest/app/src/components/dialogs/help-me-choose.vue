<template>
  <v-dialog
    v-model="showModal"
    max-width="40%"
  >
    <v-card class="pa-6">
      <v-card-text class="h3">
        Which Entity Type?
      </v-card-text>
      <v-card-text class="copy-normal">
        Media Presentation to display here when it is completed (by way of another initiative not related to NRO)
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          text
          @click="showModal = false"
        >
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import { ActionBindingIF } from '@/interfaces/store-interfaces'

@Component({})
export default class HelpMeChooseDialog extends Vue {
  @Getter(useStore) getHelpMeChooseModalVisible!: boolean
  @Action(useStore) setHelpMeChooseModalVisible!: ActionBindingIF

  get showModal () {
    return this.getHelpMeChooseModalVisible
  }

  set showModal (value: boolean) {
    this.setHelpMeChooseModalVisible(value)
  }
}

</script>
