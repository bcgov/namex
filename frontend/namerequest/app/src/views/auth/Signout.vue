<template>
  <SbcSignout :redirectUrl="redirectUrl" />
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import SbcSignout from 'sbc-common-components/src/components/SbcSignout.vue'

/**
 * When the user clicks "Log out", they are are redirected to THIS page, which
 * renders the SbcSignout component that actually performs the signout process.
 */
@Component({
  components: { SbcSignout }
})
export default class Signout extends Vue {
  /** The URL to redirect to when the signout process completes: the NR URL. */
  get redirectUrl (): string {
    return `${window.location.origin}${import.meta.env.VUE_APP_PATH}`
  }
}
</script>
