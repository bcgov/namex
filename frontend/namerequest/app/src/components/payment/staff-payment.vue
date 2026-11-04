<template>
  <div
    id="staff-payment"
    :class="{'invalid-section': showStaffPaymentInvalidSection}"
  >
    <StaffPaymentShared
      :staffPaymentData="getStaffPayment"
      :validate="validate"
      :displaySideLabel="false"
      :displayPriorityCheckbox="false"
      @update:staffPaymentData="onStaffPaymentDataUpdate($event)"
      @valid="onStaffPaymentValidity($event)"
    />
  </div>
</template>

<script lang="ts">
import { Component, Emit, Vue } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'

// Components
import { StaffPayment as StaffPaymentShared } from '@bcrs-shared-components/staff-payment'

// Interfaces and Enums
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { StaffPaymentIF } from '@/interfaces'
import { StaffPaymentOptions } from '@/enums'

@Component({
  components: {
    StaffPaymentShared
  }
})
export default class StaffPayment extends Vue {
  @Getter(useStore) getStaffPayment!: StaffPaymentIF
  @Action(useStore) setStaffPayment!: ActionBindingIF

  /** Whether to validate the data. */
  validate = false

  /** Whether to show the staff payment invalid section styling. */
  get showStaffPaymentInvalidSection (): boolean {
    const option = this.getStaffPayment.option ?? StaffPaymentOptions.NONE
    // True if no option is selected
    return this.validate && (option === StaffPaymentOptions.NONE)
  }

  /** Called externally to set validation state. */
  public setValidation (val: boolean) {
    this.validate = val
  }

  /** Called when component's staff payment data has been updated. */
  onStaffPaymentDataUpdate (val: StaffPaymentIF) {
    let staffPaymentData: StaffPaymentIF = { ...this.getStaffPayment, ...val }

    // disable validation
    this.validate = false

    switch (staffPaymentData.option) {
      case StaffPaymentOptions.FAS:
        staffPaymentData = {
          option: StaffPaymentOptions.FAS,
          routingSlipNumber: staffPaymentData.routingSlipNumber,
          isPriority: staffPaymentData.isPriority,
          bcolAccountNumber: '',
          datNumber: '',
          folioNumber: ''
        }
        break

      case StaffPaymentOptions.BCOL:
        staffPaymentData = {
          option: StaffPaymentOptions.BCOL,
          bcolAccountNumber: staffPaymentData.bcolAccountNumber,
          datNumber: staffPaymentData.datNumber,
          folioNumber: staffPaymentData.folioNumber,
          isPriority: staffPaymentData.isPriority,
          routingSlipNumber: ''
        }
        break

      case StaffPaymentOptions.NO_FEE:
        staffPaymentData = {
          option: StaffPaymentOptions.NO_FEE,
          routingSlipNumber: '',
          isPriority: false,
          bcolAccountNumber: '',
          datNumber: '',
          folioNumber: ''
        }
        break

      case StaffPaymentOptions.NONE: // should never happen
        break
    }

    this.setStaffPayment(staffPaymentData)
  }

  /** Called when component's validity has changed. */
  @Emit('isValid')
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  onStaffPaymentValidity (val: boolean): void {}
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/theme";

// error border
.invalid-section {
  border-left: 3px solid $app-red !important;
}

// override internal whitespace
::v-deep #staff-payment-container {
  padding: 0 !important;
  margin: 0 !important;
}

// override default radio input background colour
::v-deep .v-input--radio-group__input {
  background-color: white;
}

// remove margin below radio group
::v-deep .v-input--radio-group > .v-input__control > .v-input__slot {
  margin-bottom: 0 !important;
}

// hide messages below radio group
::v-deep .v-input--radio-group > .v-input__control > .v-messages {
  display: none;
}
</style>
