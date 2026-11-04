import Keycloak from 'keycloak-js'

export default defineNuxtPlugin(async (_nuxtApp) => {
  const config = useRuntimeConfig()
  const keycloak = new Keycloak({
    url: config.public.keycloakAuthUrl,
    realm: config.public.keycloakRealm,
    clientId: config.public.keycloakClientId,
  })

  try {
    const authenticated = await keycloak.init({
      onLoad: 'login-required',
      responseMode: 'query',
      pkceMethod: 'S256',
    })
  } catch (error) {
    console.error('Failed to initialize Keycloak adapter: ', error)
  }

  return {
    provide: {
      auth: keycloak,
      userProfile: await keycloak.loadUserProfile(),
    },
  }
})
