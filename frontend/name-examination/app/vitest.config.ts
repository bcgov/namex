import { defineVitestConfig } from '@nuxt/test-utils/config'

export default defineVitestConfig({
  test: {
    environment: 'nuxt',
    setupFiles: ['./tests/vue-test-utils-plugins.ts', './tests/setup.ts'],
  },
})
