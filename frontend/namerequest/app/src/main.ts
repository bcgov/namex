import Vue from 'vue'
import App from './App.vue'
import { getVueRouter } from '@/router'
import { getConfig, getKeycloakGuid, getVuetify, InitLdClient, isSigningIn, isSigningOut, getPiniaStore,
  getVuexStore } from '@/plugins'
import AuthServices from '@/services/auth-services'
import KeycloakService from 'sbc-common-components/src/services/keycloak.services'
import { SessionStorageKeys } from 'sbc-common-components/src/util/constants'
import ConfigHelper from 'sbc-common-components/src/util/config-helper'

// Styles
// NB: order matters - do not change
import 'quill/dist/quill.core.css'
import 'vuetify/dist/vuetify.min.css'
import '@mdi/font/css/materialdesignicons.min.css'
import '@/assets/styles/base.scss'
import '@/assets/styles/layout.scss'
import '@/assets/styles/overrides.scss'

Vue.config.productionTip = true
Vue.config.devtools = true

const vuetify = getVuetify()
const router = getVueRouter()
const store = getVuexStore()
const pinia = getPiniaStore()

// attach global Vuex store and Vuetify instance to Vue instance
Vue.prototype.$store = store
Vue.prototype.$vuetify = vuetify

/**
 * Our app start code, which is a function so that:
 * 1. we can use await
 * 2. we can catch errors
 */
async function startVue () {
  // Fetch the configuration
  getConfig()

  // FUTURE: remove this global assignment if possible
  Vue.prototype.$PAYMENT_PORTAL_URL = import.meta.env.VUE_APP_PAYMENT_PORTAL_URL as string

  // Initialize Keycloak / sync SSO
  await syncSession()

  // Seed the current account before the app mounts
  await syncCurrentAccount()

  // Initialize Launch Darkly
  if (window['ldClientId']) {
    console.info('Initializing Launch Darkly...') // eslint-disable-line no-console
    await InitLdClient()
  }

  // Start Vue application
  console.info('Starting app...') // eslint-disable-line no-console
  new Vue({
    vuetify,
    router,
    store,
    pinia,
    render: h => h(App)
  }).$mount('#app')
}

async function syncSession () {
  console.info('Starting Keycloak service...') // eslint-disable-line no-console
  const keycloakConfig: any = {
    url: `${window['keycloakAuthUrl']}`,
    realm: `${window['keycloakRealm']}`,
    clientId: `${window['keycloakClientId']}`
  }

  await KeycloakService.setKeycloakConfigUrl(keycloakConfig)
  // Auto authenticate user only if they are not trying a login or logout
  if (!isSigningIn() && !isSigningOut()) {
    // Initialize token service which will do a check-sso to initiate session
    await KeycloakService.initializeToken(null).then(() => {
      const token = ConfigHelper.getFromSession(SessionStorageKeys.KeyCloakToken)
      if (!token) {
        // when there is no token in session storage, e.g. because token has expired due to user inactivity,
        // make sure to clear out account info saved on previous login
        ConfigHelper.removeFromSession(SessionStorageKeys.CurrentAccount)
      }
    }).catch(err => {
      if (err?.message !== 'NOT_AUTHENTICATED') {
        throw err
      }
    })
  }
}

/**
 * Seeds the current account in session storage before the app mounts, so that code
 * which reads CURRENT_ACCOUNT on startup (eg, the NR replay logic in App.vue) doesn't
 * race SbcHeader's asynchronous account sync. Honours the "accountid" query param
 * appended to the return URL by the Business Home login page.
 */
async function syncCurrentAccount (): Promise<void> {
  const token = ConfigHelper.getFromSession(SessionStorageKeys.KeyCloakToken)
  if (!token) return

  const urlAccountId = new URLSearchParams(window.location.search).get('accountid')
  const storedAccountId = JSON.parse(
    ConfigHelper.getFromSession(SessionStorageKeys.CurrentAccount) || '{}'
  )?.id
  // nothing to do if an account is already stored and the URL doesn't specify a different one
  if (storedAccountId && (!urlAccountId || String(storedAccountId) === urlAccountId)) return

  await AuthServices.fetchUserSettings(getKeycloakGuid()).then(settings => {
    const accounts = settings?.filter(setting => setting.type === 'ACCOUNT') || []
    const account = accounts.find(acct => String(acct.id) === urlAccountId) || accounts[0]
    if (account) {
      ConfigHelper.addToSession(SessionStorageKeys.CurrentAccount, JSON.stringify(account))
    }
  }).catch(error => {
    // don't block app startup - SbcHeader will sync the account when it mounts
    console.error('syncCurrentAccount =', error) // eslint-disable-line no-console
  })
}

// NB: the .then() makes sure linter doesn't pick up on an un-awaited promise
startVue().then().catch(error => {
  console.error('main =', error) // eslint-disable-line no-console
})
