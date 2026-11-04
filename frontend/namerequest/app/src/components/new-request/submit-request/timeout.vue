<template>
  <v-row>
    <v-col
      cols="12"
      class="text-center h4"
    >
      Request Timed Out
    </v-col>
    <v-col
      cols="12"
      class="text-center mt-n3"
    >
      Unfortunately you took too long to complete your submission. Please try again from the beginning.
    </v-col>
    <v-col
      cols="12"
      class="text-center"
    >
      <v-btn @click="restart">
        Search Again
      </v-btn>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import MainContainer from '@/components/new-request/main-container.vue'
import { Action } from 'pinia-class'
import { useStore } from '@/store'
import { ActionBindingIF } from '@/interfaces/store-interfaces'

@Component({
  components: { MainContainer }
})
export default class Timeout extends Vue {
  @Action(useStore) resetAnalyzeName!: ActionBindingIF
  @Action(useStore) setActiveComponent!: ActionBindingIF

  async restart () {
    await this.resetAnalyzeName(null)
    this.setActiveComponent('Tabs')
  }
}
</script>
