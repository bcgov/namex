import { Component, Vue } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import NamexServices from '@/services/namex-services'
import { NrState } from '@/enums'

@Component({})
export class DisplayedComponentMixin extends Vue {
  @Getter(useStore) getDisplayedComponent!: string
  @Getter(useStore) getNrId!: number
  @Getter(useStore) getNrState!: NrState

  @Action(useStore) cancelAnalyzeName!: ActionBindingIF
  @Action(useStore) cancelEditExistingRequest!: ActionBindingIF
  @Action(useStore) setDisplayedComponent!: ActionBindingIF
  @Action(useStore) setSubmissionTabComponent!: ActionBindingIF
  @Action(useStore) setEditMode!: ActionBindingIF

  componentName = ''

  get displayedComponent () {
    // We can't watch a computed property directly, and we don't want to inject displayedComponent as a prop
    // so we're using an intermediate data property, which we CAN watch - set its value here
    const componentName = this.getDisplayedComponent
    if (this.componentName !== componentName) {
      // Update the active component name
      this.componentName = componentName
    }
    return componentName
  }

  get isIncompletePayment (): boolean {
    return (this.getNrState === NrState.PENDING_PAYMENT)
  }

  async cancelAndResetState () {
    const componentName = this.getDisplayedComponent
    this.setSubmissionTabComponent(0)
    // Are we cancelling a new NR?
    if (['SubmissionTabs'].indexOf(componentName) > -1) {
      await this.cancelAnalyzeName('Tabs')
      this.redirectToStart()
    } else if (['ExistingRequestDisplay'].indexOf(componentName) > -1) {
      await this.cancelAnalyzeName('Tabs')
      this.redirectToStart()
    } else if (['ExistingRequestEdit'].indexOf(componentName) > -1) {
      // Cancel edit mode
      await this.setEditMode(false)
      // Check in the NR to release the INPROGRESS lock on the NR
      await this.cancelEditExistingRequest(null)
      await NamexServices.checkinNameRequest(this.getNrId, this.getNrState)
      this.redirectToStart()
    } else {
      await this.cancelAnalyzeName('Tabs')
      this.redirectToStart()
    }
  }

  async redirectToStart () {
    console.info('Redirecting to start...') // eslint-disable-line no-console
    // Redirect to the start
    // Catch any errors, so we don't get errors like:
    // Avoided redundant navigation to current location: "/"
    await this.$router.replace('/').catch(() => {})
  }
}
