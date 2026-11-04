<template>
  <div
    class="ml-auto flex w-full items-center justify-center space-x-1 border-l-4 px-4 py-1.5"
    :class="{
      'border-red-600 bg-red-200': type === 'warning',
      'border-yellow-600 bg-yellow-200': type === 'lock',
      'border-orange-600 bg-orange-100 py-2': type === 'info',
    }"
  >
    <ExclamationTriangleIcon
      v-if="type === 'warning'"
      class="mt-0.5 h-6 w-6 stroke-2"
    />
    <LockClosedIcon v-if="type === 'lock'" class="mt-0.5 h-6 w-6 stroke-2" />
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
/** Shows a message to the user with a styled banner. */
import {
  ExclamationTriangleIcon,
  LockClosedIcon,
} from '@heroicons/vue/24/outline'

defineProps<{
  type: 'warning' | 'lock' | 'info'
}>()
</script>
