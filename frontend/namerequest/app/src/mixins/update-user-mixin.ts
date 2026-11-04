import { Component, Vue } from 'vue-property-decorator'
import { Getter } from 'pinia-class'
import { useStore } from '@/store'
import { UpdateLdUser } from '@/plugins'
import AuthServices from '@/services/auth-services'
import { SessionStorageKeys } from 'sbc-common-components/src/util/constants'

@Component({})
export class UpdateUserMixin extends Vue {
  @Getter(useStore) getKeycloakRoles!: string[]

  /** Fetches the user and org info and updates LaunchDarkly. */
  async updateLaunchDarkly (): Promise<any> {
    // don't run when Vitest is running the code
    if (import.meta.env.VITEST) return

    try {
      // get user info
      const userInfo = await AuthServices.fetchUserInfo().catch(() => null)

      // get org info
      const currentAccount = sessionStorage.getItem(SessionStorageKeys.CurrentAccount)
      const accountId = currentAccount && JSON.parse(currentAccount)?.id
      const orgInfo = accountId && await AuthServices.fetchOrgInfo(accountId).catch(() => null)

      const userContext = userInfo && {
        kind: 'user',
        // since username is unique, use it as the user key
        key: userInfo.username,
        // if we can't get contact email then use user email
        email: userInfo.contacts[0]?.email || userInfo.email,
        firstName: userInfo?.firstname,
        lastName: userInfo?.lastname,
        roles: this.getKeycloakRoles
      }

      const orgContext = orgInfo && {
        kind: 'organization',
        key: orgInfo.id.toString(),
        name: orgInfo.name
      }

      return UpdateLdUser(userContext, orgContext)
    } catch (err) {
      // just log the error -- no need to halt app
      console.log('Error updating LaunchDarkly =', err) // eslint-disable-line no-console
    }
  }
}
