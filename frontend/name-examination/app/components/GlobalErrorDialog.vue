<template>
  <PopupDialog :show="showErrorDialog">
    <template #title>
      <span v-if="errorQueue[0]" class="inline-flex items-center text-red-600 text-xl">
        <ExclamationTriangleIcon class="mr-2 h-7 w-7 stroke-2" />
        {{ errorQueue[0].title }}
      </span>
    </template>
    <div v-if="errorQueue[0]" class="flex flex-col space-y-4 rounded">
      <span class="whitespace-pre-wrap">{{ errorQueue[0].message }}</span>
      <IconButton light @click="popError">Close</IconButton>
    </div>
  </PopupDialog>
</template>

<script setup lang="ts">
/** Listens for errors on the global event bus and displays an error dialog */
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'
import type { AppError } from '~/types/errors'
import { emitter } from '~/util/emitter'

const showErrorDialog = ref(false)
const errorQueue = ref<Array<AppError>>([])

emitter.on('error', pushError)

function pushError(error: AppError) {
  errorQueue.value.push(error)
  showErrorDialog.value = true
}

function popError() {
  showErrorDialog.value = false
  // wait some time for the dialog to disappear before retrieving next error
  setTimeout(() => {
    errorQueue.value.shift()
    if (errorQueue.value.length > 0) {
      showErrorDialog.value = true
    }
  }, 500)
}
</script>
