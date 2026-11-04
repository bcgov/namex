<template>
  <v-dialog
    v-model="dialog"
    width="45rem"
    persistent
    :attach="attach"
  >
    <v-card>
      <v-card-title id="dialog-title">
        {{ title }}
      </v-card-title>

      <v-card-text id="dialog-text">
        <!-- display message -->
        <div class="general-error">
          <p>{{ dialogText }}</p>
        </div>
      </v-card-text>

      <v-divider class="my-0" />

      <v-card-actions>
        <v-spacer />
        <v-btn
          id="dialog-cancel-button"
          class="dialog-close"
          text
          @click="close()"
        >
          Cancel
        </v-btn>
        <v-btn
          id="dialog-try-again-button"
          class="dialog-close"
          text
          @click="tryAgain()"
        >
          Try Again
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Vue, Prop, Emit } from 'vue-property-decorator'
import { Getter } from 'pinia-class'
import { useStore } from '@/store'

@Component({})
export default class CreateBusinessErrorDialog extends Vue {
  /** Prop to display the dialog. */
  @Prop() readonly dialog: boolean

  /** Prop to provide attachment selector. */
  @Prop() readonly attach: string

  @Getter(useStore) getAmalgamateNowErrorStatus!: boolean
  @Getter(useStore) getContinuationInErrorStatus!: boolean
  @Getter(useStore) getIncorporateNowErrorStatus!: boolean

  /** The title depending on the action that was done. */
  get title (): string {
    if (this.getAmalgamateNowErrorStatus) return 'Unable to Amalgamate Now'
    if (this.getContinuationInErrorStatus) return 'Unable to Begin Continuation'
    if (this.getIncorporateNowErrorStatus) return 'Unable to Incorporate Now'
    return ''
  }

  /** The dialog text depending on the action that was done. */
  get dialogText (): string {
    if (this.getAmalgamateNowErrorStatus) return 'Unable to amalgamate now. Please cancel or try again.'
    if (this.getContinuationInErrorStatus) return 'Unable to begin continuation. Please cancel or try again.'
    if (this.getIncorporateNowErrorStatus) return 'Unable to incorporate now. Please cancel or try again.'
    return ''
  }

  /** Try again button clicked. Pass click event to parent. */
  @Emit('tryAgain')
  tryAgain () { }

  /** Close button clicked. Reload the app. */
  @Emit() close () {
    window.location.reload()
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/theme.scss";

.v-dialog {
  margin: 2rem;

  .v-card {
    padding: 0;

    .v-card__title {
      padding: 1.25rem 1.5rem;
      color: $BCgovFontColorInverted;
      background: $BCgovBlue5;
      font-size: $px-18;
      font-weight: bold;
      margin: 0;
    }

    .v-card__text {
      padding: 1.5rem !important;
      font-weight: 300;
      color: $gray7 !important;
      font-size: $px-16;
    }

    .v-card__actions {
      padding: 1rem;
    }
  }
}
</style>
