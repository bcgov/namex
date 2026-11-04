<template>
  <div>
    <v-alert
      v-if="fetchError"
      color="error"
      icon="mdi-alert"
      outlined
      class="my-0"
      v-html="fetchError"
    />

    <ul
      v-show="!fetchError"
      class="fee-list pl-0 mb-n1"
    >
      <li>
        <div class="font-weight-bold nr-num">
          Your Name Request Number is {{ nrNum }}
        </div>
      </li>
      <li>
        Use this number to check the status of your Name Request
      </li>
    </ul>

    <RequestDetails
      class="mt-4"
      :applicant="applicant"
      :nameChoices="nameChoices"
      :name="name"
    />

    <v-container>
      <v-row
        v-show="!fetchError"
        align="center"
        justify="center"
        class="receipt-summary"
      >
        <v-col cols="10">
          <div class="font-weight-bold pb-3 header">
            Receipt No. {{ receipt.receiptNumber }}
          </div>

          <ul class="fee-list pt-3 px-0">
            <li
              v-if="receipt"
              class="container fee-list__item px-0"
            >
              <div class="fee-list__item-name">
                Payment Date
              </div>
              <div class="fee-list__item-value">
                {{ receipt.receiptDate }}
              </div>
            </li>
            <li
              v-if="receipt"
              class="container fee-list__item px-0"
            >
              <div class="fee-list__item-name">
                Amount
              </div>
              <div class="fee-list__item-value">
                ${{ receipt.receiptAmount.toFixed(2) }} CAD
              </div>
            </li>
            <li
              v-if="summary"
              class="container fee-list__item px-0"
            >
              <div class="fee-list__item-name">
                Status
              </div>
              <div class="fee-list__item-value">
                {{ summary.statusCode }}
              </div>
            </li>
          </ul>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import RequestDetails from '@/components/common/request-details.vue'
import { ApplicantI, NameChoicesIF } from '@/interfaces'
import { Getter } from 'pinia-class'
import { useStore } from '@/store'

@Component({
  components: {
    RequestDetails
  }
})
export default class PaymentConfirm extends Vue {
  @Prop(String) readonly nrNum!: string
  @Prop(Object) readonly summary!: any
  @Prop(Object) readonly receipt!: any
  @Prop(Object) readonly applicant!: ApplicantI
  @Prop(Object) readonly nameChoices!: {
    type: any[]
    required: false
  }
  @Prop(String) readonly name!: string

  @Getter(useStore) getNameChoices!: NameChoicesIF

  fetchError = ''
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/theme";

.receipt-summary {
  background-color: $gray1;
}

.filing_receipt-list {
  border-bottom: 1px solid $gray3;
}

.filing_receipt-list__item {
  &-name, &-value {
    font-weight: bold;
  }

  &-name {
    flex: 1 1 auto;
    margin-right: 2rem;
  }

  &-value {
    flex: 0 0 auto;
    text-align: right;
  }
}

.filing_receipt-list__item + .filing_receipt-list__item {
  border-top: 1px solid $gray3;
}

.filing_receipt-total {
  align-items: center;
  letter-spacing: -0.01rem;
  line-height: auto;

  &__name {
    flex: 1 1 auto;
    margin-right: auto;
    font-weight: bold;
  }

  &__currency {
    margin-right: 0.5rem;
    color: $gray5;
    font-weight: normal;
  }

  &__value {
    font-size: 1.65rem;
    font-weight: bold;
  }
}

.fee-total {
  font-weight: bold;
}

.fee-list__item {
  display: flex;
  flex-flow: row nowrap;
  line-height: 0;
  justify-content: space-between;
  font-size: $px-16;
}

.header {
  font-size: $px-18;
  color: $dk-text;
  border-bottom: 1px solid $gray4;
}

.nr-num {
  color: $gray9;
}
</style>
