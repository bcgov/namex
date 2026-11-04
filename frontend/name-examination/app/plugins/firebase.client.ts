import { initializeApp } from 'firebase/app'
import { getRemoteConfig, fetchAndActivate } from 'firebase/remote-config'
import { getAnalytics } from 'firebase/analytics'
import { FeatureFlags } from '@/util/constants'

export default defineNuxtPlugin(async (nuxtApp) => {
  const config = useRuntimeConfig()

  const firebaseConfig = {
    apiKey: config.public.firebaseApiKey,
    authDomain: config.public.firebaseAuthDomain,
    projectId: config.public.firebaseProjectId,
    appId: config.public.firebaseAppId
  }

  const app = initializeApp(firebaseConfig)

  const analytics = getAnalytics(app)
  const remoteConfig = getRemoteConfig(app)

  remoteConfig.settings.fetchTimeoutMillis = 60000
  remoteConfig.settings.minimumFetchIntervalMillis = 60000

  remoteConfig.defaultConfig = {
    [FeatureFlags.NAMEX_BANNER]: ''
  }

  await fetchAndActivate(remoteConfig)

  // Only this is needed
  nuxtApp.provide('analytics', analytics)
  nuxtApp.provide('remoteConfig', remoteConfig)
})
