<template>
  <nuxt-link :to="route">
    <span
      class="whitespace-nowrap font-medium transition hover:border-b-2 hover:border-bcgov-blue5"
      :class="{
        'border-b-2 border-bcgov-blue5': highlight,
      }"
    >
      {{ text }}
    </span>
  </nuxt-link>
</template>

<script setup lang="ts">
/** A navigation link that takes you to another page. */
const { route } = defineProps<{
  /** The text that the link should display */
  text: string
  /** The page this link should lead to */
  route: string
}>()

const highlight = computed(
  () =>
    route &&
    useRoute().path.toString().toLowerCase().startsWith(route.toLowerCase())
)
</script>
