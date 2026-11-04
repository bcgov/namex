<template>
  <!-- Navigation Link Container -->
  <li
    :class="{
      'inline-block mr-1 lg:pr-2 xl:mr-2': true,
      'lg:border-r border-solid border-bcgov-blue3': !isLast
    }"
  >
    <!-- Nuxt Navigation Link Text -->
    <nuxt-link
      :to="route"
      class="px-2 py-1 text-white hover:underline"
      :target="target"
    >
      {{ text }}
    </nuxt-link>
  </li>
</template>

<script setup lang="ts">
defineProps<{
  text: string,
  route: string,
  target: string,
  isLast: boolean
}>()
</script>
