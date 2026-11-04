<template>
  <div class="mx-8 my-10">
    <ul>
      <li>Check review time and approval status</li>
      <li>Upgrade Name Request to Priority ($100.00)</li>
      <li>Renew your Name Request for an additional 56 days before it expires ($30.00)</li>
      <li>Cancel your Name Request</li>
      <li>Edit details, download receipts, and more</li>
    </ul>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class SearchHelpContent extends Vue {
}
</script>

<style lang="scss" scoped>
ul {
  display: inline-table;

  li  {
    padding-bottom: 10px;
  }
}
</style>
