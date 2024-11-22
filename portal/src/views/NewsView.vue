<script setup>
import NewsWidget from "@/components/NewsWidget.vue";
</script>

<template>
  <main>
    <section class="news-section has-navbar-fixed-top">
      <div class="container px-4 py-6">
        <h1 class="title is-1 mb-6">Noticias</h1>
        <NewsWidget />
      </div>
    </section>
  </main>
</template>

<style scoped>
.news-section {
  min-height: 100vh;
  padding-top: 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

@media (min-width: 1024px) {
  .news-section {
    padding-top: 3rem;
  }
}
</style>
