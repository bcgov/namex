<template>
  <v-container id="business-designation">
    <h4>Include a designation based on the type of business</h4>

    <v-list class="business-designation-list">
      <v-row>
        <v-col
          cols="12"
          sm="6"
        >
          <v-list-item-group color="primary">
            <v-list-item
              v-for="(item, i) in items"
              :key="i"
              class="business-designation-list-item py-0"
              :ripple="false"
              @mouseover="itemIndex = i"
            >
              <v-list-item-content class="py-2">
                <v-list-item-title
                  class="business-designation-list-item-title py-0"
                  :class="{ 'business-designation-list-item-title-active': isActiveTab(i) }"
                  v-html="item.title"
                />
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-col>
        <v-col
          cols="12"
          sm="6"
        >
          <p>{{ items[itemIndex].content }}</p>
        </v-col>
      </v-row>
    </v-list>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class BusinessDesignation extends Vue {
  private itemIndex = 0
  private items = [
    {
      title: 'Incorporated Companies',
      content: `Incorporated companies must have as the last word in the name, the corporate designation, "Limited",
      "Limitee", "Incorporated", "Incorporee" or "corporation".  For all purposes using the abbreviations of these
      words (e.g. "Ltd.", "Ltee.", "Inc." or "Corp.") is acceptable`
    },
    {
      title: 'Extraprovincial Companies',
      content: `Extraprovincial companies may have "Limited Liability Company" or "LLC" as the last word in their
      name.`
    },
    {
      title: 'Partnerships and Sole Proprietorship',
      content: `Business names for partnerships and proprietorship cannot use "Ltd.", "Inc." or "Corp." at the end of
      their names, but they may use "Company" or "Co.".`
    },
    {
      title: 'Limited Partnerships',
      content: `Business  names for limited partnerships must use "Limited Partnership" at the end of the name.`
    },
    {
      title: 'Limited Liability Partnerships',
      content: `Business names for limited liability partnerships must use "Limited Liability Partnership" or "LLP," at
      the end of the name.`
    },
    {
      title: 'Societies',
      content: `Societies should have the designation "Society" or "Association" as the last word in their name.
      Companies are precluded from the use of these words in their names.`
    },
    {
      title: 'Cooperatives',
      content: `Cooperatives must use the word "Cooperative" or "Co-operative" or "Coop" or "Co-op" within the name.`
    },
    {
      title: 'Unlimited Liability Companies',
      content: `Unlimited Liability Companies must have "Unlimited Liability Company" or the abbreviation "ULC" at the
      end of its name.`
    }
  ]

  /** Check if current tab is active */
  private isActiveTab (index: number): boolean {
    return (this.itemIndex === index)
  }
}
</script>

<style scoped lang="scss">
  @import '@/assets/styles/theme.scss';

  #business-designation {
    p {
      font-size: $px-14;
      margin-bottom: 0;
    }

    .business-designation-list {
      background: inherit;

      .business-designation-list-item {
        color: $text;
        font-size: $px-14;
        letter-spacing: 0;
        line-height: 22px;
        min-height: 0 !important;
        padding-left: 0;
      }

      .business-designation-list-item:before {
        background: white;
      }

      .business-designation-list-item-title {
        font-size: $px-14;
        color: $app-blue;
        margin-bottom: 0;
        text-decoration: underline;
      }

      .business-designation-list-item-title-active {
        font-weight: bolder;
        text-decoration: none;
      }
    }
  }
</style>
