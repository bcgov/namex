<template>
  <v-row
    id="quick-search-names"
    no-gutters
  >
    <v-col class="pa-3">
      <v-row
        v-for="name of namesList"
        :key="name.name"
        class="quickSearchNames"
        no-gutters
      >
        <v-col>
          <b v-if="name.type==='exact'">{{ name.name }}</b>
          <span v-else>{{ name.name }}</span>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import MainContainer from '@/components/new-request/main-container.vue'

@Component({
  components: { MainContainer }
})
export default class QuickSearchNames extends Vue {
  @Prop() readonly namesList!: Array<{ name: string, type: string }>
}

</script>

<style scoped lang="scss">
@import '@/assets/styles/theme.scss';
#quick-search-names {
  background-color: $gray1;
  display: block;
  max-height: 10.5rem;
  overflow: auto;
}
.quickSearchNames {
    font-size: $px-16;
    line-height: 1.75rem;
    color: $text;
}
</style>
