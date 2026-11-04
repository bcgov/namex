<template>
  <v-col
    id="dummy-input-box"
    :cols="cols"
    :md="md"
  >
    <v-text-field
      filled
      disabled
      hide-details
      :label="label"
    />
  </v-col>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component({})
export default class DummyInputBox extends Vue {
  @Prop({ default: '12' }) readonly cols!: string
  @Prop({ default: '6' }) readonly md!: string
  @Prop({ default: 'Select an action first' }) readonly label!: string
}
</script>
