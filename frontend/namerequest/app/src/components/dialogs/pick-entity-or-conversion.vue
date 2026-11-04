<template>
  <v-dialog
    :value="getPickEntityModalVisible"
    :max-width="maxWidth"
    persistent
  >
    <v-card class="no-border pick-entity-card">
      <v-row>
        <v-col cols="10">
          <span
            v-if="!showSocietiesInfo"
            class="copy-small"
          >{{ getLocationText }}</span>
        </v-col>
        <v-col cols="2">
          <v-icon
            class="float-right"
            md
            color="primary"
            @click="closeIconClicked()"
          >
            mdi-close
          </v-icon>
        </v-col>
      </v-row>

      <template v-if="isConversion">
        <v-card-text>
          <v-container>
            <v-row class="category-bg">
              <v-col
                cols="12"
                class="font-weight-bold"
              >
                Alterations
              </v-col>
            </v-row>
            <v-row
              v-for="(conversion, i) in ConversionTypes"
              :key="`conv-${i}`"
            >
              <v-col
                :id="conversion.value"
                cols="12"
                class="clickable-cell"
                @click="chooseConversion(conversion)"
              >
                <v-tooltip
                  bottom
                  content-class="bottom-tooltip"
                  transition="fade-transition"
                  :disabled="isMobile"
                >
                  <template #activator="scope">
                    <button
                      class="link-sm-sans-ul entity-link"
                      v-on="scope.on"
                    >
                      {{ conversion.desc }}
                    </button>
                  </template>
                  <div
                    v-for="(blurb, j) in entityBlurbs(conversion.value)"
                    :key="`blurb-${j}`"
                  >
                    <span>{{ blurb }}</span>
                  </div>
                </v-tooltip>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </template>

      <!-- Special case for societies -->
      <template v-if="showSocietiesInfo">
        <v-card-text class="mt-n12">
          <v-container fluid>
            <v-row
              no-gutters
              class="text-center"
            >
              <v-col cols="12">
                To request a name for a Society
              </v-col>
              <v-col cols="12">
                please use the Societies Online website
              </v-col>
              <v-col cols="12">
                <a href="https://www.bcregistry.ca/societies/">https://www.bcregistry.ca/societies/</a>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </template>

      <!-- Category tables -->
      <template v-else>
        <v-card-text class="pt-4">
          <v-row no-gutters>
            <v-col
              v-for="(category, i) in tableData"
              :key="`cat-${i}`"
            >
              <v-simple-table>
                <tr class="category-bg cell">
                  <th>
                    <span class="font-weight-bold">{{ category.text }}</span>
                  </th>
                </tr>
                <tr
                  v-for="(entity, n) in category.entities"
                  :key="`ent-${n}`"
                >
                  <td
                    :id="entity.value"
                    class="clickable-cell"
                    @click="chooseType(entity)"
                  >
                    <v-tooltip
                      bottom
                      content-class="bottom-tooltip"
                      transition="fade-transition"
                      :disabled="isMobile"
                    >
                      <template #activator="scope">
                        <button
                          class="link-sm-sans-ul entity-link"
                          v-on="scope.on"
                        >
                          {{ entity.text }}
                        </button>
                      </template>
                      <div
                        v-for="(blurb, index) in entityBlurbs(entity.value)"
                        :key="`blurb-${index}`"
                      >
                        <span :class="{ 'tooltip-bullet': index !== 0}">{{ blurb }}</span>
                      </div>
                    </v-tooltip>
                  </td>
                </tr>
              </v-simple-table>
            </v-col>
          </v-row>
        </v-card-text>
      </template>

      <!-- Category tables - xpro (amalgamation only) -->
      <template v-if="isAmalgamation && !showSocietiesInfo">
        <v-row class="pt-4">
          <v-col cols="12">
            <span class="copy-small">Extraprovincial:</span>
          </v-col>
        </v-row>

        <v-card-text class="pt-4">
          <v-row no-gutters>
            <v-col
              v-for="(category, i) in tableDataXPRO"
              :key="`cat-xpro-${i}`"
            >
              <v-simple-table>
                <tr class="category-bg cell">
                  <th>
                    <span class="font-weight-bold">{{ category.text }}</span>
                  </th>
                </tr>
                <tr
                  v-for="(entity, n) in category.entities"
                  :key="`ent-xpro-${n}`"
                >
                  <td
                    :id="entity.value"
                    class="clickable-cell"
                    @click="chooseType(entity)"
                  >
                    <v-tooltip
                      bottom
                      content-class="bottom-tooltip"
                      transition="fade-transition"
                      :disabled="isMobile"
                    >
                      <template #activator="scope">
                        <button
                          class="link-sm-sans-ul entity-link"
                          v-on="scope.on"
                        >
                          {{ entity.text }}
                        </button>
                      </template>
                      <div
                        v-for="(blurb, index) in entityBlurbs(entity.value)"
                        :key="`blurb-xpro-${index}`"
                      >
                        <span :class="{ 'tooltip-bullet': index !== 0}">{{ blurb }}</span>
                      </div>
                    </v-tooltip>
                  </td>
                </tr>
              </v-simple-table>
            </v-col>
          </v-row>
        </v-card-text>
      </template>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Watch } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import { ConversionTypesI, EntityI, SelectOptionsI } from '@/interfaces'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { EntityTypes, Location } from '@/enums'
import { ConversionTypes } from '@/list-data'
import { CommonMixin } from '@/mixins'

@Component({})
export default class PickEntityOrConversionDialog extends CommonMixin {
  // enum for template
  readonly ConversionTypes = ConversionTypes

  @Getter(useStore) getConversionTypeOptions!: ConversionTypesI[]
  @Getter(useStore) getEntityBlurbs!: Array<EntityI | ConversionTypesI>
  @Getter(useStore) getEntityTypeOptions!: Array<EntityI>
  @Getter(useStore) getEntityTypesBC!: Array<EntityI>
  @Getter(useStore) getEntityTypesXPRO!: Array<EntityI>
  @Getter(useStore) getLocation!: Location
  @Getter(useStore) getLocationText!: string
  @Getter(useStore) getPickEntityModalVisible!: boolean
  @Getter(useStore) isAmalgamation!: boolean
  @Getter(useStore) isConversion!: boolean
  @Getter(useStore) isMobile!: boolean

  @Action(useStore) setConversionType!: ActionBindingIF
  @Action(useStore) setConversionTypeAddToSelect!: ActionBindingIF
  @Action(useStore) setEntityTypeCd!: ActionBindingIF
  @Action(useStore) setEntityTypeAddToSelect!: ActionBindingIF
  @Action(useStore) setPickEntityModalVisible!: ActionBindingIF

  showSocietiesInfo = false

  closeIconClicked () {
    this.setPickEntityModalVisible(false)
    // clear empty string selection
    this.setEntityTypeCd(null)
  }

  @Watch('getPickEntityModalVisible')
  handleModalClose (newVal: boolean) {
    if (!newVal) {
      setTimeout(() => { this.showSocietiesInfo = false }, 500)
    }
  }

  get tableData (): any[] {
    // default table data for amalgamation is always BC
    if (this.getLocation === Location.BC || this.isAmalgamation) {
      return this.tableDataBC
    } else {
      return this.tableDataXPRO
    }
  }

  get tableDataBC (): any[] {
    let categories = []
    for (let type of this.getEntityTypesBC) {
      let i = categories.indexOf(type.cat)
      if (i === -1) {
        categories.push(type.cat)
      }
    }
    const getEntities = (category) => {
      return this.getEntityTypesBC.filter(type => type.cat === category)
    }
    let output = categories.map(cat =>
      ({
        text: cat,
        entities: getEntities(cat)
      })
    )
    return output
  }

  get tableDataXPRO (): any[] {
    let categories = []
    for (let type of this.getEntityTypesXPRO) {
      let i = categories.indexOf(type.cat)
      if (i === -1) {
        categories.push(type.cat)
      }
    }
    const getEntities = (category) => {
      return this.getEntityTypesXPRO.filter(type => type.cat === category)
    }
    let output = categories.map(cat =>
      ({
        text: cat,
        entities: getEntities(cat)
      })
    )
    return output
  }

  get maxWidth (): string {
    if (this.showSocietiesInfo || this.isConversion || this.isAmalgamation) {
      return '550px'
    }

    // 210 per column with a max threshold of 960px (sm)
    const cols = this.tableData.length
    const maxThreshold = this.$vuetify.breakpoint.thresholds.sm
    const val = (210 * cols > maxThreshold) ? maxThreshold : (210 * cols)
    return `${val}px`
  }

  // FUTURE: clean up return type
  entityBlurbs (entity_type_cd: string): string[][] | string[] | string {
    return this.getEntityBlurbs.find(type => type.value === entity_type_cd)?.blurbs || []
  }

  chooseConversion (conversion) {
    let index = this.getConversionTypeOptions.findIndex((conv: any) => conv.value === conversion.value)
    if (index === -1) {
      this.setConversionTypeAddToSelect(conversion)
    }
    // special case for sub-menu
    if (conversion.value !== 'INFO') {
      this.setEntityTypeCd(conversion.entity_type_cd)
    }
    this.setConversionType(conversion.value)
    this.setPickEntityModalVisible(false)
  }

  chooseType (entity: SelectOptionsI) {
    // special case for Society: if FF is not enabled then show society info panel and don't set the type
    if (!this.isSocietyEnabled() && (entity.value === EntityTypes.SO || entity.value === EntityTypes.XSO)) {
      this.showSocietiesInfo = true
      return
    }
    // if not already there, save selected entry for later addition to menu list
    let index = this.getEntityTypeOptions.findIndex((ent: any) => ent.value === entity.value)
    if (index === -1) {
      this.setEntityTypeAddToSelect(entity)
    }
    this.setEntityTypeCd(entity.value)
    this.setPickEntityModalVisible(false)
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';

.v-data-table {
  margin: 0 -3px;
}

.category-bg {
  background-color: $gray1;
}

.cell {
  padding: 10px;
  color: $dk-text;
  display: flex;
}

.entity-link {
  width: 100%;
  text-decoration: none;
  text-align: left;
}

.clickable-cell {
  min-width: 180px;
  width: 100%;
  padding: 10px;

  &:hover {
    background-color: $app-lt-blue;
    cursor: pointer;
  }
}

.no-border {
  border-radius: 0 !important;
  text-decoration: none !important;
}

::v-deep .v-data-table__wrapper {
  overflow-x: hidden;
}
</style>
