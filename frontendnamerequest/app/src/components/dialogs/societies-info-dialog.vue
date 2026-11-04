<template>
  <v-dialog
    v-model="showModal"
    width="45rem"
    persistent
    content-class="custom-dialog"
  >
    <v-card>
      <v-row>
        <v-col cols="10">
          <span class="copy-small" />
        </v-col>
        <v-col cols="2">
          <v-icon
            class="float-right"
            md
            color="primary"
            @click="emitClose()"
          >
            mdi-close
          </v-icon>
        </v-col>
      </v-row>
      <v-card-text class="mt-n12">
        <v-container fluid>
          <v-row
            no-gutters
            class="text-center"
          >
            <v-col cols="12">
              To {{ type }} a Society
            </v-col>
            <v-col cols="12">
              please use the Societies Online website
            </v-col>
            <v-col cols="12">
              <a href="https://www.bcregistry.ca/societies/">https://www.bcregistry.ca/societies/</a>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions class="pt-0">
        <v-spacer />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import { ActionBindingIF } from '@/interfaces/store-interfaces'

@Component({})
export default class SocietiesInfo extends Vue {
  @Prop({ required: true }) readonly type: string

  @Getter(useStore) getSocietiesModalVisible!: boolean
  @Action(useStore) setSocietiesModalVisible!: ActionBindingIF

  get showModal () {
    return this.getSocietiesModalVisible
  }

  set showModal (value: boolean) {
    this.setSocietiesModalVisible(value)
  }

  emitClose (): void {
    this.showModal = false
  }
}
</script>
