<template>
  <v-dialog
    v-model="display"
    width="45rem"
    persistent
    :attach="attach"
  >
    <v-card>
      <v-card-title>
        <v-row no-gutters>
          <v-col
            cols="6"
            class="text-end"
          >
            <v-icon
              class="mr-n4"
              :color="options.iconColor"
              size="2.5rem"
            >
              {{ options.icon }}
            </v-icon>
          </v-col>
          <v-col>
            <v-btn
              cols="6"
              class="close-btn outlined"
              icon
              :ripple="false"
              size="2.5rem"
              @click="proceed(false)"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-title>
      <v-card-text class="pt-7">
        <p class="dialog-title ma-0 pb-10">
          {{ options.title }}
        </p>
        <p
          v-for="line, index in options.text"
          :key="`options-text-${index}`"
          class="copy-normal ma-0 pb-5"
          v-html="line"
        />
      </v-card-text>
      <v-card-actions class="pt-7">
        <v-row
          justify="center"
          no-gutters
        >
          <v-col
            v-if="options.cancelText"
            cols="12"
            md="auto"
            lg="auto"
          >
            <v-btn
              class="cancel-btn outlined"
              outlined
              @click="proceed(false)"
            >
              {{ options.cancelText }}
            </v-btn>
          </v-col>
          <v-col
            v-if="options.acceptText"
            :class="{'pl-3': !isMobile}"
            cols="12"
            md="auto"
            lg="auto"
          >
            <v-btn
              class="accept-btn"
              @click="proceed(true)"
            >
              {{ options.acceptText }}
              <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Vue, Prop, Emit } from 'vue-property-decorator'
import { Getter } from 'pinia-class'
import { useStore } from '@/store'
import { DialogOptionsI } from '@/interfaces'

@Component({})
export default class NameCheckIssuesDialog extends Vue {
  @Prop() readonly attach: string
  @Prop() readonly display: boolean
  @Prop() readonly options: DialogOptionsI

  @Getter(useStore) isMobile!: boolean

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  @Emit() proceed (val: boolean) { }
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';
.cancel-btn {
  @media only screen and (max-width: 600px) {
    width: 100%;
  }
}
.accept-btn {
  font-size: $px-14 !important;
  font-weight: bold;

  @media only screen and (max-width: 600px) {
    margin-top: 10px;
    width: 100%;
  }
}
.close-btn {
  float: right;
  box-shadow: none !important;
}
.close-btn:before {
  box-shadow: none !important;
  background-color: transparent !important;
}
.dialog-title {
  color: $gray9;
  font-size: $px-24;
  font-weight: bold;
  text-align: center;
}
</style>
