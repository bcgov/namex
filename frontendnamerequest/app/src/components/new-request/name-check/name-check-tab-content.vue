<template>
  <v-row
    class="check-tab-content"
    justify="center"
    no-gutters
  >
    <v-col>
      <span class="check-tab-title">{{ title }}</span>
      <div
        v-if="loading"
        class="pt-2"
      >
        <v-progress-circular
          class="check-tab-spinner"
          indeterminate
          size="25"
          width="2"
        />
      </div>
      <v-row
        v-else
        justify="center"
        no-gutters
      >
        <v-col
          v-if="!isXproFlow"
          cols="auto"
        >
          <v-icon
            class="check-tab-icon pt-2"
            size="1.3rem"
          >
            {{ tabIcon }}
          </v-icon>
        </v-col>
        <v-col cols="auto">
          <p
            :class="contentClass"
            v-html="subtitle"
          >
            {{ subtitle }}
          </p>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>
<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { Getter } from 'pinia-class'
import { useStore } from '@/store'

@Component({})
export default class NameCheckTabContent extends Vue {
  @Getter(useStore) isXproFlow!: boolean

  @Prop({ default: true }) readonly loading!: boolean
  @Prop() readonly subtitle!: string
  @Prop() readonly tabIcon!: string
  @Prop() readonly title!: string

  get contentClass (): string {
    const baseClasses = 'check-tab-sub-title pt-2 pb-7'
    if (this.isXproFlow) return baseClasses
    if (this.noConflicts) return baseClasses + ' no-text-decoration pl-1'
    return baseClasses + ' pl-2'
  }
  get noConflicts (): boolean {
    return this.subtitle === 'OK'
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';
.active-tab .check-tab-icon {
  color: $app-blue;
}
.active-tab .check-tab-spinner {
  color: $app-blue;
}
.active-tab .check-tab-sub-title {
  color: $gray7;
  text-decoration: none;
}
.active-tab .check-tab-title {
  color: $gray9;
}
.check-tab-content {
  height: 80px;
}
.check-tab-icon {
  color: white;
  background-color: transparent;
}
.check-tab-spinner {
  color: white
}
.check-tab-sub-title {
  color: white;
  font-size: $px-16 !important;
  font-weight: normal;
  letter-spacing: normal !important;
  margin: 0 !important;
  text-decoration: underline;
}
.check-tab-title {
  color: white;
  font-size: $px-18 !important;
  font-weight: bold;
  letter-spacing: normal !important;
  margin: 0 !important;
}
.no-text-decoration {
  text-decoration: none !important;
}
</style>
