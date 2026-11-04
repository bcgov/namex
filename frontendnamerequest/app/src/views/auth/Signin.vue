<template>
  <!-- this page immediately redirects to the Business Home login page -->
  <div />
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { getBusinessHomeLoginUrl, Navigate } from '@/plugins'

/**
 * When the user clicks "Log in":
 * - they are redirected to THIS page
 * - this forwards them to the Business Home login page, which triggers the chosen
 *   login method immediately (or offers all login options if the method is unknown)
 * - after login/account selection and/or creation, Business Home redirects back to the main app page
 * - then the Keycloak information is picked up on app init (see syncSession() in main.ts)
 *   and roles / LaunchDarkly are loaded (see App.vue created()).
 */
@Component({})
export default class Signin extends Vue {
  /** The login method, which is passed in the signin route by the SBC Header. */
  @Prop({ default: 'bcsc' }) readonly idpHint!: string

  created (): void {
    Navigate(getBusinessHomeLoginUrl(`${window.location.origin}${import.meta.env.VUE_APP_PATH}`, this.idpHint))
  }
}
</script>
