<template>
  <v-expand-transition>
    <!-- check for valid receipt, as the payment may exist but not be completed -->
    <section
      v-if="summary.receipt"
      class="payment-summary"
    >
      <v-row
        class="py-5"
        no-gutters
      >
        <div class="col1 align-self-center">
          {{ receiptNumber }}
        </div>
        <div class="col2 align-self-center">
          {{ receiptDate }}
        </div>
        <div class="col3 align-self-center">
          {{ receiptDescription }}
        </div>
        <div class="col4 align-self-center">
          {{ receiptAmount }}
        </div>
        <div class="col5 align-self-center">
          <v-btn
            class="download-receipt-btn float-right"
            :loading="loading"
            @click="downloadReceipt()"
          >
            <span>Download PDF</span>
          </v-btn>
        </div>
      </v-row>
    </section>
  </v-expand-transition>
</template>

<script lang="ts">
import { Component, Mixins, Prop, Watch } from 'vue-property-decorator'
import { PaymentMixin } from '@/mixins'

@Component({})
export default class PaymentSummary extends Mixins(PaymentMixin) {
  @Prop(Object) readonly summary!: any

  /** Used to show loading state on button. */
  loading = false

  get receiptNumber (): string {
    const receiptNumber = this.summary?.receipt.receiptNumber || 'UNK'
    return `Receipt No. ${receiptNumber}`
  }

  get receiptDate (): string {
    return this.summary?.receipt.receiptDate || 'UNK'
  }

  get receiptDescription (): string {
    const lineItem = this.summary?.payment.sbcPayment.lineItems[0] // just look at first one
    return lineItem?.description
  }

  get receiptAmount (): string {
    if (this.summary?.receipt?.receiptAmount) {
      return `$${this.summary?.receipt.receiptAmount.toFixed(2)} CAD`
    }
    return null
  }

  async downloadReceipt () {
    const id = this.summary?.id
    this.loading = true
    await this.downloadReceiptPdf(id)
    this.loading = false
  }

  @Watch('summary', { immediate: true })
  onSummaryChanged () {
    this.$nextTick(() => {
      if (this.$el?.querySelector instanceof Function) {
        // add classname to button text (for more detail in breadcrumbs)
        const receiptsDownloadBtn = this.$el.querySelector && this.$el.querySelector('.download-receipt-btn > span')
        if (receiptsDownloadBtn) receiptsDownloadBtn.classList.add('receipts-download-btn')
      }
    })
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/theme";

.col1 {
  flex: 0 0 23.75%;
  max-width: 23.75%;
  font-weight: bold;
}

.col2 {
  flex: 0 0 20%;
  max-width: 20%;
}

.col3 {
  flex: 0 0 18.75%;
  max-width: 18.75%;
}

.col4 {
  flex: 0 0 16.25%;
  max-width: 16.25%;
  text-align: right;
}

.col5 {
  flex: 0 0 21.25%;
  max-width: 21.25%;
}
</style>
