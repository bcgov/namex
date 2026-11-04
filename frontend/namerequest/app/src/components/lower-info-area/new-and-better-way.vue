<template>
  <div
    id="new-and-better-way"
    class="pt-16 pb-4"
  >
    <v-row
      no-gutters
      class="px-6 content-container"
    >
      <v-col
        cols="12"
        md="6"
        lg="6"
        class="pb-4"
        :class="{'pr-15' : !isMobile }"
      >
        <img
          class="max-width-100"
          src="@/assets/images/bcnamerequest-laptop_x2.jpg"
        >
      </v-col>
      <v-col
        cols="12"
        md="6"
        lg="6"
        :class="{'pl-15' : !isMobile }"
      >
        <v-row>
          <v-col
            cols="12"
            class="h3 pb-5 mt-n5"
            :class="{'text-center' : isMobile }"
          >
            A new and better way to get a name <br>for your business in B.C.
          </v-col>
          <v-col cols="12">
            <ul>
              <li><span>Interactive help building a name</span></li>
              <li><span>Get alternatives when your name is not available</span></li>
              <li><span>Guidance picking the most appropriate business structure</span></li>
              <li><span>Know how long it will take to get results for your name request</span></li>
              <li><span>Self-serve options to help track and manage your name request</span></li>
            </ul>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Getter } from 'pinia-class'
import { useStore } from '@/store'

@Component
export default class NewAndBetterWay extends Vue {
  @Getter(useStore) isMobile!: boolean
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

#new-and-better-way {
  background-color: white;
  width: 100%;

  ul {
    li {
      list-style-type: circle;
      color: $app-md-blue;
      padding: 5px 0;

      span {
        color: $text;
      }
    }
  }
}
</style>
