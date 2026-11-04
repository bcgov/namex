import { Component, Mixins } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import AuthServices from '@/services/auth-services'
import BusinessServices from '@/services/business-services'
import { BusinessRequest, NameRequestI } from '@/interfaces'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { getBusinessHomeLoginUrl, Navigate } from '@/plugins'
import { CommonMixin } from '@/mixins'
import { EntityTypes, NrAffiliationErrors } from '@/enums'
import { CREATED, BAD_REQUEST } from 'http-status-codes'
import { CorpTypeCd } from '@bcrs-shared-components/corp-type-module'
import { AmalgamationTypes, CorrectNameOptions, FilingTypes, NrRequestActionCodes }
  from '@bcrs-shared-components/enums'

@Component({})
export class NrAffiliationMixin extends Mixins(CommonMixin) {
  @Getter(useStore) isAmalgamation!: boolean
  @Getter(useStore) isContinuationIn!: boolean
  @Getter(useStore) isNewBusiness!: boolean
  @Getter(useStore) getBusinessAccountId: string
  @Getter(useStore) getEntityTypeCd!: EntityTypes
  @Getter(useStore) getRequestActionCd!: NrRequestActionCodes
  @Getter(useStore) isAuthenticated!: boolean
  @Getter(useStore) isChangeName!: boolean
  @Getter(useStore) isConversion!: boolean
  @Getter(useStore) isRestoration!: boolean
  @Getter(useStore) isRoleStaff!: boolean

  @Action(useStore) setAffiliationErrorModalValue!: ActionBindingIF
  @Action(useStore) setAmalgamateNowErrorStatus!: ActionBindingIF
  @Action(useStore) setContinuationInErrorStatus!: ActionBindingIF
  @Action(useStore) setIncorporateNowErrorStatus!: ActionBindingIF

  /**
   * Affiliates a NR to the current account, creates a temporary business, and then navigates
   * to the entity dashboard page.
   * @param nr The NR to affiliate.
   */
  async createAffiliation (nr: NameRequestI): Promise<any> {
    try {
      // show spinner since the network calls below can take a few seconds
      this.$root.$emit('showSpinner', true)

      // NB: fall back is user's default account
      const accountId = +JSON.parse(sessionStorage.getItem('CURRENT_ACCOUNT'))?.id || 0

      // try to affiliate the NR
      const createAffiliationResponse = await AuthServices.createNrAffiliation(accountId, nr)
      if (!createAffiliationResponse || !createAffiliationResponse.status) {
        this.setAffiliationErrorModalValue(NrAffiliationErrors.UNABLE_TO_START_REGISTRATION)
        throw Error('Unable to find existing affiliation')
      }

      // check if affiliation succeeded
      if (createAffiliationResponse.status === CREATED) {
        // create the business
        const businessId = await this.createBusiness(accountId, nr, true)
          .catch(error => {
            this.setAffiliationErrorModalValue(NrAffiliationErrors.UNABLE_TO_START_REGISTRATION)
            throw error
          })

        // go to entity dashboard
        this.goToEntityDashboard(businessId)
        return
      }

      // check if NR is already affiliated
      if (
        createAffiliationResponse.status === BAD_REQUEST &&
        createAffiliationResponse.data?.code === 'NR_CONSUMED'
      ) {
        // fetch existing affiliations
        const fetchAffiliationsResponse = await AuthServices.fetchAffiliations(accountId)
          .catch(error => {
            this.setAffiliationErrorModalValue(NrAffiliationErrors.UNABLE_TO_START_REGISTRATION)
            throw error
          })

        const entities = fetchAffiliationsResponse?.entities || []

        // is this a name request affiliation?
        const nameRequestEntity = entities.find(entity => entity.businessIdentifier === nr.nrNum)
        if (nameRequestEntity) {
          // create the business
          const businessId = await this.createBusiness(accountId, nr, false)
            .catch(error => {
              this.setAffiliationErrorModalValue(NrAffiliationErrors.UNABLE_TO_START_REGISTRATION)
              throw error
            })

          // go to entity dashboard
          this.goToEntityDashboard(businessId)
          return
        }

        // is this a temporary business affiliation?
        const temporaryBusinessEntity = entities.find(entity => entity.nrNumber === nr.nrNum)
        if (temporaryBusinessEntity) {
          // use existing business id
          const businessId = temporaryBusinessEntity.businessIdentifier

          if (!businessId) {
            this.setAffiliationErrorModalValue(NrAffiliationErrors.UNABLE_TO_START_REGISTRATION)
            throw Error('Invalid existing affiliation business identifier')
          }

          // go to entity dashboard
          this.goToEntityDashboard(businessId)
          return
        }

        this.setAffiliationErrorModalValue(NrAffiliationErrors.ASSOCIATED_OTHER_ACCOUNT)
        throw Error('Unable to find existing affiliation')
      }

      this.setAffiliationErrorModalValue(NrAffiliationErrors.UNABLE_TO_START_REGISTRATION)
      throw Error('Unable to create new affiliation')
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error('createAffiliation() =', err)

      // hide spinner
      this.$root.$emit('showSpinner', false)
    }
  }

  /**
   * Creates temporary business record and returns business identifier.
   * Throws on error.
   */
  private async createBusiness (
    accountId: number, nr: NameRequestI, isNewAffiliation: boolean
  ): Promise<string> {
    const createBusinessResponse =
      await BusinessServices.createBusiness(this.getBusinessRequest(accountId, nr)).catch(() => null)

    if (createBusinessResponse?.status !== CREATED) {
      // create failed -- delete new affiliation to avoid orphan records
      if (isNewAffiliation) {
        await AuthServices.removeNrAffiliation(accountId, nr.nrNum).catch(() => null)
      }

      throw Error('Unable to create new business')
    }

    return createBusinessResponse.data?.filing?.business?.identifier as string
  }

  /** Returns business request object. */
  private getBusinessRequest (accountId: number, nr: NameRequestI): BusinessRequest {
    let name = ''
    let legalType = ''
    let businessRequest = {} as BusinessRequest
    const nrNumber = nr.nrNum
    if (!this.isFirm(nr)) {
      if (nr.request_action_cd === NrRequestActionCodes.AMALGAMATE) {
        name = FilingTypes.AMALGAMATION_APPLICATION
        legalType = nr.legalType
        businessRequest = {
          filing: {
            business: { legalType },
            header: { accountId, name },
            amalgamationApplication: {
              type: AmalgamationTypes.REGULAR,
              nameRequest: { legalType, nrNumber }
            }
          }
        }
      } else if (nr.request_action_cd === NrRequestActionCodes.MOVE) {
        name = FilingTypes.CONTINUATION_IN
        legalType = nr.legalType
        businessRequest = {
          filing: {
            business: { legalType },
            header: { accountId, name },
            continuationIn: {
              nameRequest: { legalType, nrNumber }
            }
          }
        }
      } else {
        name = FilingTypes.INCORPORATION_APPLICATION
        legalType = this.entityTypeToCorpType(nr.entity_type_cd)
        businessRequest = {
          filing: {
            business: { legalType },
            header: { accountId, name },
            incorporationApplication: {
              nameRequest: { legalType, nrNumber }
            }
          }
        }
      }
    }

    if (this.isFirm(nr)) {
      name = FilingTypes.REGISTRATION
      legalType = nr.legalType
      businessRequest = {
        filing: {
          business: { legalType },
          header: { accountId, name },
          registration: {
            business: { natureOfBusiness: nr.natureOfBusiness },
            nameRequest: { legalType, nrNumber }
          }
        }
      }
    }

    return businessRequest
  }

  /** Navigates to entity dashboard (BUSINESS_DASHBOARD UI). */
  goToEntityDashboard (businessId: string): void {
    if (businessId) {
      const businessDashUrl = sessionStorage.getItem('BUSINESS_DASH_URL')
      Navigate(`${businessDashUrl}${businessId}`)
    }
  }

  /**
   * If user is authenticated, create draft business and redirect to Dashboard.
   * If restoration/reinstatement selected, go to business dashboard.
   * If user is not authenticated, redirect to login screen then redirect back.
   */
  async actionNowClicked (): Promise<void> {
    const legalType = this.entityTypeToCorpType(this.getEntityTypeCd)
    if (this.isAuthenticated) {
      if (this.isConversion || this.isRestoration || this.isChangeName) {
        this.goToEntityDashboard(this.getSearchBusiness.identifier)
      } else {
        await this.actionNumberedEntity(legalType)
      }
    } else {
      // persist legal type and request type of the action in session, replayed in App.vue after authentication
      sessionStorage.setItem('LEGAL_TYPE', legalType)
      sessionStorage.setItem('REQUEST_ACTION_CD', this.getRequestActionCd)
      // navigate to Business Home login page, returning to the current page after login
      Navigate(getBusinessHomeLoginUrl())
    }
  }

  /**
   * 1. Handles the action buttons (numbered selection).
   * 2. Creates draft business depending on legal type.
   * 3. Redirects to entity dashboard.
   * @param legalType The legal type of the business.
   */
  async actionNumberedEntity (legalType: CorpTypeCd): Promise<any> {
    // show spinner since this is a network call
    this.$root.$emit('showSpinner', true)
    let businessAccountId: number

    if (this.getBusinessAccountId && this.isRoleStaff) {
      businessAccountId = Number(this.getBusinessAccountId)
    } else {
      const storedAccount = sessionStorage.getItem('CURRENT_ACCOUNT')
      businessAccountId = storedAccount ? +JSON.parse(storedAccount)?.id || 0 : 0
    }

    try {
      const businessId = await this.createNumberedBusiness(businessAccountId, legalType)
      this.goToEntityDashboard(businessId)
      return
    } catch (error) {
      this.$root.$emit('showSpinner', false)
      if (this.isAmalgamation) {
        this.setAmalgamateNowErrorStatus(true)
        throw new Error('Unable to Amalgamate Now = ' + error)
      } else if (this.isContinuationIn) {
        this.setContinuationInErrorStatus(true)
        throw new Error('Unable to Begin Continuation = ' + error)
      } else if (this.isNewBusiness) {
        this.setIncorporateNowErrorStatus(true)
        throw new Error('Unable to Incorporate Now = ' + error)
      }
      throw new Error('Error in actionNumberedEntity() = ' + error)
    }
  }

  /**
   * Creates a draft numbered business based on specified legal type.
   * @param accountId Account ID of logged in user.
   * @param legalType The legal type of the business that's being created.
   */
  async createNumberedBusiness (accountId: number, legalType: CorpTypeCd): Promise<string> {
    if (this.isContinuationIn) {
      // convert regular legal type to continuation in legal type
      switch (legalType) {
        case CorpTypeCd.BC_COMPANY: legalType = CorpTypeCd.CONTINUE_IN; break
        case CorpTypeCd.BENEFIT_COMPANY: legalType = CorpTypeCd.BEN_CONTINUE_IN; break
        case CorpTypeCd.BC_CCC: legalType = CorpTypeCd.CCC_CONTINUE_IN; break
        case CorpTypeCd.BC_ULC_COMPANY: legalType = CorpTypeCd.ULC_CONTINUE_IN; break
        case CorpTypeCd.SOCIETY: legalType = CorpTypeCd.CONT_IN_SOCIETY; break
      }
    }

    const businessRequest = {
      filing: {
        header: { accountId },
        business: { legalType }
      }
    } as BusinessRequest

    if (this.isAmalgamation) {
      businessRequest.filing.header.name = FilingTypes.AMALGAMATION_APPLICATION
      businessRequest.filing.amalgamationApplication = {
        nameRequest: { legalType, correctNameOption: CorrectNameOptions.CORRECT_AML_NUMBERED },
        type: AmalgamationTypes.REGULAR
      }
    } else if (this.isContinuationIn) {
      businessRequest.filing.header.name = FilingTypes.CONTINUATION_IN
      businessRequest.filing.continuationIn = { nameRequest: { legalType } }
    } else if (this.isNewBusiness) {
      businessRequest.filing.header.name = FilingTypes.INCORPORATION_APPLICATION
      businessRequest.filing.incorporationApplication = { nameRequest: { legalType } }
    } else {
      throw new Error('Invalid Request Type')
    }

    const createBusinessResponse = await BusinessServices.createBusiness(businessRequest)

    return createBusinessResponse.data?.filing?.business?.identifier as string
  }
}
