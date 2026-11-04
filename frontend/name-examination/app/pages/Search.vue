<template>
  <div class="mx-4 mt-4 flex h-[91vh] flex-col">
    <h1 class="text-2xl font-bold text-gray-700">Search</h1>
    <SearchResultsControl />
    <SearchResultsBox class="my-4" />
  </div>
</template>

<script setup lang="ts">
useHead({ title: 'BC Registry: Name Examination - Search Name Requests' })
</script>
