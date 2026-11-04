<template>
  <v-dialog
    v-model="showModal"
    max-width="40%"
  >
    <v-card class="pa-9">
      <v-card-text class="h4">
        {{ nameObject.name }}
      </v-card-text>
      <v-card-text class="h5 my-n2">
        Has been approved, subject to the following conditions:
      </v-card-text>
      <v-card-text class="copy-normal">
        <div class="pre-line px-2 pt-2 mb-n6">
          {{ nameObject.decision_text }}
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          id="nr-required-close-btn"
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
import { NameState } from '@/enums'
import { ActionBindingIF } from '@/interfaces/store-interfaces'

@Component({})
export default class ConditionsDialog extends Vue {
  @Getter(useStore) getConditionsModalVisible!: boolean
  @Getter(useStore) getNrNames!: any
  @Action(useStore) setConditionsModalVisible!: ActionBindingIF

  get nameObject () {
    const name = (this.getNrNames || []).find(name => name.state === NameState.CONDITIONAL && name.decision_text)
    return name || {}
  }
  get showModal () {
    return this.getConditionsModalVisible
  }
  set showModal (value: boolean) {
    this.setConditionsModalVisible(value)
  }
}
</script>
