import { beforeAll, vi } from 'vitest'
import { createRouter, createMemoryHistory } from 'vue-router'
import { config } from '@vue/test-utils'

const router = createRouter({
  history: createMemoryHistory(),
  routes: []
})

config.global.plugins = [router]

beforeAll(() => {
  vi.mock('../util/namex-api', async (importOriginal) => {
    const mod = await importOriginal()
    return {
      // @ts-ignore
      ...mod,
      // Mock the url that is returned by getNamexApiUrl
      // so that it doesn't throw an error from creating an empty url when
      // the environment variables are undefined, such as when running in ci
      getNamexApiUrl: vi.fn().mockImplementation((endpoint) => {
        return new URL('/api/v1' + endpoint, 'https://localhost:8080/')
      }),
      getNamexObject: vi.fn(),
    }
  })
})
