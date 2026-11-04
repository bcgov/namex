<template>
  <v-data-table
    id="advanced-search-results-table"
    :headers="getHeaders"
    :items="nameRequestResults"
    :items-per-page="1000"
    :custom-sort="sortTable"
    fixed-header
    height="20rem"
    hide-default-footer
  >
    <template #item="{ item }">
      <tr @click="setNrNum(item.nrNum)">
        <td class="copy-normal">
          {{ apiToDateString(item.submittedDate) }}
        </td>
        <td class="copy-normal">
          <span
            v-for="(name, index) in item.names"
            :key="`business-name-${index}`"
          >{{ name.name }}<br></span>
        </td>
        <td
          v-if="isApplicantNameSearch"
          class="copy-normal"
        >
          <span
            v-for="(applicant, index) in item.applicants"
            :key="`applicant-${index}`"
          >
            {{ applicant.lastName }}, {{ applicant.firstName }} {{ applicant.middleName }}
          </span>
        </td>
        <td>
          <v-btn class="button-text retrieve-nr-btn my-n3 pr-0">
            Retrieve
            <v-icon class="retrieve-nr-icon ml-3">
              mdi-chevron-right
            </v-icon>
          </v-btn>
        </td>
      </tr>
    </template>
  </v-data-table>
</template>

<script lang='ts'>
import { Component, Emit, Mixins, Prop, Watch } from 'vue-property-decorator'
import { Action } from 'pinia-class'
import { useStore } from '@/store'
import { ActionBindingIF } from '@/interfaces/store-interfaces'
import { DateMixin } from '@/mixins'
import { NameRequestI } from '@/interfaces'

@Component({})
export default class AdvancedSearchTable extends Mixins(DateMixin) {
  @Prop({ default: [] })
  readonly nameRequestResults

  @Prop({ default: false })
  readonly isApplicantNameSearch

  @Action(useStore) setExistingRequestSearch!: ActionBindingIF

  private headers: Array<any> = []

  /** Filter the headers we want to show. */
  private get getHeaders (): Array<any> {
    return this.headers.filter(x => x.show)
  }

  /** Sort the table by the specified column.
   * @param items An array of Name Request objects
   * @param columnValue The string value of the associated column. By Vuetify default always the first index.
   * @param isDesc A boolean indicated if sort is Asc or Desc.
   */
  private sortTable (items: Array<NameRequestI>, columnValue: Array<string>, isDesc: boolean): NameRequestI[] {
    // Sort by date
    if (columnValue[0] === 'date') {
      items.sort((a, b) => {
        if (!isDesc[0]) {
          return this.sortByDate(a.submittedDate, b.submittedDate)
        } else {
          return this.sortByDate(b.submittedDate, a.submittedDate)
        }
      })
    }

    // Sort by last name, first name AND date
    // Currently DISABLED in the header options until further refinement. ie last name in conjunction with date.
    if (columnValue[0] === 'applicantName') {
      items.sort((a, b) => {
        let lastNameA = a.applicants[0].lastName
        let lastNameB = b.applicants[0].lastName

        if (!isDesc[0]) {
          return lastNameA.localeCompare(lastNameB)
        } else {
          return lastNameB.localeCompare(lastNameA)
        }
      })
    }

    return items
  }

  /** Sort helper for Dates.
   * @param a Date A
   * @param b Date B
   * @return An integer
   */
  private sortByDate (a, b): number {
    const dateA = new Date(a).getTime()
    const dateB = new Date(b).getTime()
    return dateA > dateB ? 1 : -1
  }

  /** Apply data table headers dynamically to account for computed properties. */
  @Watch('isApplicantNameSearch', { immediate: true })
  private applyHeaders (): void {
    this.headers = [
      { text: 'Submitted Date', align: 'start', value: 'date', sortable: true, show: true },
      { text: 'Request Name(s)', value: 'businessName', sortable: false, show: true },
      { text: 'Applicant Name', value: 'applicantName', sortable: false, show: this.isApplicantNameSearch },
      { text: '', value: 'actions', sortable: false, show: true }
    ]
  }

  /** Set Name Request to store. */
  @Emit('selectNameRequest')
  private setNrNum (nrNum: string): void {
    this.setExistingRequestSearch({ key: 'nrNum', value: nrNum.toUpperCase() })
  }
}
</script>
<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';

#advanced-search-results-table {
  ::v-deep th {
    font-size: $px-14;
    font-weight: bold;
    color: $dk-text;
  }

  tbody {
    td:first-child {
      width: 10rem;
    }

    tr {
      background-color: $gray1;
      vertical-align: top;

      &:hover {
        cursor: pointer;
        background-color: $app-lt-blue !important;

        .retrieve-nr-icon {
          color: white;
          background-color: $app-blue !important;
        }
      }

      td {
        padding: 10px 16px;
        line-height: 1.125rem;
      }
    }
  }

  .retrieve-nr-btn {
    text-decoration: none;
    float: right;

    &:before {
      background-color: transparent !important;
    }

    .retrieve-nr-icon {
      font-size: 1.875rem;
      color: $app-blue;
      background-color: white;
      border-radius: 50%;
    }
  }
}

::v-deep .v-data-table > .v-data-table__wrapper > table > tbody > tr > td {
  font-size: $px-16;
  color: $text;
  line-height: 1.375rem;
}

// Override the default scroll bar to meet design requirements
/* width */
::v-deep ::-webkit-scrollbar {
  width: 10px;
}

/* Track */
::v-deep ::-webkit-scrollbar-track {
  margin-top: 47px;
  background: rgb(250,250,250);
}

/* Handle */
::v-deep ::-webkit-scrollbar-thumb {
  background: rgb(193,193,193);
  border-radius: 10px;
  height: 2rem;
}

/* Handle on hover */
::v-deep ::-webkit-scrollbar-thumb:hover {
  background: $gray6;
}
</style>
