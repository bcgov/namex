// https://v3.nuxtjs.org/api/configuration/nuxt.config
import path from 'path'

export default defineNuxtConfig({
  ssr: false,
  devServer: {
    port: 8080,
  },
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'BC Registry: Name Examination',
    },
    baseURL: '/',
  },
  modules: [
    '@nuxt/content',
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
  ],
  css: ['@/assets/css/main.scss'],
  typescript: {
    typeCheck: true,
  },
  pinia: {
    autoImports: [
      // automatically imports `defineStore`
      'defineStore', // import { defineStore } from 'pinia'
      ['defineStore', 'definePiniaStore'], // import { defineStore as definePiniaStore } from 'pinia'
      'acceptHMRUpdate', // import `acceptHMRUpdate` from 'pinia
    ],
  },
  vite: {
    mode: 'spa',
  },
  nitro: {
    output: {
      publicDir: path.join(__dirname, 'dist'),
    },
  },
  runtimeConfig: {
    // Private keys are only available on the server
    // apiSecret: '123',

    // Public keys that are exposed to the client
    public: {
      firebaseApiKey: process.env.NUXT_API_KEY,
      firebaseAuthDomain: process.env.NUXT_AUTH_DOMAIN,
      firebaseProjectId: process.env.NUXT_PROJECT_ID,
      firebaseAppId: process.env.NUXT_APP_ID,
      namexAPIURL: process.env.NUXT_NAMEX_API_GW_URL,
      namexAPIKey: process.env.NUXT_NAMEX_API_KEY,
      namexAPIVersion: process.env.NUXT_NAMEX_API_VERSION,
      namexAdminURL: process.env.NUXT_NAMEX_ADMIN_URL,
      keycloakAuthUrl: process.env.NUXT_KEYCLOAK_AUTH_URL,
      keycloakRealm: process.env.NUXT_KEYCLOAK_REALM,
      keycloakClientId: process.env.NUXT_KEYCLOAK_CLIENTID,
    },
  },
})
