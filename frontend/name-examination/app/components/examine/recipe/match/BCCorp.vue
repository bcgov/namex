<template>
  <div class="flex p-2 text-sm">
    <div class="grid basis-1/2 grid-cols-2 gap-y-2 overflow-x-auto">
      <h3 class="font-bold">Type</h3>
      <p>BC Corporation</p>

      <h3 class="font-bold">Corp Number</h3>
      <p>{{ data['identifier'] }}</p>

      <h3 class="font-bold">Directors</h3>
      <div class="flex flex-col">
        <p v-if="!data?.directors?.length">Not Available</p>
        <p v-else v-for="director in data.directors">{{ director }}</p>
      </div>

      <h3 class="font-bold">Nature of Business</h3>
      <p>{{ data['nature of business'] }}</p>
    </div>

    <div class="grid basis-1/2 grid-cols-2 overflow-x-auto">
      <h3 class="font-bold">Records Office Delivery Address</h3>
      <div>
        <p v-if="!data?.['records office delivery address']?.length">
          Not Available
        </p>
        <p
          v-else
          v-for="addrLine in parseAddress(
            data['records office delivery address']
          )"
        >
          {{ addrLine }}
        </p>
      </div>

      <h3 class="font-bold">Registered Office Delivery Address</h3>
      <div v-if="data['registered office delivery address']">
        <p
          v-for="addrLine in parseAddress(
            data['registered office delivery address']
          )"
        >
          {{ addrLine }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { BCCorporation } from '~/types'
import { parseAddress } from '~/util'

defineProps<{
  data: BCCorporation
}>()
</script>
