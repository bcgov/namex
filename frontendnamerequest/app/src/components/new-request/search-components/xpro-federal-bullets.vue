<template>
  <v-col
    id="xpro-federal-bullets"
    :cols="cols"
    :md="md"
  >
    <ul class="bullet-points">
      <li>Federally incorporated businesses do not need a Name Request.</li>

      <li v-if="isAmalgamation">
        To register your extraprovincial amalgamation, download and complete
        <a :href="federalAmalgamationFormLink">
          this form <v-icon
            small
            class="ml-1"
            color="primary"
          >mdi-open-in-new</v-icon>
        </a>.
      </li>

      <li v-else-if="isRestoration && isSelectedXproAndRestorable">
        To reinstate your business, complete
        <a
          :href="fullReinstatementFormLink"
          target="_blank"
        >
          this form <v-icon
            small
            class="ml-1"
            color="primary"
          >mdi-open-in-new</v-icon>
        </a> for a full reinstatement or
        <a
          :href="limitedReinstatementFormLink"
          target="_blank"
        >
          this form  <v-icon
            small
            class="ml-1"
            color="primary"
          >mdi-open-in-new</v-icon>
        </a> for a limited reinstatement.
      </li>

      <li v-else>
        You may register your extraprovincial business immediately using its existing name
        at Corporate Online.
      </li>
    </ul>
  </v-col>
</template>

<script lang="ts">
import { Component, Mixins, Prop } from 'vue-property-decorator'
import { SearchMixin } from '@/mixins'

@Component({})
export default class XproFederalBullets extends Mixins(SearchMixin) {
  @Prop({ default: '12' }) readonly cols!: string
  @Prop({ default: null }) readonly md!: string

  readonly federalAmalgamationFormLink = 'https://www2.gov.bc.ca/assets/gov/employment-business-and-economic-' +
    'development/business-management/permits-licences-and-registration/registries-packages/' +
    'pack_34_xco_-_amalgamation_application_and_business_number_request.pdf'
  readonly fullReinstatementFormLink = 'https://www2.gov.bc.ca/assets/gov/employment-business-and-economic-' +
    'development/business-management/permits-licences-and-registration/registries-forms/' +
    'form_31_xco_-_full_reinstatement_application.pdf'
  readonly limitedReinstatementFormLink = 'https://www2.gov.bc.ca/assets/gov/employment-business-and-economic-' +
    'development/business-management/permits-licences-and-registration/registries-forms/' +
    'form_29_xco_-_limited_reinstatement_application.pdf'
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';

// l between bullet points and sizing
.bullet-points {
  line-height: 1.5rem;
  font-size: $px-15;
}
</style>
