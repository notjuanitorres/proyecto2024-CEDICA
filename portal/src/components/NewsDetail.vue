<template>
  <article class="news-article box">
    <div v-if="loading" class="has-text-centered">
      <p>Cargando...</p>
    </div>
    <div v-else-if="error" class="has-text-danger has-text-centered">
      <p>Error: {{ error }}</p>
    </div>
    <div v-else>
      <!-- Breadcrumb -->
      <nav class="breadcrumb mb-4" aria-label="breadcrumbs">
        <ul>
          <li>
            <router-link to="/">Inicio</router-link>
          </li>
          <li>
            <router-link to="/noticias">Noticias</router-link>
          </li>
          <li class="is-active">
            <a href="#" aria-current="page">{{ article.title }}</a>
          </li>
        </ul>
      </nav>
      <button class="button is-link is-light mb-4" @click="$router.back()">
        ← Volver
      </button>
      <header>
        <h2 class="title is-3 has-text-black">{{ article.title }}</h2>
        <p class="subtitle is-6 has-text-grey">
          Publicado el {{ formatDate(article.publish_date) }} por {{ article.author }}
        </p>
      </header>
      <div class="content">
        <p v-html="article.content"></p>
      </div>
    </div>
  </article>
</template>

<script setup>
import { onMounted, defineProps } from 'vue';
import { useRouter } from 'vue-router';
import { useNewsStore } from '../stores/news.js';
import { storeToRefs } from 'pinia';

const props = defineProps({
  id: {
    type: [String, Number],
    required: true
  }
});

const router = useRouter();
const store = useNewsStore();
const { article, loading, error } = storeToRefs(store);

const fetchArticle = async () => {
  try {
    await store.fetchArticle(props.id);
  } catch (e) {
    console.error('Failed to fetch article:', e);
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
  fetchArticle();
});
</script>

<style scoped>
.news-article {
  padding: 1.5rem;
  background-color: #fff;
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.title {
  margin-bottom: 0.5rem;
}

.subtitle {
  margin-bottom: 1.5rem;
}
</style>
