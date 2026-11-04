<template>
  <div class="container mx-auto mt-5 px-6 lg:px-48">
    <div class="text-gray-800">
      <h2 class="mb-3 text-3xl font-bold">Welcome to Name X!</h2>
      <span
        >Canada's most modern, semi-automated way to examine business name
        requests. Automated indicators show you:</span
      >

      <div class="mb-5 ml-10 space-y-1">
        <div>
          <h2 class="text-xl font-semibold">Conflicts</h2>
          <p class="ml-6">
            Searches the name against related industry categories, synonyms,
            word substitutions (eg. 9 and nine), and more. The conflict search
            is only as good as the information in it, so if you don't see
            something come back in the search you should check the SOLR admin
            tool to see if it is in the correct industry category or other
            search options.
          </p>
        </div>

        <div>
          <h2 class="text-xl font-semibold">Condition</h2>
          <p class="ml-6">
            This gives you the messages to clients and internal information
            based on condition of words or phrases, eg. 'Doctor', 'BC', and
            such.
          </p>
        </div>

        <div>
          <h2 class="text-xl font-semibold">Trademarks</h2>
          <p class="ml-6">
            Searches the Canadian Trademarks database and shows you active
            trademarks related to the name request
          </p>
        </div>

        <div>
          <h2 class="text-xl font-semibold">History</h2>
          <p class="ml-6">
            If a similar name has been approved or rejected previously (use this
            to tell you if they are holding a name too long).
          </p>
        </div>
      </div>

      <StatusBox />
    </div>
  </div>
</template>

<script setup lang="ts">
useHead({ title: 'BC Registry: Name Examination - Home' })
</script>
