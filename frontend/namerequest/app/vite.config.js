import { defineConfig } from 'vite'
import vue2 from '@vitejs/plugin-vue2'
import EnvironmentPlugin from 'vite-plugin-environment'
import { NodeModulesPolyfillPlugin } from '@esbuild-plugins/node-modules-polyfill'
import path from 'path'
import fs from 'fs'

const packageJson = fs.readFileSync('./package.json')
const appName = JSON.parse(packageJson).appName
const appVersion = JSON.parse(packageJson).version
const sbcName = JSON.parse(packageJson).sbcName
const sbcVersion = JSON.parse(packageJson).dependencies['sbc-common-components']
const aboutText1 = (appName && appVersion) ? `${appName} v${appVersion}` : ''
const aboutText2 = (sbcName && sbcVersion) ? `${sbcName} v${sbcVersion}` : ''

// https://vitejs.dev/config/
export default defineConfig(() => {
  return {
    define: {
      'import.meta.env.ABOUT_TEXT':
        (aboutText1 && aboutText2) ? `"${aboutText1}<br>${aboutText2}"`
          : aboutText1 ? `"${aboutText1}"`
            : aboutText2 ? `"${aboutText2}"`
              : ''
    },
    envPrefix: 'VUE_APP_', // Need to remove this after fixing vaults. Use import.meta.env with VUE_APP.
    plugins: [
      vue2(),
      EnvironmentPlugin({
        BUILD: 'web' // Fix for Vuelidate, allows process.env with Vite.
      })
    ],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        // next line is needed to prevent "multiple Vue instances" when deployed
        vue: 'vue/dist/vue.runtime.esm.js'
      },
      extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue'],
      // Fix inline dependency of a dependency, which is the case in Tiptap-Vuetify
      mainFields: ['module']
    },
    server: {
      host: true,
      port: 8080
    },
    test: {
      // simulate DOM with jsdom
      environment: 'jsdom',
      // enable jest-like global test APIs
      globals: true,
      setupFiles: ['./tests/setup.ts'],
      // enable threads to speed up test running
      threads: true,
      // hide Vue Devtools message
      onConsoleLog: function (log) {
        if (log.includes('Download the Vue Devtools extension')) {
          return false
        }
      }
    },
    optimizeDeps: {
      // Needs to be in here so there aren't two instances of sbc-common-components created.
      exclude: ['@vue/composition-api', 'sbc-common-components'],
      esbuildOptions: {
        // Fix Module has been externalized for browser compatibility warning.
        plugins: [
          NodeModulesPolyfillPlugin()
        ]
      }
    }
  }
})
