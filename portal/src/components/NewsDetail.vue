<template>
  <div>
    <div v-if="loading">Cargando...</div>
    <div v-else-if="error">Error: {{ error }}</div>
    <div v-else>
      <h2 class="title">{{ article.title }}</h2>
      <p class="subtitle has-text-grey">
        Publicado el {{ formatDate(article.publish_date) }}
      </p>
      <div class="content">
        <p v-html="article.content"></p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.title {
  margin-bottom: 1rem;
}

.subtitle {
  margin-bottom: 2rem;
}
</style>

<script setup>
import { onMounted, defineProps } from 'vue';
import { useRouter } from 'vue-router';
import { useArticleStore } from '../stores/singleNews';
import { storeToRefs } from 'pinia';

const props = defineProps({
  id: {
    type: [String, Number],
    required: true
  }
});

const router = useRouter();
const store = useArticleStore();
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
