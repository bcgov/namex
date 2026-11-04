<template>
  <div class="flex p-2 text-sm">
    <div class="grid basis-1/2 grid-cols-2 gap-y-2 overflow-x-auto">
      <h3 class="font-bold">Type</h3>
      <p>XPRO Corporation</p>

      <h3 class="font-bold">Corp Number</h3>
      <p>{{ conflict['identifier'] }}</p>

      <h3 class="font-bold">Attorneys</h3>
      <div class="flex flex-col">
        <p v-if="!conflict?.['attorney names']?.length">Not available</p>
        <p v-else v-for="attorney in conflict['attorney names']">
          {{ attorney }}
        </p>
      </div>

      <b>Nature of Business</b>
      <p>{{ conflict['nature of business'] }}</p>
    </div>

    <div class="grid basis-1/2 grid-cols-2 overflow-x-auto">
      <h3 class="font-bold">Directors</h3>
      <div class="flex flex-col">
        <p v-if="!conflict?.directors?.length">Not available</p>
        <p v-else v-for="director in conflict.directors">{{ director }}</p>
      </div>

      <h3 class="font-bold">Head Office</h3>
      <div v-if="conflict['head office']" >
        <p v-for="addrLine in parseAddress(conflict['head office'])">
          {{ addrLine }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { XproCorporation } from '~/types'
import { parseAddress } from '~/util'

defineProps<{
  conflict: XproCorporation
}>()

const isNotAvailable = (val: any) => val === 'Not Available'
</script>
