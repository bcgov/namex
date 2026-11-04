<template>
  <v-container id="unavailable-words">
    <h4>Words that can not be used by the public</h4>

    <v-list class="unavailable-words-list">
      <v-row>
        <v-col
          cols="12"
          sm="6"
        >
          <v-list-item
            v-for="(item, i) in listItems1"
            :key="'list1-' + i"
            class="unavailable-words-list-item"
          >
            <p
              class="mb-0"
              v-html="item"
            />
          </v-list-item>
        </v-col>
        <v-col
          cols="12"
          sm="6"
        >
          <v-list-item
            v-for="(item, i) in listItems2"
            :key="'list2-' + i"
            class="unavailable-words-list-item"
          >
            <p
              class="mb-0"
              v-html="item"
            />
          </v-list-item>
        </v-col>
      </v-row>
    </v-list>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class UnavailableWords extends Vue {
  private listItems1 = ['Access BC', 'Authorized', 'Bankrupt', 'BC Tech', 'BC Online', 'Better Business Bureau',
    'Bonded', 'Build BC', 'Canadian National', 'Canada Standard', 'Certified', 'Council', 'CPIC']
  private listItems2 = ['Credit Union', 'Farmers Institute', 'GST', 'Guarantee', 'ICPO / Interpol', 'LLB',
    'Post Office', 'RCMP', 'Road Star', 'Savings and Loans', 'VSE', 'White Knight']
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/theme.scss';

#unavailable-words {
  p {
    font-size: $px-14;
  }

  .unavailable-words-list {
    background: inherit;

    .unavailable-words-list-item {
      color: $text;
      font-size: $px-14;
      letter-spacing: 0;
      line-height: 22px;
      min-height: 0 !important;
      padding-left: 0;
    }
  }
}
</style>
