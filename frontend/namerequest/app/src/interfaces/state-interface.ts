import { AuthorizedActions } from '@/enums'
import { NewRequestIF } from '@/interfaces/new-request-interface'
import { NameCheckModelIF, StaffPaymentIF, RefundParamsIF } from '@/interfaces'

export interface StateIF {
  common: {
    currentJsDate: Date,
    keycloakRoles: Array<string>
    authorizedActions: Array<AuthorizedActions>
  }
  newRequestModel: NewRequestIF
  staffPayment: StaffPaymentIF
  nameCheckModel: NameCheckModelIF
  refundParams: RefundParamsIF
  windowWidth: number
}
