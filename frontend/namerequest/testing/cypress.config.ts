import { defineConfig } from 'cypress'
import fs from 'fs'

export default defineConfig({
  chromeWebSecurity: false,
  defaultCommandTimeout: 40000,
  includeShadowDom: true,
  responseTimeout: 40000,
  redirectionLimit: 100,
  experimentalStudio: true,
  experimentalMemoryManagement: true,
  numTestsKeptInMemory: 0,
  viewportHeight: 1080,
  viewportWidth: 1920,
  video: true,
  reporter: 'mochawesome',
  reporterOptions: {
    files: ['./mochawesome-report/*.json'],
    overwrite: false,
    html: true,
    json: true,
  },
  e2e: {
    // baseUrl: 'https://dev.namex.bcregistry.gov.bc.ca',
    // baseUrl: 'https://test.namex.bcregistry.gov.bc.ca',
    baseUrl: 'https://test.names.bcregistry.gov.bc.ca',
    projectId: '',
    setupNodeEvents(on, config) {
      on('task', {
        checkFileExists(filePath) {
          // Check if the file exists
          if (fs.existsSync(filePath)) {
            return true
          } else {
            return false
          }
        },
      })
      on('before:browser:launch', (browser, launchOptions) => {
        if (
          browser.family === 'chromium' &&
          (browser.name === 'chrome' || browser.name === 'chromium')
        ) {
          // If the browser is Chrome or Chromium, add the flags to expose the `gc` function and disable GPU
          launchOptions.args.push('--js-flags=--expose-gc')
          launchOptions.args.push('--disable-gpu')
        }
        return launchOptions
      })
    },
  },
})
