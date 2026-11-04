<template>
  <MainContainer id="existing-request-edit">
    <template #container-header>
      <v-col cols="auto">
        <span
          v-if="submissionTabNumber === 1"
          class="h3 user-select-all"
        >{{ getNrNum }}</span>
        <span
          v-else
          class="font-weight-bold h4 py-0"
        >Application Details</span>
      </v-col>
    </template>

    <template #content>
      <v-tabs
        id="applicant-info-slider"
        v-model="submissionTabNumber"
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

          <v-tab-item class="pt-10">
            <NamesCapture />
          </v-tab-item>

          <v-tab-item>
            <ApplicantInfo1 />
          </v-tab-item>

          <v-tab-item>
            <ApplicantInfo2 v-if="getActingOnOwnBehalf" />
            <ApplicantInfo3 v-else />
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
import MainContainer from '@/components/new-request/main-container.vue'
import EntityCannotBeAutoAnalyzed from '@/components/new-request/submit-request/entity-cannot-be-auto-analyzed.vue'
import NamesCapture from '@/components/common/names-capture.vue'
import ApplicantInfo1 from '@/components/common/applicant-info-1.vue'
import ApplicantInfo2 from '@/components/common/applicant-info-2.vue'
import ApplicantInfo3 from '@/components/common/applicant-info-3.vue'

import { ActionBindingIF } from '@/interfaces/store-interfaces'

/**
 * This is the component for the steps when editing an existing NR.
 */
@Component({
  components: {
    MainContainer,
    EntityCannotBeAutoAnalyzed,
    NamesCapture,
    ApplicantInfo1,
    ApplicantInfo2,
    ApplicantInfo3
  }
})
export default class ExistingRequestEdit extends Vue {
  @Getter(useStore) getActingOnOwnBehalf!: boolean
  @Getter(useStore) getNrNum!: string
  @Getter(useStore) getSubmissionTabNumber!: number

  @Action(useStore) setSubmissionTabNumber!: ActionBindingIF

  get submissionTabNumber (): number {
    return this.getSubmissionTabNumber
  }

  set submissionTabNumber (value: number) {
    this.setSubmissionTabNumber(value)
  }
}
</script>
