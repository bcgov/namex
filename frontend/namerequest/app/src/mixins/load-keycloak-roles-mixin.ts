import { Component, Vue } from 'vue-property-decorator'
import { getKeycloakRoles } from '@/plugins'
import { Action } from 'pinia-class'
import { useStore } from '@/store'
import { ActionBindingIF } from '@/interfaces/store-interfaces'

@Component({})
export class LoadKeycloakRolesMixin extends Vue {
  @Action(useStore) setKeycloakRoles!: ActionBindingIF

  /** Gets and stores Keycloak roles. */
  loadKeycloakRoles (): void {
    try {
      const keycloakRoles = getKeycloakRoles()
      this.setKeycloakRoles(keycloakRoles)
      console.info('Got roles!') // eslint-disable-line no-console
    } catch (err) {
      const error = err as Error
      // just log the error message
      console.log(`Did not get roles (${error.message})`) // eslint-disable-line no-console
    }
  }
}
