<script setup>
import NewsDetail from "@/components/NewsDetail.vue";
import { useRoute } from 'vue-router';

const route = useRoute();
</script>

<template>
  <main class="news-page">
    <section class="section">
      <div class="container">
        <h1 class="title has-text-centered mb-6">Detalles de la Noticia</h1>
        <div class="columns is-centered">
          <div class="column is-8">
            <NewsDetail :id="route.params.id" />
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.news-page {
  min-height: 100vh;
  padding-top: 2rem;
}

.section {
  padding: 2rem 1.5rem;
}

@media (min-width: 1024px) {
  .section {
    padding-top: 3rem;
  }
}
</style>
