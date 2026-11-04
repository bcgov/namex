<template>
  <MainContainer id="success-container">
    <template #content>
      <v-row class="my-9 py-9">
        <v-col
          cols="12"
          class="text-center h4"
        >
          Update Successful
        </v-col>
        <v-col
          cols="12"
          class="text-center approved fs-58"
        >
          <v-icon class="approved fs-58">
            mdi-check-circle
          </v-icon>
        </v-col>
      </v-row>
    </template>
  </MainContainer>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import MainContainer from '@/components/new-request/main-container.vue'

@Component({
  components: {
    MainContainer
  }
})
export default class Success extends Vue {}
</script>

<style scoped lang="scss">
.fs-58 {
  font-size: 58px !important;
}
</style>
