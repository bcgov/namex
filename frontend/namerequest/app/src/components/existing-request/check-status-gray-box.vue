<template>
  <v-row
    no-gutters
    class="bg-light-gray"
  >
    <v-col class="text-body-4 px-5 py-4">
      <p>
        To check on the status of this Name Request in the future, enter the request number
        <strong>{{ nrNum }}</strong> plus the Applicant Phone Number or Email Address using the "Manage My Name
        Request tab" on the site.
      </p>
      <v-row no-gutters>
        <v-col
          cols="auto"
          class="pt-1 mr-2"
        >
          <v-icon color="caution">
            mdi-alert
          </v-icon>
        </v-col>
        <v-col
          cols="11"
          class="pt-1 pb-1 no-gutters"
        >
          <strong>Important:</strong> Name Requests expire. If a Name Request is approved, it is reserved for
          56 days from the date of approval. Be sure to use the Name Request before your name reservation
          expires. If it expires, you will need to submit a new Name Request ($30.00 fee) as the name will once
          again be available to the public.
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component({})
export default class CheckStatusGrayBox extends Vue {
  @Prop({ default: 'TBD' })
  readonly nrNum: string
}
</script>
