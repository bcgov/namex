<template>
  <div id="fee-summary">
    <v-row
      no-gutters
      align="center"
      justify="center"
    >
      <v-col cols="10">
        <div class="font-weight-bold header pt-10 pb-4">
          Payment Details
        </div>
        <v-alert
          v-if="fetchError"
          color="error"
          icon="mdi-alert"
          outlined
          class="my-0"
          v-html="fetchError"
        />
        <v-row
          no-gutters
          class="fee-list py-4"
        >
          <v-col v-show="!fetchError">
            <v-row
              v-for="lineItem, index in fees"
              v-show="(totalFees > 0 && lineItem.filingFees) || (totalFees === 0)"
              :key="index"
              no-gutters
            >
              <v-col>
                <v-row no-gutters>
                  <v-col cols="8">
                    <div>{{ lineItem.filingType }}</div>
                  </v-col>
                  <v-col cols="4">
                    <div
                      v-if="lineItem.filingFees > 0"
                      class="float-right"
                    >
                      ${{ lineItem.filingFees.toFixed(2) }}
                    </div>
                    <div
                      v-else
                      class="float-right"
                    >
                      No Fee
                    </div>
                  </v-col>
                </v-row>
                <v-expand-transition>
                  <v-row
                    v-if="lineItem.priorityFees"
                    no-gutters
                  >
                    <v-col cols="8">
                      <div>Priority Request fee</div>
                    </v-col>
                    <v-col cols="4">
                      <div class="float-right">
                        ${{ lineItem.priorityFees.toFixed(2) }}
                      </div>
                    </v-col>
                  </v-row>
                </v-expand-transition>
                <v-expand-transition>
                  <v-row
                    v-if="lineItem.serviceFees"
                    no-gutters
                  >
                    <v-col cols="8">
                      <div>Service fee</div>
                    </v-col>
                    <v-col cols="4">
                      <div class="float-right">
                        ${{ lineItem.serviceFees.toFixed(2) }}
                      </div>
                    </v-col>
                  </v-row>
                </v-expand-transition>
              </v-col>
            </v-row>
          </v-col>
        </v-row>

        <!--<div class="container fee-total" v-show="!fetchError">
          <div class="fee-total__name">Fees</div>
          <div class="fee-total__value">
            <v-slide-y-reverse-transition name="slide" mode="out-in">
              <div>${{totalFees.toFixed(2)}}</div>
            </v-slide-y-reverse-transition>
          </div>
        </div>

        <div class="container fee-total tax-total" v-show="!fetchError">
          <div class="fee-total__name">Tax</div>
          <div class="fee-total__value">
            <v-slide-y-reverse-transition name="slide" mode="out-in">
              <div>${{totalTax.toFixed(2)}}</div>
            </v-slide-y-reverse-transition>
          </div>
        </div> -->
        <v-row
          no-gutters
          class="pt-4 pb-10"
        >
          <v-col cols="8">
            <div
              v-show="!fetchError"
              class="payment-total"
            >
              Total Amount (CAD)
            </div>
          </v-col>
          <v-col cols="4">
            <div class="payment-total float-right">
              <v-slide-y-reverse-transition
                name="slide"
                mode="out-in"
              >
                <div><b>${{ total.toFixed(2) }}</b></div>
              </v-slide-y-reverse-transition>
            </div>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

@Component({})
export default class FeeSummary extends Vue {
  @Prop({ default: () => [] }) readonly fees!: any[]

  fetchError = ''

  get totalFees (): number {
    return this.fees instanceof Array ? this.fees.reduce((feeTotal: number, item: any) => {
      return feeTotal + item.filingFees + item.futureEffectiveFees + item.priorityFees + item.serviceFees
    }, 0) : 0
  }

  get totalTax (): number {
    return this.fees instanceof Array ? this.fees.reduce((taxTotal: number, item: any) => {
      const { gst = 0.00, pst = 0.00 } = item.tax
      return taxTotal + gst + pst
    }, 0) : 0
  }

  get total (): number {
    return this.fees instanceof Array ? this.fees.reduce((feeTotal: number, item: any) => {
      return feeTotal + item.total
    }, 0) : 0
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/theme";

#fee-summary {
  background-color: $gray1;
}

.fee-list {
  padding-left: 0 !important;
  border-bottom: 1px solid $gray4;
}

.payment-total {
  font-weight: bold;
  color: $dk-text;
}

.header {
  font-size: $px-18;
  color: $dk-text;
  border-bottom: 1px solid $gray4;
}
</style>
