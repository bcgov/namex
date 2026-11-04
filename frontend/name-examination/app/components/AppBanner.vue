<template>
  <NoticeBanner id="app-banner" v-if="bannerText" type="info">
    {{ bannerText }}
  </NoticeBanner>
</template>

<script setup>
/** Banner that shows a notification message to the user, retrieved from Firebase */
import { useNuxtApp } from '#app'
import { getString } from 'firebase/remote-config'
import { FeatureFlags } from '@/util/constants'

const { $remoteConfig } = useNuxtApp()
const bannerText = getString($remoteConfig, FeatureFlags.NAMEX_BANNER)
</script>
