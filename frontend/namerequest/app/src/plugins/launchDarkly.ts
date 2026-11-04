import { initialize, LDClient, LDContext, LDFlagSet, LDOptions } from 'launchdarkly-js-client-sdk'

// get rid of "element implicitly has an 'any' type..."
declare const window: any

/**
 * Default flag values when LD is not available.
 * Uses "namerequest" project (per LD client id in env config).
 */
const defaultFlagSet: LDFlagSet = {
  'banner-text': '', // by default, there is no banner text
  'disable-analysis': true, // by default, analysis is disabled
  'enable-genesys-web-message': false, // by default, genesys web message is disabled
  'enable-numbered-company-launcher': false, // by default, numbered company launcher is disabled
  'enable-priority-checkbox': false, // by default, priority is disabled
  'enable-society': false, // by default society is disabled
  'enable-web-chat': false, // by default, old webchat is disabled
  'hardcoded_priority_wait_time': 0, // by default, use actual wait time
  'hardcoded_regular_wait_time': 0, // by default, use actual wait time
  'priority-wait-time-tooltip-text': '', // by default, display default tooltip text
  'supported-amalgamation-entities': [],
  'supported-continuation-in-entities': [],
  'supported-incorporation-registration-entities': [],
  'use-business-api-gw-url': false
}

/**
 * The Launch Darkly client instance.
 */
let ldClient: LDClient = null

/**
 * An async method that initializes the Launch Darkly client.
 */
export async function InitLdClient (): Promise<void> {
  const envKey: string = window['ldClientId']

  if (envKey) {
    // since we have no user or org data yet, start with an anonymous user context
    const context: LDContext = { kind: 'user', key: 'anonymous', anonymous: true }

    const options: LDOptions = {
      // fetch flags using REPORT request (to see user data as JSON)
      useReport: true,
      // opt out of sending diagnostics data
      diagnosticOptOut: true,
      // open streaming connection for live flag updates
      streaming: true
    }

    ldClient = initialize(envKey, context, options)

    try {
      await ldClient.waitForInitialization()
    } catch {
      // shut down client -- `variation()` will return undefined values
      await ldClient.close()
      // do nothing -- LD logs its own errors
    }
  }
}

/**
 * An async method that updates the Launch Darkly user and org properties.
 * @param user an optional user context object
 * @param org an optional organization context object
 */
export async function UpdateLdUser (user: LDContext, org: LDContext): Promise<void> {
  if (ldClient) {
    try {
      if (user && org) await ldClient.identify({ kind: 'multi', user, org })
      else if (user) await ldClient.identify(user)
      else if (org) await ldClient.identify(org)
    } catch {
      // do nothing -- LD logs its own errors
    }
  }
}

/**
 * A method that gets the value of the specified feature flag.
 * @param name the name of the feature flag
 * @returns the flag value/variation, or undefined if the flag is not found
 */
export function GetFeatureFlag (name: string): any {
  return ldClient ? ldClient.variation(name) : defaultFlagSet[name]
}
