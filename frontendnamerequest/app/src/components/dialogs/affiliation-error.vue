<template>
  <v-dialog
    id="affiliation-error-dialog"
    :value="isShowModal"
    max-width="45rem"
    persistent
  >
    <v-card>
      <v-card-title class="d-flex justify-space-between">
        <div v-if="isUnableToStartRegistration">
          Unable to start registration
        </div>
        <div v-if="isAssociatedOtherAccount">
          Name Request associated with another account
        </div>
        <div class="mt-3">
          <v-btn
            icon
            large
            class="dialog-close"
            @click="hideModal()"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
      </v-card-title>

      <v-card-text class="copy-normal pt-8">
        <p
          v-if="isUnableToStartRegistration"
          class="mb-0"
        >
          We encountered an error starting your registration. Try again later, or go to
          <a
            :href="businessRegistryUrl"
            target="_blank"
          >My Business Registry</a> and manually
          add this Name Request to your list to register this business name.
        </p>
        <p
          v-if="isAssociatedOtherAccount"
          class="mb-0"
        >
          This Name Request has already been linked to a different BC Registries account. It
          must be removed from that account before it can be used.
        </p>
        <br>
        <p class="mb-0">
          If you require assistance, please contact us.
        </p>
        <br>
        <ContactInfo direction="col" />
      </v-card-text>

      <v-card-actions class="justify-center pt-8">
        <v-btn
          text
          class="px-12"
          @click="hideModal()"
        >
          OK
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
import { NrAffiliationErrors } from '@/enums'
import ContactInfo from '@/components/common/contact-info.vue'

@Component({
  components: { ContactInfo }
})
export default class AffiliationErrorDialog extends Vue {
  @Getter(useStore) getAffiliationErrorModalValue!: number
  @Action(useStore) setAffiliationErrorModalValue!: ActionBindingIF

  get isShowModal (): boolean {
    return (this.getAffiliationErrorModalValue !== NrAffiliationErrors.NONE)
  }

  get isUnableToStartRegistration (): boolean {
    return (this.getAffiliationErrorModalValue === NrAffiliationErrors.UNABLE_TO_START_REGISTRATION)
  }

  get isAssociatedOtherAccount (): boolean {
    return (this.getAffiliationErrorModalValue === NrAffiliationErrors.ASSOCIATED_OTHER_ACCOUNT)
  }

  get businessRegistryUrl (): string {
    const businessesUrl = sessionStorage.getItem('BUSINESS_REGISTRY_URL')
    // NB: fall back is user's default account
    const accountId = JSON.parse(sessionStorage.getItem('CURRENT_ACCOUNT')).id || 0
    return `${businessesUrl}account/${accountId}`
  }

  protected hideModal (): void {
    this.setAffiliationErrorModalValue(NrAffiliationErrors.NONE)
  }
}
</script>
