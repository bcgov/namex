<template>
  <Tab v-slot="{ selected }">
    <IconButton
      white
      :class="[
        'h-8 w-full border bg-white hover:!bg-gray-200',
        selected
          ? 'border-2 border-gray-700 !bg-sky-100 hover:!bg-sky-100'
          : '',
      ]"
      :text="text"
    >
      <CheckCircleIcon
        v-if="type === 'ok'"
        class="h-5 w-5 stroke-2 text-lime-600"
      />
      <ExclamationCircleIcon
        v-if="type === 'warning'"
        class="h-5 w-5 stroke-2 text-yellow-600"
      />
      <XCircleIcon
        v-if="type === 'error'"
        class="h-5 w-5 stroke-2 text-red-error"
      />
      <slot v-if="type === 'custom'"></slot>
    </IconButton>
  </Tab>
</template>

<script setup lang="ts">
import { Tab } from '@headlessui/vue'
import {
  CheckCircleIcon,
  ExclamationCircleIcon,
  XCircleIcon,
} from '@heroicons/vue/24/outline'

defineProps<{
  text: string
  type: 'ok' | 'warning' | 'error' | 'custom'
}>()
</script>
