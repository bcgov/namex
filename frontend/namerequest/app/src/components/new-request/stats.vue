<template>
  <v-container
    class="mt-1"
    fluid
  >
    <v-row
      class="stats-v-row"
      no-gutters
    >
      <v-col
        v-if="!isMobile"
        cols="4"
      />
      <v-col
        cols="6"
        md="4"
        lg="4"
        class="pr-4"
      >
        <v-tooltip
          bottom
          nudge-left="45"
          content-class="bottom-tooltip wait-time-tooltip"
          transition="fade-transition"
          :disabled="isMobile || !showPriorityTooltip"
        >
          <template #activator="{ on }">
            <div
              class="stats-content-outer py-0"
              :class="{'float-right': !isMobile}"
              v-on="on"
            >
              <div class="stats-content-inner-1 pa-1 text-center">
                <div class="stats-value h3-lt">
                  {{ getPriorityWaitTime }}
                </div>
                <div class="stats-unit">
                  Days
                </div>
              </div>
              <div class="stats-content-inner-2">
                <span :class="{'dotted-underline': !isMobile}">Priority Request</span><br>
                <span :class="{'dotted-underline': !isMobile}">Wait Time</span>
              </div>
            </div>
          </template>
          <span>
            If you need your name reviewed as quickly as possible,
            Priority requests are available for a fee ($100.00).
            Priority name requests are usually reviewed within {{ getPriorityWaitTime }} business days.
          </span>
        </v-tooltip>
      </v-col>
      <v-col
        cols="6"
        md="4"
        lg="4"
      >
        <v-tooltip
          bottom
          nudge-left="45"
          content-class="bottom-tooltip new-submission-wait-time-tooltip"
          transition="fade-transition"
          :disabled="isMobile || !showRegularTooltip"
        >
          <template #activator="{ on }">
            <div
              id="stats-content-outer-3"
              :class="[{'float-right': !isMobile}, 'stats-content-outer py-0']"
              v-on="on"
            >
              <div class="stats-content-inner-1 pa-1 text-center">
                <div class="stats-value h3-lt">
                  {{ getRegularWaitTime }}
                </div>
                <div class="stats-unit">
                  Days
                </div>
              </div>
              <div class="stats-content-inner-2">
                <span :class="{'dotted-underline': !isMobile}">New Submission</span><br>
                <span :class="{'dotted-underline': !isMobile}">Wait Time</span>
              </div>
            </div>
          </template>
          <span>
            This is the estimated review wait time when submitting a new name request
            <strong>today</strong>. Wait times are approximate and subject to change.
          </span>
        </v-tooltip>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { Action, Getter } from 'pinia-class'
import { useStore } from '@/store'
import { StatsI } from '@/interfaces'
import { GetFeatureFlag } from '@/plugins'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import NamexServices from '@/services/namex-services'

@Component({})
export default class Stats extends Vue {
  @Getter(useStore) getStats!: StatsI
  @Getter(useStore) isMobile!: boolean
  @Getter(useStore) getRegularWaitTime!: string | number
  @Getter(useStore) getPriorityWaitTime!: string | number

  @Action(useStore) setStats!: ActionBindingIF

  async created (): Promise<void> {
    if (
    /*
     * Feature-flag semantics for hardcoded_*_wait_time:
     * - flag > 0 : use the flag value (explicit positive wait time).
     * - flag === 0 OR FF disabled: fall back to backend stats.
     * - flag < 0 : flag indicates the wait time is disabled.
     */
      GetFeatureFlag('hardcoded_regular_wait_time') === 0 ||
      GetFeatureFlag('hardcoded_priority_wait_time') === 0
    ) {
      try {
        const stats = await NamexServices.fetchStats()
        console.info('[stats] fetched stats', stats)
        if (stats) this.setStats(stats)
      } catch (error) {
        console.error('Error fetching stats:', error)
      }
    }
  }

  get autoApprovedCount (): string | number {
    return (this.getStats?.auto_approved_count ?? '-')
  }

  get showRegularTooltip (): boolean {
    const val = Number(this.getRegularWaitTime)
    return Number.isFinite(val) && val > 0
  }

  get showPriorityTooltip (): boolean {
    const val = Number(this.getPriorityWaitTime)
    return Number.isFinite(val) && val > 0
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';

.stats-content-inner-1 {
  width: 68px;
  display: inline-block;
  min-height: 70px;
}

.stats-content-inner-2 {
  white-space: nowrap;
  padding-left: 8px;
  font-size: $px-12;
  line-height: 18px;
}

.stats-content-outer {
  width: fit-content;
  background: url('@/assets/images/stats-circle.png');
  background-repeat: no-repeat;
  display: flex;
  align-items: center;

  &:hover {
    cursor: default;
  }
}

.stats-unit {
  display: block;
  position: relative;
  top: -8px;
  font-size: $px-12;
  font-weight: bold;
}

.stats-value {
  display: block;
  margin: 0;
  padding: 0;
  font-size: $px-24;
  font-weight: bold;
}

.wait-time-tooltip {
  text-align: left;
  width: 270px !important;
}

.new-submission-wait-time-tooltip {
  text-align: left;
  width: 270px !important;
}
</style>
