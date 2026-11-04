<template>
  <div
    class="contact-info"
    :class="{ 'flex-column': direction === 'col' }"
  >
    <div
      v-for="(contact, i) in contactsToShow"
      :key="i"
      class="contact-container"
      :class="{ 'justify-center': direction === 'row' }"
    >
      <v-icon class="contact-icon">
        {{ contact.icon }}
      </v-icon>
      <div
        class="contact-key"
        v-html="contact.key"
      />
      <a
        :href="contact.href"
        class="contact-value"
        v-html="contact.val"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component({})
export default class ContactInfo extends Vue {
  /** Can be "row" (default) or "col". */
  @Prop({ default: 'row' })
  readonly direction: string

  /** If true, display help desk contact numbers, otherwise display BC Registries staff contact numbers. */
  @Prop({ default: true })
  readonly isHelpDesk: boolean

  get contactsToShow () {
    const phoneContacts = this.isHelpDesk
      ? [
        {
          icon: 'mdi-phone',
          key: 'Canada and U.S. Toll Free:',
          val: '1-877-370-1033',
          href: 'tel:+1-877-370-1033'
        },
        {
          icon: 'mdi-phone',
          key: 'Victoria Office:',
          val: '250-370-1033',
          href: 'tel:+1-250-370-1033'
        }
      ]
      : [
        {
          icon: 'mdi-phone',
          key: 'Canada and U.S. Toll Free:',
          val: '1-877-526-1526',
          href: 'tel:+1-877-526-1526'
        },
        {
          icon: 'mdi-phone',
          key: 'Victoria Office:',
          val: '250-387-7848',
          href: 'tel:+1-250-387-7848'
        }
      ]

    return [
      ...phoneContacts,
      {
        icon: 'mdi-email',
        key: 'Email:',
        val: 'BCRegistries@gov.bc.ca',
        href: 'mailto:BCRegistries@gov.bc.ca'
      }
    ]
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/theme";

.contact-info {
  display: flex;
  justify-content: space-between;
  row-gap: 0.25rem; /* in case direction = row */
}

.contact-container {
  display: flex;
  flex-wrap: wrap;
  column-gap: 0.5rem;
  min-width: 12rem;
}

.contact-icon {
  font-size: $px-20;
  color: $non-clickable-blue;
}

.contact-key {
  white-space: nowrap;
}

.contact-value {
  white-space: nowrap;
  align-self: center;
}
</style>
