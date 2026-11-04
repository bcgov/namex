<template>
  <v-col
    cols="12"
    md="5"
    lg="5"
    class="py-0"
    :class="isMobile ? 'mt-6 text-center' : 'text-right'"
  >
    <v-btn
      v-if="showBack"
      id="submit-back-btn"
      x-large
      :class="isMobile ? 'mobile-btn' : 'mr-3'"
      @click="back()"
    >
      {{ backText }}
    </v-btn>
    <v-btn
      x-large
      :class="{ 'mobile-btn' : isMobile }"
      :loading="getIsLoadingSubmission"
      class="submit-continue-btn"
      @click="nextAction()"
    >
      {{ nextText }}
    </v-btn>
  </v-col>
</template>

<script lang="ts">
import { Component, Emit, Vue } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import { SubmissionTypeT } from '@/interfaces'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { NrState } from '@/enums'

@Component({})
export default class ApplicantInfoNav extends Vue {
  @Getter(useStore) getEditMode!: boolean
  @Getter(useStore) getIsLoadingSubmission!: boolean
  @Getter(useStore) getNrState!: NrState
  @Getter(useStore) getSubmissionTabNumber!: number
  @Getter(useStore) getSubmissionType!: SubmissionTypeT
  @Getter(useStore) isMobile!: boolean

  @Action(useStore) setSubmissionTabNumber!: ActionBindingIF

  get backText () {
    if (this.getEditMode) {
      return 'Previous'
    }
    return 'Back'
  }

  get nextText () {
    if (this.getSubmissionTabNumber === 3) {
      if (this.getEditMode) {
        return 'Submit Changes'
      }
      return 'Review and Confirm'
    }
    if (this.getEditMode) {
      return 'Next'
    }
    return 'Continue'
  }

  get showBack (): boolean {
    if (this.getSubmissionTabNumber < 2) {
      return false
    }
    if (this.getSubmissionTabNumber === 2) {
      return (this.getSubmissionType === 'examination' || this.getNrState === NrState.DRAFT)
    }
    if (this.getSubmissionTabNumber === 3) {
      return true
    }
    return false
  }

  back () {
    this.setSubmissionTabNumber(this.getSubmissionTabNumber - 1)
  }

  @Emit('nextAction')
  nextAction () : void {}
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/theme";

.submit-back-btn {
  background-color: white !important;
  color: $app-blue !important;
  border: 1px solid $app-blue !important;
  box-shadow: none !important;
  text-transform: none !important;
}

.submit-continue-btn {
  @media only screen and (max-width: 600px) {
    width: 100%;
  }
}

.mobile-btn {
  width: 16.5rem !important;
  margin: .5rem 0;
}
</style>
