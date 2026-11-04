<template>
  <v-container id="example-name">
    <v-row>
      <v-col
        cols="12"
        md="5"
        lg="5"
        class="mx-3"
      >
        <v-row justify="center">
          <img
            src="@/assets/images/Sarahsx1.png"
            class="name-img"
          >
        </v-row>
        <v-row
          align="center"
          justify="center"
        >
          <div class="text-divider" />
        </v-row>
        <v-row justify="center">
          <p class="text-content">
            Use unique words that will set you apart such as: <br>
            an individual's name; <br>
            a geographical location; <br>
            a coined, made-up word; <br>
            or an acronym.
          </p>
        </v-row>
      </v-col>
      <v-col
        cols="12"
        md="5"
        lg="5"
        class="mx-3"
      >
        <v-row justify="center">
          <img
            src="@/assets/images/Constructionx1.png"
            class="name-img"
          >
        </v-row>
        <v-row
          align="center"
          justify="center"
        >
          <div class="text-divider" />
        </v-row>
        <v-row justify="center">
          <p class="text-content">
            The second part of your name describes the "nature of your business".
            What is the service that your business is offering to the public?
          </p>
        </v-row>
      </v-col>
    </v-row>

    <v-divider class="ml-0 my-4" />

    <v-row class="ml-0">
      <h5>Improper name examples</h5>
    </v-row>
    <v-row>
      <v-col
        cols="12"
        sm="6"
      >
        <p>
          <v-icon
            color="red"
            left
          >
            mdi-cancel
          </v-icon>Construction Renovation
        </p>
      </v-col>
      <v-col
        cols="12"
        sm="6"
      >
        <p>
          <v-icon
            color="red"
            left
          >
            mdi-cancel
          </v-icon>Renovation Development
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class ExampleName extends Vue {}
</script>

<style scoped lang="scss">
@import "@/assets/styles/base.scss";

#example-name {
  p {
    font-size: $px-14;
    margin-bottom: 0;
  }

  @media (max-width: 1299px) {
    .name-img {
      height: 50px;
    }
  }

  .text-content {
    text-align: center;
  }
  .text-divider {
    border-left: 1px solid $border;
    height: 2rem;
  }
}
</style>
