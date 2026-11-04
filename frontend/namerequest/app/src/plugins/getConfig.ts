import axios from 'axios'

export function getConfig (): void {
  // get config from environment
  const windowLocationOrigin = window.location.origin
  const envVueAppPath = import.meta.env.VUE_APP_PATH as string
  const envBaseUrl = import.meta.env.BASE_URL

  if (!windowLocationOrigin || !envVueAppPath || !envBaseUrl) {
    throw new Error('Missing environment variables')
  }

  // set Base URL for fetching local documents and for returning from redirects
  const baseUrl = `${windowLocationOrigin}${envVueAppPath}`.replace(/\/+$/, '') // trim trailing slash
  sessionStorage.setItem('BASE_URL', baseUrl)

  // set base URL for axios calls
  axios.defaults.baseURL = baseUrl

  const paymentPortalUrl: string = import.meta.env.VUE_APP_PAYMENT_PORTAL_URL
  sessionStorage.setItem('PAYMENT_PORTAL_URL', paymentPortalUrl)

  const corporateOnlineUrl: string = import.meta.env.VUE_APP_CORPORATE_ONLINE_URL
  sessionStorage.setItem('CORPORATE_ONLINE_URL', corporateOnlineUrl)

  const businessDashUrl: string = import.meta.env.VUE_APP_BUSINESS_DASH_URL
  sessionStorage.setItem('BUSINESS_DASH_URL', businessDashUrl)

  const businessHomeUrl: string = import.meta.env.VUE_APP_BUSINESS_HOME_URL
  sessionStorage.setItem('BUSINESS_HOME_URL', businessHomeUrl)

  const businessRegistryUrl: string = import.meta.env.VUE_APP_BUSINESS_REGISTRY_URL
  sessionStorage.setItem('BUSINESS_REGISTRY_URL', businessRegistryUrl)

  const namexApiURL: string = import.meta.env.VUE_APP_NAMEX_API_GW_URL + import.meta.env.VUE_APP_NAMEX_API_VERSION
  sessionStorage.setItem('NAMEX_API_URL', namexApiURL)

  const legalApiUrl: string = import.meta.env.VUE_APP_LEGAL_API_URL + import.meta.env.VUE_APP_LEGAL_API_VERSION_2
  sessionStorage.setItem('LEGAL_API_URL', legalApiUrl)

  const businessApiGwUrl: string =
    import.meta.env.VUE_APP_BUSINESS_API_GW_URL + import.meta.env.VUE_APP_LEGAL_API_VERSION_2
  sessionStorage.setItem('BUSINESS_API_GW_URL', businessApiGwUrl)

  const authApiUrl: string = import.meta.env.VUE_APP_AUTH_API_URL + import.meta.env.VUE_APP_AUTH_API_VERSION
  sessionStorage.setItem('AUTH_API_URL', authApiUrl)

  const siteminderLogoutUrl: string = import.meta.env.VUE_APP_SITEMINDER_LOGOUT_URL
  sessionStorage.setItem('SITEMINDER_LOGOUT_URL', siteminderLogoutUrl)

  const registryHomeUrl: string = import.meta.env.VUE_APP_REGISTRY_HOME_URL
  sessionStorage.setItem('REGISTRY_HOME_URL', registryHomeUrl)

  const societiesOnlineHomeUrl: string = import.meta.env.VUE_APP_SOCIETIES_ONLINE_HOME_URL
  sessionStorage.setItem('SOCIETIES_ONLINE_HOME_URL', societiesOnlineHomeUrl)

  const stepsToRestoreUrl: string = import.meta.env.VUE_APP_STEPS_TO_RESTORE_URL
  sessionStorage.setItem('STEPS_TO_RESTORE_URL', stepsToRestoreUrl)

  // for system alert banner (sbc-common-components)
  const statusApiUrl: string = import.meta.env.VUE_APP_STATUS_API_URL + import.meta.env.VUE_APP_STATUS_API_VERSION
  sessionStorage.setItem('STATUS_API_URL', statusApiUrl)

  // for sbc header (sbc-common-components)
  const authWebUrl: string = import.meta.env.VUE_APP_AUTH_WEB_URL
  sessionStorage.setItem('AUTH_WEB_URL', authWebUrl)

  const registriesSearchApiUrl: string =
    (import.meta.env.VUE_APP_REGISTRIES_SEARCH_API_URL + import.meta.env.VUE_APP_REGISTRIES_SEARCH_API_VERSION_2 + '/')
  sessionStorage.setItem('REGISTRIES_SEARCH_API_URL', registriesSearchApiUrl)

  const ldClientId: string = import.meta.env.VUE_APP_NAMEREQUEST_LD_CLIENT_ID;
  (<any>window).ldClientId = ldClientId

  const authTokenUrl: string = import.meta.env.VUE_APP_AUTH_TOKEN_URL;
  (<any>window).authTokenUrl = authTokenUrl

  const quickSearchPublicId: string = import.meta.env.VUE_APP_QUICK_SEARCH_PUBLIC_ID;
  (<any>window).quickSearchPublicId = quickSearchPublicId

  const quickSearchPublicSecret: string = import.meta.env.VUE_APP_QUICK_SEARCH_PUBLIC_SECRET;
  (<any>window).quickSearchPublicSecret = quickSearchPublicSecret

  const genesysEnv: string = import.meta.env.VUE_APP_GENESYS_ENV;
  (<any>window).genesysEnv = genesysEnv

  const genesysId: string = import.meta.env.VUE_APP_GENESYS_ID;
  (<any>window).genesysId = genesysId

  const genesysUrl: string = import.meta.env.VUE_APP_GENESYS_URL;
  (<any>window).genesysUrl = genesysUrl

  const webChatUrl: string = import.meta.env.VUE_APP_WEBCHAT_URL;
  (<any>window).webChatUrl = webChatUrl

  const webChatReason: string = import.meta.env.VUE_APP_WEBCHAT_REASON;
  (<any>window).webChatReason = webChatReason

  const webChatStatusUrl: string = import.meta.env.VUE_APP_WEBCHAT_STATUS_URL;
  (<any>window).webChatStatusUrl = webChatStatusUrl

  const entitySelectorUrl: string = import.meta.env.VUE_APP_ENTITY_SELECTOR_URL
  entitySelectorUrl && sessionStorage.setItem('ENTITY_SELECTOR_URL', entitySelectorUrl)

  const keycloakAuthUrl: string = import.meta.env.VUE_APP_KEYCLOAK_AUTH_URL;
  (<any>window).keycloakAuthUrl = keycloakAuthUrl

  const keycloakRealm: string = import.meta.env.VUE_APP_KEYCLOAK_REALM;
  (<any>window).keycloakRealm = keycloakRealm

  const keycloakClientId: string = import.meta.env.VUE_APP_KEYCLOAK_CLIENTID;
  (<any>window).keycloakClientId = keycloakClientId
}
