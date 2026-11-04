<template>
  <!-- NB: dummy modal attach point so unit tests can see it -->
  <v-dialog
    v-model="showModal"
    width="70rem"
    attach=""
  >
    <v-card class="pa-14">
      <v-card-title class="justify-center pa-0">
        Choose the website you want to use
      </v-card-title>
      <v-btn
        id="numbered-company-help-close-btn"
        class="close-btn"
        icon
        :ripple="false"
        @click="showModal = false"
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>

      <v-card-text class="copy-normal pa-0 pt-6">
        <v-row>
          <!-- Corporate Online card (below the Registry card on small screens) -->
          <v-col
            cols="12"
            md="6"
            order="2"
            order-md="1"
          >
            <v-card
              id="corporate-online-card"
              class="option-card"
            >
              <div class="option-card-header">
                <div class="option-card-title">
                  Corporate Online
                </div>
                <div class="option-card-subtitle">
                  For complex filings.
                </div>
              </div>

              <v-divider />

              <div class="option-card-body">
                <p>Choose this if you need to do any of the following in the next 6 months:</p>
                <ul>
                  <li>combine or merge your business with another business (Amalgamation)</li>
                  <li>reactivate a business (Restoration)</li>
                </ul>
                <p class="font-weight-bold">
                  Note: all businesses in Corporate Online will be moved to the new BC Business Registry soon
                </p>
                <v-btn
                  id="help-corporate-online-btn"
                  class="button-blue mt-auto"
                  :href="colinLink"
                  target="_blank"
                >
                  Continue to Corporate Online
                  <v-icon
                    right
                    small
                  >
                    mdi-open-in-new
                  </v-icon>
                </v-btn>
              </div>
            </v-card>
          </v-col>

          <!-- BC Business Registry card (above the Corporate Online card on small screens) -->
          <v-col
            cols="12"
            md="6"
            order="1"
            order-md="2"
          >
            <v-card
              id="business-registry-card"
              class="option-card"
            >
              <div class="option-card-header option-card-header-dark d-flex justify-space-between align-center">
                <div>
                  <div class="option-card-title">
                    BC Business Registry
                  </div>
                  <div class="option-card-subtitle">
                    For everyday filings.
                  </div>
                </div>
                <div class="gold-badge">
                  Most common for business owners
                </div>
              </div>

              <v-divider />

              <div class="option-card-body">
                <p>
                  Choose this <strong>if you won’t need to change your business information in the
                    next 6 months</strong>, or you will only need to do the following:
                </p>
                <ul>
                  <li>file annual reports</li>
                  <li>change your business address when you move</li>
                  <li>change directors names or addresses</li>
                  <li>change basic business information (Alteration)</li>
                </ul>
                <v-btn
                  id="help-business-registry-btn"
                  class="mt-auto"
                  :disabled="!isSupportedIncorporationRegistration(getEntityTypeCd)"
                  @click="registryClicked()"
                >
                  Use the New BC Business Registry
                </v-btn>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Mixins } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { NrAffiliationMixin } from '@/mixins'

@Component({})
export default class NumberedCompanyHelpDialog extends Mixins(NrAffiliationMixin) {
  @Getter(useStore) getNumberedCompanyHelpModalVisible!: boolean
  @Action(useStore) setNumberedCompanyHelpModalVisible!: ActionBindingIF

  readonly colinLink = sessionStorage.getItem('CORPORATE_ONLINE_URL')

  get showModal () {
    return this.getNumberedCompanyHelpModalVisible
  }
  set showModal (value: boolean) {
    this.setNumberedCompanyHelpModalVisible(value)
  }

  /** Same action as the "Incorporate using the New BC Business Registry" launcher button. */
  async registryClicked (): Promise<void> {
    this.showModal = false
    await this.actionNowClicked()
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';

#numbered-company-help-close-btn {
  box-shadow: none !important;
  background-color: transparent !important;

  .v-icon {
    color: $dk-text;
  }
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
}

.option-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 -2px 6px rgba(0, 0, 0, 0.12), 0 3px 6px rgba(0, 0, 0, 0.2) !important;
  padding: 0 !important;
}

.option-card-header {
  padding: 1rem 1.5rem;

  .option-card-title {
    color: $dk-text;
    font-size: $px-18;
    font-weight: bold;
    white-space: nowrap;
  }

  .option-card-subtitle {
    color: $text;
    font-size: $px-14;
  }
}

.option-card-header-dark {
  background-color: $BCgovBlue5;

  .option-card-title,
  .option-card-subtitle {
    color: white;
  }
}

.gold-badge {
  background-color: $BCgovGold5;
  border-radius: 4px;
  color: black;
  font-size: $px-14;
  font-weight: bold;
  line-height: 1.125rem;
  padding: 0.25rem 0.5rem;
  margin-left: 1rem;
  max-width: 10rem;
  text-align: center;
}

.option-card-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  color: $text;

  strong,
  .font-weight-bold {
    color: $text;
  }

  ul {
    margin-bottom: 1rem;
  }

  .v-btn {
    align-self: center;
  }
}
</style>
