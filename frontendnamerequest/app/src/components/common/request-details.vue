<template>
  <div id="request-details">
    <section>
      <h4>Requested Name <span v-if="nameChoices.name2">Choices</span></h4>
      <ul class="pl-0">
        <li v-if="!nameChoices.name2">
          {{ nameChoices.name1 }} {{ nameChoices.designation1 }}
        </li>
        <template v-else>
          <li v-if="nameChoices.name1">
            1. {{ nameChoices.name1 }} {{ nameChoices.designation1 }}
          </li>
          <li v-if="nameChoices.name2">
            2. {{ nameChoices.name2 }} {{ nameChoices.designation2 }}
          </li>
          <li v-if="nameChoices.name3">
            3. {{ nameChoices.name3 }} {{ nameChoices.designation3 }}
          </li>
        </template>
      </ul>
    </section>

    <v-row>
      <v-col cols="6">
        <h4>Applicant Information</h4>
        <ul class="pl-0">
          <!-- If there's no contact person (agent / lawyer / etc.) the applicant is the contact -->
          <li>{{ `${applicantName}` }}</li>
          <li>
            {{ `${applicant.addrLine1 || ''} ${applicant.addrLine2 || ''}` }}
          </li>
          <li>
            {{ `${applicant.city || ''}, ${applicant.stateProvinceCd || ''}` }}
          </li>
          <li>
            {{ `${applicant.countryTypeCd === Location.CA ? 'Canada' : applicant.countryTypeCd},
             ${applicant.postalCd || ''}` }}
          </li>
        </ul>
      </v-col>

      <v-col cols="6">
        <ul class="pl-0">
          <li v-if="client">
            <h4>Client Name</h4>
            <ul class="pl-0">
              <li>{{ `${client}` }}</li>
            </ul>
          </li>
          <li v-if="contactPerson">
            <h4>Primary Contact</h4>
            <ul class="pl-0">
              <li>{{ `${contactPerson}` }}</li>
              <li>{{ applicant.emailAddress }}</li>
              <li>{{ applicant.phoneNumber }}</li>
              <li>
                <span
                  v-if="getFolioNumber"
                  class="title-bold-16"
                >Folio: </span>{{ getFolioNumber }}
              </li>
            </ul>
          </li>
          <li v-if="!contactPerson">
            <h4>Primary Contact</h4>
            <ul class="pl-0">
              <!-- If there's no contact person (agent / lawyer / etc.) the applicant is the contact -->
              <li>{{ `${applicantName}` }}</li>
              <li>{{ applicant.emailAddress }}</li>
              <li>{{ applicant.phoneNumber }}</li>
              <li>
                <span
                  v-if="getFolioNumber"
                  class="title-bold-16"
                >Folio: </span>{{ getFolioNumber }}
              </li>
            </ul>
          </li>
        </ul>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { ApplicantI, NameChoicesIF } from '@/interfaces'
import { Component, Prop, Vue } from 'vue-property-decorator'
import { Getter } from 'pinia-class'
import { useStore } from '@/store'
import { Location } from '@/enums'

@Component({})
export default class RequestDetails extends Vue {
  // enum for template
  readonly Location = Location

  @Prop(Object)
  readonly applicant: ApplicantI

  @Prop(Object)
  readonly nameChoices: NameChoicesIF

  @Getter(useStore) getNameChoices!: NameChoicesIF
  @Getter(useStore) getFolioNumber!: string
  @Getter(useStore) getEditMode!: boolean

  get applicantName (): string {
    const applicant = this.applicant
    if (!applicant) return ''
    return [applicant.firstName, applicant.middleName, applicant.lastName]
      .filter(str => !!str).join(' ')
  }

  get contactPerson () {
    const { applicant = { contact: '' } } = this
    return (applicant.contact) ? `${applicant.contact}` : undefined
  }

  get client () {
    const { applicant = { clientFirstName: '', clientLastName: '' } } = this
    return (applicant.clientFirstName || applicant.clientLastName)
      ? `${applicant.clientFirstName} ${applicant.clientLastName}`
      : undefined
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/theme";
@import "@/assets/styles/base";

h4 {
  @extend .title-bold-16
}

ul {
  list-style: none;
}
</style>
