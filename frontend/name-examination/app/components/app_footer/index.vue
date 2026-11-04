<template>
  <footer
    id="app-footer"
    class="grid grid-cols-10 items-center min-h-[3.5rem] text-[0.94rem] px-[1rem] xl:px-[8rem]
           bg-bcgov-blue5 border-t-2 border-bcgov-gold5"
  >
    <!-- Navigation Links -->
    <nav class="col-span-7 flex justify-between">
      <ul class="p-0 list-none">
        <AppFooterNavLink
          v-for="(link, index) in links"
          :key="index"
          :text="link.text"
          :route="link.route"
          :target="link.target || '_blank'"
          :isLast="index === links.length - 1"
        />
      </ul>
    </nav>

    <!-- Version Number -->
    <aside class="col-span-3 flex justify-self-end justify-content-end">
      <span class="italic text-bcgov-gold5">A BC Online Application</span>
      <AppFooterVersionInfo />
    </aside>
  </footer>
</template>

<script setup lang="ts">
const links = [
  { text: 'Home', route: '/', target: '_self' },
  { text: 'Disclaimer', route: 'https://www2.gov.bc.ca/gov/content/home/disclaimer' },
  { text: 'Privacy', route: 'https://www2.gov.bc.ca/gov/content/home/privacy' },
  { text: 'Accessibility', route: 'https://www2.gov.bc.ca/gov/content/home/accessibility' },
  { text: 'Hours of Availability', route: 'https://www2.gov.bc.ca/gov/content?id=C41D8179671441B2BAA3BDDD3D89C9A9' },
  { text: 'Copyright', route: 'https://www2.gov.bc.ca/gov/content/home/copyright' }
]
</script>
