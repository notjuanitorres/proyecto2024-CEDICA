<template>
  <div class="recent-news-widget">
    <h3 class="title has-text-centered is-4">Noticias Recientes</h3>

    <div v-if="loading" class="has-text-centered my-4">
      <div class="button is-loading is-white"></div>
    </div>
    <div v-if="!loading && recentNews.length">
      <div class="columns is-multiline">
        <div v-for="article in recentNews" :key="article.id" class="column is-12">
          <div class="card">
            <div class="card-content">
              <div class="media">
                <div class="media-content">
                  <p class="title is-5">{{ article.title }}</p>
                  <p class="subtitle is-6">{{ article.author }}</p>
                </div>
              </div>
              <div class="content">
                {{ article.summary }}
                <br>
                <time :datetime="article.published_at" class="is-size-7 has-text-grey">
                  Publicado el {{ formatDate(article.published_at) }}
                </time>
              </div>
              <div class="card-footer">
                <router-link
                  :to="`/noticia/${article.id}`"
                  class="card-footer-item button is-primary is-light"
                >
                  Leer más
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="has-text-centered mt-5">
        <router-link to="/noticias/" class="button is-link is-outlined is-medium">
          <span class="icon">
            <i class="fas fa-arrow-right"></i>
          </span>
          <span>Leer más noticias</span>
        </router-link>
      </div>
    </div>
    <div v-else-if="!loading && !recentNews.length" class="has-text-centered">
      <p>No hay noticias recientes disponibles.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useNewsStore } from '../stores/news';
import { storeToRefs } from 'pinia';

const store = useNewsStore();
const { news, loading } = storeToRefs(store);

const recentNews = ref([]);

const fetchRecentNews = async () => {
  try {
    await store.fetchNews({ page: 1, per_page: 3 });
    recentNews.value = news.value.slice(0, 3); // Take only the first 3 items
  } catch (error) {
    console.error('Error fetching recent news:', error);
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

onMounted(() => {
  fetchRecentNews();
});
</script>

<style scoped>
.recent-news-widget {
  margin-top: 1.5rem;
}

.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>
