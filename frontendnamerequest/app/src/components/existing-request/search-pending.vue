<template>
  <MainContainer id="search-pending-container">
    <template #container-header>
      <v-col cols="auto h4 py-0 mt-1">
        You are searching for an existing Name Request
      </v-col>
    </template>

    <template #content>
      <v-row
        justify="center"
        class="mt-3"
      >
        <v-col cols="auto">
          <b>Please wait a moment</b>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col cols="auto">
          <v-progress-circular
            id="analyze-pending-spinner"
            color="orange"
            size="50"
            indeterminate
          />
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col
          cols="auto"
          class="copy-small pb-0"
        >
          Search Status: Searching
        </v-col>
      </v-row>
    </template>
  </MainContainer>
</template>

<script lang="ts">
import MainContainer from '@/components/new-request/main-container.vue'
import { Component, Vue } from 'vue-property-decorator'

@Component({
  components: { MainContainer }
})
export default class SearchPending extends Vue {}
</script>
