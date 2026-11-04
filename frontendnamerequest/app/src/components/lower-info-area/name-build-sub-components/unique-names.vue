<template>
  <v-container
    id="unique-names"
    class="pb-0"
  >
    <h4>Choose a unique name for your business</h4>

    <p class="my-6 mb-0">
      Company names can not be too similar to existing names within the same "nature of business"
      sector. Here are examples of types of companies within the same sector;
    </p>
    <p class="my-6 mb-0">
      <strong>Construction:</strong> building; contracting; development; remodelling; renovation;
      restoration; structure; estate; land; listing; property; realty; real estate;
    </p>
    <p class="my-6 mb-0">
      <strong>Salon:</strong> barber; beauty; coiffure; cut; hair; hairstyling; style;
    </p>

    <v-divider class="ml-0 mb-4" />

    <v-row class="ml-1 mb-4">
      <h5>Similar name examples</h5>
    </v-row>

    <v-row class="ml-1 mb-4">
      <p class="mb-1">
        <v-icon
          color="red"
          left
          small
        >
          mdi-cancel
        </v-icon>
        <strong>Sarah's Contracting Ltd.</strong>
        is too similar to
        <strong>Sarah's Renovation Ltd.</strong>
      </p>
      <p class="mb-1">
        <v-icon
          color="green"
          left
          small
        >
          mdi-check
        </v-icon>
        <strong>Sarah's Contracting Ltd.</strong>
        is different from
        <strong>Sarah's Home Renovation Ltd.</strong>
      </p>
    </v-row>

    <v-row class="ml-1 mb-4">
      <p class="mb-1">
        <v-icon
          color="red"
          left
          small
        >
          mdi-cancel
        </v-icon>
        <strong>Westcoast Hair Salon Inc.</strong>
        is too similar to
        <strong>Westcoast Barbers Inc.</strong>
      </p>
      <p class="mb-1">
        <v-icon
          color="green"
          left
          small
        >
          mdi-check
        </v-icon>
        <strong>Westcoast Hair Salon Inc.</strong>
        is different from
        <strong>Westcoast Barbers Collective Inc.</strong>
      </p>
    </v-row>

    <v-divider class="ml-0 mb-4" />

    <v-row class="ml-1 mb-4">
      <a
        href="./pdfs/groupings_of_similar_descriptive_words.pdf"
        target="_blank"
        class="link-std-sans-ul"
      >
        <v-icon color="primary">mdi-file-pdf-outline</v-icon>
        Download Groupings of Similar Descriptive Words
      </a>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class UniqueNames extends Vue {}
</script>

<style scoped lang="scss">
@import '@/assets/styles/theme.scss';

#unique-names {
  p {
    font-size: $px-14;
  }
}
</style>
