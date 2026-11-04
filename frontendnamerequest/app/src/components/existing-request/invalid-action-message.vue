<template>
  <v-row class="my-3 py-3">
    <v-col
      cols="12"
      class="text-center h4"
    >
      {{ details.heading }}
    </v-col>
    <v-col
      cols="12"
      class="text-center copy-normal mt-n2 mb-2"
      v-html="details.details"
    />
    <v-col
      cols="12"
      class="text-center"
    >
      <v-btn @click="goBack()">
        Return to NR Summary
      </v-btn>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import MainContainer from '@/components/new-request/main-container.vue'
import { NrState } from '@/enums'
import { NameRequestI } from '@/interfaces'
import { ActionBindingIF } from '@/interfaces/store-interfaces'

@Component({
  components: { MainContainer }
})
export default class InvalidActionMessage extends Vue {
  @Getter(useStore) getNr!: Partial<NameRequestI>

  @Action(useStore) setActiveComponent!: ActionBindingIF

  get stateCd (): string {
    return (this.getNr?.stateCd || '')
  }

  get details () {
    switch (this.stateCd) {
      case NrState.APPROVED:
      case NrState.CONDITIONAL:
      case NrState.REJECTED:
        return {
          heading: 'We have finished examining your Name Request',
          details: 'Your request has been ' +
            (this.stateCd === NrState.CONDITIONAL ? 'CONDITIONALLY APPROVED' : this.stateCd) +
            '.'
        }
      case NrState.CANCELLED:
        return {
          heading: 'Unfortunately your Name Request has been CANCELLED',
          details: 'Please contact <i>Registries and Online Services</i> at 250-387-7848 if you require ' +
           'further assistance.'
        }
      default:
        return {
          heading: 'Your Name Request is currently being examined',
          details: 'Please check back later to see the result.'
        }
    }
  }

  async goBack () {
    this.setActiveComponent('ExistingRequestDisplay')
  }
}
</script>
