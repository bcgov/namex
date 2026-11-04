<template>
  <v-col
    id="numbered-company-bullets"
    :cols="cols"
    :md="md"
  >
    <template v-if="isConversion && !isAlterOnline(getConversionType)">
      <div class="contact-registries">
        <p>To complete this alteration, contact us at:</p>
        <p>
          <v-icon small>
            mdi-phone
          </v-icon>&nbsp;Canada and U.S. Toll Free:
          <a href="tel:+1877-526-1526">1-877-526-1526</a>
        </p>
        <p>
          <v-icon small>
            mdi-phone
          </v-icon>&nbsp;Victoria Office:
          <a href="tel:250-387-7848">250-387-7848</a>
        </p>
        <p>
          <v-icon small>
            mdi-email
          </v-icon>&nbsp;Email:
          <a href="mailto:BCRegistries@gov.bc.ca">BCRegistries@gov.bc.ca</a>
        </p>
      </div>
    </template>

    <template v-else-if="!isXproFlow">
      <ul
        v-if="isNumberedCompanyLauncherEnabled()"
        class="bullet-points"
      >
        <li>
          Your business name will be the Incorporation Number assigned by the Registry.
          (It is not possible to request a specific number)
        </li>
        <li>You can change your business name at a later date.</li>
      </ul>
      <ul
        v-else
        class="bullet-points"
      >
        <li>Your business name will be the Incorporation Number assigned by the Registry.</li>
        <li>You can change your business name at a later date.</li>
        <li>It is not possible to request a specific Incorporation Number.</li>
      </ul>
    </template>
  </v-col>
</template>

<script lang="ts">
import { Component, Mixins, Prop } from 'vue-property-decorator'
import { SearchMixin } from '@/mixins'

@Component({})
export default class NumberedCompanyBullets extends Mixins(SearchMixin) {
  @Prop({ default: '12' }) readonly cols!: string
  @Prop({ default: null }) readonly md!: string
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';

// icon colour
.v-icon.mdi-phone,
.v-icon.mdi-email {
  color: $app-dk-blue;
}

// line spacing between bullet points and sizing
.bullet-points {
  line-height: 1.5rem;
  font-size: $px-15;
}
</style>
