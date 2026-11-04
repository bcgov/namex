<template>
  <MainContainer id="submission-tabs">
    <template #container-header>
      <v-col
        cols="8"
        class="font-weight-bold h5 py-0"
      >
        {{ submissionModeHeader }}
      </v-col>
    </template>

    <template #content>
      <v-tabs
        id="applicant-info-slider"
        v-model="submissionTabNumber"
        class="mt-2"
      >
        <v-tabs-items
          v-model="submissionTabNumber"
          touchless
        >
          <v-tab-item>
            <keep-alive>
              <EntityCannotBeAutoAnalyzed />
            </keep-alive>
          </v-tab-item>

          <v-tab-item>
            <NamesCapture />
          </v-tab-item>

          <v-tab-item>
            <ApplicantInfo1 />
          </v-tab-item>

          <v-tab-item>
            <ApplicantInfo2 v-if="getActingOnOwnBehalf" />
            <ApplicantInfo3 v-else />
          </v-tab-item>

          <v-tab-item>
            <InvalidActionMessage />
          </v-tab-item>

          <v-tab-item>
            <Timeout />
          </v-tab-item>
        </v-tabs-items>
      </v-tabs>
    </template>
  </MainContainer>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import MainContainer from '../main-container.vue'
import EntityCannotBeAutoAnalyzed from './entity-cannot-be-auto-analyzed.vue'
import NamesCapture from '../../common/names-capture.vue'
import ApplicantInfo1 from '../../common/applicant-info-1.vue'
import ApplicantInfo2 from '../../common/applicant-info-2.vue'
import ApplicantInfo3 from '../../common/applicant-info-3.vue'
import InvalidActionMessage from '../../existing-request/invalid-action-message.vue'
import Timeout from './timeout.vue'
import { ActionBindingIF } from '@/interfaces/store-interfaces'

/**
 * This is the component for the steps when creating a new NR.
 */
@Component({
  components: {
    MainContainer,
    EntityCannotBeAutoAnalyzed,
    NamesCapture,
    ApplicantInfo1,
    ApplicantInfo2,
    ApplicantInfo3,
    InvalidActionMessage,
    Timeout
  }
})
export default class SubmissionTabs extends Vue {
  @Getter(useStore) getActingOnOwnBehalf!: boolean
  @Getter(useStore) getEditMode!: boolean
  @Getter(useStore) getSubmissionTabNumber!: number

  @Action(useStore) setSubmissionTabNumber!: ActionBindingIF

  private mounted (): void {
    let link = document.createElement('link')
    link.setAttribute('href', 'https://cdnjs.cloudflare.com/ajax/libs/open-iconic/1.1.1/font/css/open-iconic.min.css')
    link.setAttribute('rel', 'stylesheet')
    document.head.appendChild(link)
  }

  get submissionModeHeader (): string {
    // safety check
    if (this.getEditMode) return ''

    if (this.submissionTabNumber === 1) {
      return 'Submit a Name Request for Review'
    } else {
      return 'Submission Details'
    }
  }

  get submissionTabNumber (): number {
    return this.getSubmissionTabNumber
  }

  set submissionTabNumber (value: number) {
    this.setSubmissionTabNumber(value)
  }
}
</script>
