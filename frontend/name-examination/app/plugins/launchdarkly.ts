/* eslint-disable valid-jsdoc */
import { initLdClient } from '../util/feature-flags'
import { SessionStorageKeys } from '../util/constants'
// get rid of "element implicitly has an 'any' type..."
declare const window: any
/**
 * This plugin function is called before instantiating the root Vue.js application.
 * It initializes LaunchDarkly.
 */
export default defineNuxtPlugin(async (nuxtApp) => {
  // save id to window object for init function
  window['ldClientId'] = nuxtApp.$config.ldClientId

  if (window['ldClientId']) {
    console.info('Initializing LaunchDarkly...')

    // initialize LD using local library
    const ldClient = await initLdClient()

    // also save flags in session for common components (eg, SbcHeader)
    const allFlags = JSON.stringify(ldClient.allFlags())
    sessionStorage.setItem(SessionStorageKeys.LaunchDarklyFlags, allFlags)
  }
})
