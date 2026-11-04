<template>
  <button
    class="inline-flex items-center justify-center space-x-2 rounded px-4 py-1.5 transition hover:text-opacity-100 hover:opacity-90 disabled:pointer-events-none disabled:opacity-70"
    ref="button"
    :class="[
      light
        ? 'bg-bcgov-blue3 text-white'
        : white
        ? 'border border-gray-300 bg-white text-black hover:bg-gray-200'
        : 'bg-bcgov-blue5 text-white',
    ]"
  >
    <slot></slot>

    <!-- User of the component can pass in the text either as a prop or as a template (for custom styled text) -->
    <span v-if="slots.text"><slot name="text"></slot></span>
    <span v-if="text">{{ text }}</span>
  </button>
</template>

<script setup lang="ts">
/**
 * A styled button that contains an icon and/or text
 */
const props = defineProps<{
  text?: string
  /** Use lighter shade of blue for background color */
  light?: boolean
  /** Use white background */
  white?: boolean
  /** Mnemonic letter to trigger this button's onclick event handler */
  mnemonic?: string
}>()

const slots = useSlots()

const button = ref<HTMLButtonElement | null>(null)

if (props.mnemonic) {
  useMnemonic(props.mnemonic, () => button?.value?.click())
}
</script>
