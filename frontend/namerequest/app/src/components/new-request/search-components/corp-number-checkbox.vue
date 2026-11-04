<template>
  <div id="corp-number-checkbox">
    <v-tooltip
      top
      min-width="390"
      content-class="top-tooltip"
      transition="fade-transition"
      :disabled="isMobile"
    >
      <template #activator="{ on }">
        <v-checkbox
          id="corp-num-checkbox"
          #label
          v-model="noCorpNum"
          class="copy-small mt-0 pt-0"
          hide-details
          v-on="on"
        >
          <span
            class="copy-small"
            v-on="on"
          >I don't have a corporate number</span>
        </v-checkbox>
      </template>

      <p>
        If you don't have or don't know the corporation number of the business, enter the full legal name
        of the business in its home jurisdiction.
      </p>

      <p>
        Note: If the home jurisdiction requires a name reservation, you may want to complete a name search
        in the home jurisdiction first to ensure that the name is available and then return to BC.
      </p>
    </v-tooltip>
  </div>
</template>

<script lang="ts">
import { Component, Mixins } from 'vue-property-decorator'
import NestedSelect from '@/components/common/nested-select.vue'
import { SearchMixin } from '@/mixins'

@Component({
  components: { NestedSelect }
})
export default class CorpNumberCheckbox extends Mixins(SearchMixin) {
  get noCorpNum (): boolean {
    return this.getHasNoCorpNum
  }

  set noCorpNum (value: boolean) {
    this.setNoCorpNum(value)
  }
}
</script>
