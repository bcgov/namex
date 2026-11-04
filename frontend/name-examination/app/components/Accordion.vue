<template>
  <div :class="{ 'pointer-events-none': disabled }">
    <button
      class="accordion-title flex w-full items-center justify-between rounded p-1 text-left text-sm font-medium outline-none transition"
      :class="buttonStyle"
      @click="onTitleClick"
    >
      <slot name="title"></slot>
      <ChevronDownIcon
        v-if="arrow"
        :class="isOpen ? 'rotate-180 transform' : ''"
        class="ml-1 h-5 w-5 stroke-2 transition"
      />
    </button>
    <div v-if="isOpen" class="p-1">
      <slot name="content"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * Component that can show hidden content when clicked.
 */
import { ChevronDownIcon } from '@heroicons/vue/24/outline'

const props = defineProps<{
  open: boolean
  arrow?: boolean
  /** Tailwind class list that is passed to the header/summary element */
  buttonStyle?: any
  /** Whether the accordion is disabled (can't be clicked) */
  disabled?: boolean
}>()

const isOpen = ref(props.open)

const emit = defineEmits<{
  titleClicked: []
}>()

watch(
  () => [props.open],
  () => {
    isOpen.value = props.open
  }
)

function onTitleClick(_e: MouseEvent) {
  isOpen.value = !isOpen.value
  emit('titleClicked')
}
</script>
