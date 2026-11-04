<template>
  <v-container
    id="lower-container"
    fluid
  >
    <!--- Build a Name Info Container -->
    <name-build-info />

    <new-and-better-way />

    <v-row
      no-gutters
      class="bg-grey-1 px-9 py-6 pt-14 content-container"
      justify="center"
    >
      <v-col
        cols="auto"
        class="h3 mt-9 mb-2"
      >
        Helpful Tips
      </v-col>
      <v-col cols="12">
        <v-row
          no-gutters
          justify="center"
          class="mb-5 pb-6"
        >
          <v-col
            cols="auto"
            class="my-4"
          >
            <v-container class="square-card">
              <v-row justify="center">
                <v-col
                  class="h5"
                  cols="auto"
                >
                  TRADEMARKS
                </v-col>
              </v-row>
              <v-row justify="center">
                <v-col cols="auto">
                  <img
                    src="@/assets/images/lc-tm-search-icon.png"
                    height="60"
                    width="60"
                  >
                </v-col>
              </v-row>
              <v-row justify="end">
                <v-col class="text-center copy-small">
                  See if your name may be in use outside of BC,
                  <a
                    href="https://ised-isde.canada.ca/cipo/trademark-search/srch"
                    target="_blank"
                  >
                    search for Canadian trademarked names.
                    <v-icon class="launch-icon">mdi-launch</v-icon>
                  </a>
                </v-col>
              </v-row>
            </v-container>
          </v-col>

          <v-col
            cols="auto"
            class="mx-7 my-4"
          >
            <v-container class="square-card">
              <v-row justify="center">
                <v-col
                  class="h5"
                  cols="auto"
                >
                  DOMAIN NAMES
                </v-col>
              </v-row>
              <v-row justify="center">
                <v-col cols="auto">
                  <img
                    src="@/assets/images/domainicon_x1.png"
                    height="60"
                    width="60"
                  >
                </v-col>
              </v-row>
              <v-row>
                <v-col class="text-center copy-small">
                  Before selecting your business<br>
                  name, consider checking<br>
                  available website domain names.
                </v-col>
              </v-row>
            </v-container>
          </v-col>

          <v-col
            cols="auto"
            class="my-4"
          >
            <v-container class="square-card">
              <v-row justify="center">
                <v-col
                  class="h5"
                  cols="auto"
                >
                  SOCIAL MEDIA
                </v-col>
              </v-row>
              <v-row justify="center">
                <v-col cols="auto">
                  <img
                    src="@/assets/images/socialicon_x1.png"
                    height="60"
                    width="60"
                  >
                </v-col>
              </v-row>
              <v-row>
                <v-col class="text-center copy-small">
                  Search social media sites to see<br>
                  which usernames may be available<br>
                  for your business.
                </v-col>
              </v-row>
            </v-container>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <div class="contact-section">
      <v-row
        no-gutters
        class="content-container"
      >
        <v-col
          cols="12"
          md="6"
          lg="6"
        >
          <v-container class="pa-9">
            <v-row>
              <v-col
                cols="12"
                class="h3 info-underline px-0"
              >
                Need more information?
              </v-col>
              <v-col
                cols="12"
                class="px-0"
              >
                <a
                  :href="needMoreInfo"
                  target="_blank"
                  class="white--text"
                >
                  Learn more about requesting a name
                </a>
              </v-col>
            </v-row>
          </v-container>
        </v-col>
        <v-col
          cols="12"
          md="6"
          lg="6"
        >
          <v-container class="pa-9">
            <v-row
              class="alinn align-items"
              align-content="start"
            >
              <v-col
                cols="12"
                class="h3 info-underline px-0"
              >
                Contact Us
              </v-col>
              <v-col
                cols="12"
                class="px-0"
              >
                For support or questions about this application contact us at:
              </v-col>
              <ul class="contact-info-list">
                <li>
                  Toll Free: <a
                    href="tel:1-877-370-1033"
                    class="white--text"
                  >1-877-370-1033</a>
                </li>
                <li>
                  Victoria Office: <a
                    href="tel:250-370-1033"
                    class="white--text"
                  >250-370-1033</a>
                </li>
                <li>
                  Email: <a
                    href="mailto:bcregistries@gov.bc.ca"
                    class="white--text"
                  >BCRegistries@gov.bc.ca</a>
                </li>
              </ul>
              <v-col
                cols="12"
                class="pb-0 px-0 font-weight-bold"
              >
                Hours of Operation:
              </v-col>
              <v-col
                cols="12"
                class="pt-0 px-0"
              >
                Monday to Friday, 9:00am - 4:00pm Pacific time
              </v-col>
            </v-row>
          </v-container>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script lang="ts">
import NameBuildInfo from '@/components/lower-info-area/name-build-info.vue'
import NewAndBetterWay from '@/components/lower-info-area/new-and-better-way.vue'
import { Component, Vue } from 'vue-property-decorator'

@Component({
  components: { NameBuildInfo, NewAndBetterWay }
})
export default class LowerContainer extends Vue {
  readonly needMoreInfo = 'https://www2.gov.bc.ca/gov/content/employment-business/business/managing-a-business/' +
    'permits-licences/businesses-incorporated-companies/approval-business-name'
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/theme.scss";

#lower-container {
  padding: 0;
  margin: 0;
  font-size: $px-16;
  color: $text;
  background-color: $gray1;

  .contact-section {
    background-color: $BCgovBlue5;
    color: white;

    .contact-info-list {
      margin: 0;
      padding: 0;
      list-style-type: none;
    }

    .info-underline {
      font-size: $px-20;
      border-bottom: 1px solid $BCgovBlue3;
      color: white;
    }
  }

  .square-card {
    height: 260px;
    width: 300px;
    padding: 15px;
    border-radius: 4px;
    background-color: white;
    box-shadow: 2px 2px 4px 0 darkgray; /* FUTURE: should be $border? */

    .launch-icon {
      display: inline-block;
      font-size: $px-14;
      color: $app-blue;
    }
  }
}
</style>
