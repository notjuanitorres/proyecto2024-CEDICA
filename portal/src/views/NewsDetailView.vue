<script setup>
import NewsDetail from "@/components/NewsDetail.vue";
import { useRoute } from 'vue-router';

const route = useRoute();
</script>

<template>
  <main>
    <section class="news-section has-navbar-fixed-top">
      <div class="container px-4 py-6">
        <h1 class="title is-1 mb-6">Noticia</h1>
        <NewsDetail :id="route.params.id" />
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
