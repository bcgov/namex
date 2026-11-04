<template>
  <div class="flex flex-wrap items-center gap-1">
    <div
      v-for="item in modelValue"
      :key="getKey ? getKey(item) : undefined"
      class="flex h-fit w-fit flex-nowrap items-center space-x-1 rounded border border-gray-400 bg-sky-100 p-0.5 px-1 text-sm"
    >
      <span class="truncate max-w-xs">{{ display ? display(item) : item }}</span>
      <button
        @click="onChipRemove($event, modelValue, item)"
        class="rounded hover:bg-sky-200"
      >
        <XMarkIcon class="h-4 w-4" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
/** A grid of small components that represent a list of items that are deletable. */
import { XMarkIcon } from '@heroicons/vue/24/outline'

defineProps<{
  modelValue: Array<any>
  /** Function called for retrieving a string to display for an item on a chip */
  display?: (input: any) => string
  /** Function called for getting a key for a given chip item */
  getKey?: (input: any) => string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', newValue: any): void
  (e: 'chipRemoved', item: any): void
}>()

// NOTE: The `modelValue` variable from the `defineProps` call above doesn't update properly for some reason.
// The workaround is to pass the modelValue as a parameter when calling this function from the template.
function onChipRemove(event: MouseEvent, items: unknown[], item: unknown) {
  event.stopPropagation()
  emit(
    'update:modelValue',
    items.filter((c) => c !== item)
  )
  emit('chipRemoved', item)
}
</script>
