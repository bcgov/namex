<template>
  <v-container
    id="name-build-info"
    class="content-container"
  >
    <v-row no-gutters>
      <v-col
        cols="12"
        class="h3 align"
      >
        How to Build Your Name
      </v-col>
      <v-col
        cols="12"
        md="6"
        lg="6"
        class="my-9"
      >
        <v-card
          class="my-9"
          flat
        >
          <v-list class="name-build-list">
            <v-list-item-group color="primary">
              <v-list-item
                v-for="(item, i) in items"
                :key="i"
                class="name-build-list-item"
                :class="{'name-build-list-item-active': isActiveTab(i)}"
                :ripple="false"
                @mouseover="itemIndex = i"
              >
                <v-icon
                  v-if="isActiveTab(i)"
                  color="primary"
                  left
                >
                  mdi-check-circle
                </v-icon>
                <v-icon
                  v-else
                  color="primary"
                  left
                >
                  mdi-check
                </v-icon>
                <v-list-item-content>
                  <v-list-item-title
                    class="name-build-list-item-title"
                    :class="{'name-build-list-item-active': isActiveTab(i)}"
                    v-html="item.title"
                  />
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>

          <div class="bg-light-gray pl-4">
            <p class="copy-small pt-7 mb-2">
              If you require consent from an existing business to use a name:
            </p>
            <a
              :href="consentLetterSampleUrl"
              target="_blank"
              class="link-std-sans-ul"
            >
              <v-icon color="primary">mdi-file-pdf-outline</v-icon>
              Download Sample Consent Letter
            </a>
          </div>
        </v-card>
      </v-col>
      <v-divider
        v-if="!isMobile"
        class="mt-9 divider"
        vertical
      />
      <v-col
        cols="12"
        md="6"
        lg="6"
        class="my-9 px-6"
      >
        <component
          :is="getDisplayedComponent(itemIndex)"
          :key="itemIndex"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Getter } from 'pinia-class'
import { useStore } from '@/store'
import { BusinessDesignation, ConsentWords, ExampleName, UnavailableWords, UniqueNames }
  from '@/components/lower-info-area/name-build-sub-components'

@Component({
  components: {
    BusinessDesignation,
    ConsentWords,
    ExampleName,
    UnavailableWords,
    UniqueNames
  }
})
export default class NameBuildInfo extends Vue {
  @Getter(useStore) isMobile!: boolean

  private itemIndex = 0
  readonly items = [
    {
      title: 'Check the name has the correct components',
      component: ExampleName
    },
    {
      title: 'Check for unavailable words',
      component: UnavailableWords
    },
    {
      title: 'Check for words that require consent',
      component: ConsentWords
    },
    {
      title: 'Check for similar names in the same sector',
      component: UniqueNames
    },
    {
      title: 'Check for appropriate designation',
      component: BusinessDesignation
    }
  ]

  readonly consentLetterSampleUrl = 'https://www2.gov.bc.ca/assets/gov/employment-business-and-economic-development/' +
    'business-management/permits-licences-and-registration/registries-other-assets/consent_letter_sample.pdf'

  /** Get the corresponding component for display */
  private getDisplayedComponent (index: number) {
    return this.items[index].component
  }

  /** Check if current tab is active */
  private isActiveTab (index: number) {
    return this.itemIndex === index
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

#name-build-info {
  min-height: 36rem;
  padding-top: 92px;

  .divider {
    max-height: 24rem;
    border-color: $border;
    margin-left: -1px;
    z-index: 1;
  }

  .name-build-list {
    background-color: $gray1;

    .name-build-list-item {
      border: solid rgba(0, 0, 0, 0.12);
      border-width: 1px 0 0 0;
    }
    .name-build-list-item:last-of-type {
      border: solid rgba(0, 0, 0, 0.12);
      border-width: 1px 0 1px 0;
    }

    .name-build-list-item:before {
      background-color: white;
    }
    .name-build-list-item-title {
      color: $app-blue;
      white-space: initial;
    }
    .name-build-list-item-active {
      color: $text;
      font-weight: bold;
      background-color: white;
    }
  }
}
</style>
