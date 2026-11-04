import type { NameChoice, NameRequest, Transactions } from '~/types'
import packageInfo from '~/package.json'

/**
 * Retrieve the Keycloak session token, refreshing to make it valid if necessary.
 * @returns the session token
 */
async function getToken(): Promise<string | undefined> {
  const { $auth } = useNuxtApp()
  return await $auth
    .updateToken(30)
    .then((_refreshed) => {
      return $auth.token
    })
    .catch(async (error) => {
      console.error(`Failed to get session token: ${error}`)
      return undefined
    })
}

/**
 * Make an HTTP request to a given Namex API URL.
 * @param options extra options to pass to the `fetch` call, should not include headers
 * @param headers header options to pass to the request
 */
async function callNamexApi(url: URL, options?: object, headers?: object) {
  const token = await getToken()
  return fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
      'App-Name': packageInfo.name,
      'X-Apikey': useRuntimeConfig().public.namexAPIKey || '',
      ...headers,
    },
    ...(options ? options : {}),
  })
}

/**
 * Returns the full NameX API url given an endpoint
 * @param endpoint The API endpoint (including the starting slash '/')
 */
export function getNamexApiUrl(endpoint: string): URL {
  const config = useRuntimeConfig().public
  const base = config.namexAPIURL
  return new URL(
    config.namexAPIVersion.replace(/^\//, '') + endpoint,
    base.endsWith('/') ? base : base + '/' as string
  )
}

/**
 * Make a GET request to the given NameX API URL and return the response json.
 * @param url the url to fetch
 * @returns the json response object
 */
export async function getNamexObject(url: URL): Promise<any> {
  return (await callNamexApi(url)).json()
}

/**
 * Get a name request object given its NR number.
 */
export async function getNameRequest(nrNumber: string) {
  return callNamexApi(getNamexApiUrl(`/requests/${nrNumber}`))
}

/**
 * Patch the name request with the given NR number with a patch object.
 */
export async function patchNameRequest(nrNumber: string, patch: object) {
  const url = getNamexApiUrl(`/requests/${nrNumber}`)
  return callNamexApi(
    url,
    {
      method: 'PATCH',
      body: JSON.stringify(patch),
    },
    { 'content-type': 'application/json' }
  )
}

export async function postNewComment(nrNumber: string, comment: string) {
  const url = getNamexApiUrl(`/requests/${nrNumber}/comments`)
  return callNamexApi(
    url,
    {
      method: 'POST',
      body: JSON.stringify({ comment }),
    },
    { 'content-type': 'application/json' }
  )
}

/** Update a name request's data with the given name request object. */
export async function putNameRequest(nrNumber: string, nrObject: NameRequest) {
  const url = getNamexApiUrl(`/requests/${nrNumber}`)
  return callNamexApi(
    url,
    {
      method: 'PUT',
      body: JSON.stringify(nrObject),
    },
    { 'content-type': 'application/json' }
  )
}

export async function putNameChoice(nrNumber: string, choice: NameChoice) {
  const url = getNamexApiUrl(`/requests/${nrNumber}/names/${choice.choice}`)
  return callNamexApi(
    url,
    {
      method: 'PUT',
      body: JSON.stringify(choice),
    },
    { 'content-type': 'application/json' }
  )
}

export async function getTransactions(nrNumber: string): Promise<Response> {
  return callNamexApi(getNamexApiUrl(`/events/${nrNumber}`))
}

export async function resendNotification(eventId: string): Promise<Response> {
  const url = getNamexApiUrl(`/events/event/${eventId}`)
  return callNamexApi(
    url,
    {
      method: 'POST',
    },
    { 'content-type': 'application/json' }
  )
}

export async function getBusiness(corpNum: string) {
  return callNamexApi(getNamexApiUrl(`/businesses/${corpNum}`))
}

async function postDocuments(resource: string, query: string) {
  const url = getNamexApiUrl(`/documents:${resource}`)
  return callNamexApi(
    url,
    {
      method: 'POST',
      body: JSON.stringify({ type: 'plain_text', content: query }),
    },
    { 'content-type': 'application/json' }
  )
}

export async function postTrademarks(query: string) {
  return postDocuments('trademarks', query)
}

export async function postConditions(query: string) {
  const url = getNamexApiUrl(`/documents/restricted-words`)
  return callNamexApi(
    url,
    {
      method: 'POST',
      body: JSON.stringify({ type: 'plain_text', content: query }),
    },
    { 'content-type': 'application/json' }
  )
}

export async function postHistories(query: string) {
  return postDocuments('histories', query)
}

export async function getDecisionReasons() {
  return callNamexApi(getNamexApiUrl(`/requests/decisionreasons`))
}

export async function getPossibleConflicts(name: string, exactPhrase?: string): Promise<Response> {
  const phrase = exactPhrase?.trim()
  const nameTrim = name?.trim() ?? ''
  const query = phrase && !nameTrim ? phrase : nameTrim
  const url = getNamexApiUrl(`/requests/possible-conflicts/${encodeURIComponent(query)}`)
  if (phrase) {
    url.searchParams.set('exact_phrase', phrase)
  }
  return callNamexApi(url)
}

function conflictSearchBody(data: any): any {
  let body = data?.rootCause ?? data
  if (typeof body === 'string') {
    try {
      body = JSON.parse(body)
    } catch {
      return data
    }
  }
  return body
}

export async function conflictSearchErrorMessage(response: Response): Promise<string> {
  try {
    const body = conflictSearchBody(await response.json())
    if (body?.code === 'QUERY_TOO_COMPLEX') {
      return (
        body.message ||
        'This name is too complex for conflict search. Remove a word and try again.'
      )
    }
  } catch {
    // non-JSON error bodies keep the generic conflicts message
  }
  return 'Unable to retrieve possible conflicts'
}

export async function getNextNrNumber(isPriority: boolean) {
  return callNamexApi(
    getNamexApiUrl(`/requests/queues/@me/oldest?priorityQueue=${isPriority}`)
  )
}

export async function getCorporation(corpNum: string) {
  return callNamexApi(getNamexApiUrl(`/colin/${corpNum}`))
}

export async function getPayments(id: number) {
  return callNamexApi(getNamexApiUrl(`/payments/${id}`))
}

export async function getStats(params: URLSearchParams) {
  return callNamexApi(getNamexApiUrl('/requests/stats?' + params))
}

export async function getNamexApiVersion() {
  return callNamexApi(getNamexApiUrl('/meta/info'))
}
