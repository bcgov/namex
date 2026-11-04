<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <AppBanner />
    <GlobalErrorDialog />
    <main class="flex-grow">
      <slot></slot>
    </main>
    <AppFooter />
  </div>
</template>