<template>
  <!-- NB: dummy modal attach point so unit tests can see it -->
  <v-dialog
    v-model="showModal"
    width="50rem"
    attach=""
  >
    <v-card>
      <v-card-title class="d-flex justify-space-between">
        <div>You don't need to request a business name if...</div>
      </v-card-title>
      <v-card-text class="copy-normal">
        <ol>
          <li>
            <b>Your business is already Federally Incorporated.</b><br>
            Please go to <a
              :href="colinLink"
              target="_blank"
            >
              Corporate Online</a> to extra-provincially register your business.
          </li>
          <li class="my-3">
            <b>You want to incorporate a numbered company.</b><br>
            Select the action and the company type you want in the Name Request application and follow the instructions
            to complete your incorporation.
          </li>
          <li>
            <b>You are using your own legal name as the business name.</b><br>
            If you are operating a sole proprietorship or general partnership under your own legal name, you do
            not need to submit a name request or register your business with BC Registries. However, you should inquire
            with the municipality to ensure you have the appropriate business licence(s), if required.
          </li>
        </ol>
      </v-card-text>
      <v-card-actions class="justify-center">
        <v-btn
          id="nr-required-close-btn"
          text
          @click="showModal = false"
        >
          Okay
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
export default class NrNotRequiredDialog extends Vue {
  @Getter(useStore) getNrRequiredModalVisible!: boolean
  @Action(useStore) setNrRequiredModalVisible!: ActionBindingIF

  readonly colinLink = sessionStorage.getItem('CORPORATE_ONLINE_URL')
  readonly businessRegistryLink = 'https://www.bcregistry.ca/business'

  get showModal () {
    return this.getNrRequiredModalVisible
  }
  set showModal (value: boolean) {
    this.setNrRequiredModalVisible(value)
  }
}

</script>

<style lang="scss" scoped>
#nr-required-close-btn {
  width: 6.375rem;
}
a {
  text-decoration: underline;
}
</style>
