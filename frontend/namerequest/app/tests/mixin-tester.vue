<template>
  <div class="d-none" />
</template>

<script lang="ts">
import { Component, Mixins } from 'vue-property-decorator'
import { DateMixin } from '@/mixins/date-mixin'

/** Special component used only for testing mixins. */
@Component({})
export default class MixinTester extends Mixins(DateMixin) {}
</script>

<style>
</style>
