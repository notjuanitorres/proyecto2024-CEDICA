<template>
  <div class="container">
    <!-- Breadcrumb (unchanged) -->
    <nav class="breadcrumb mb-4" aria-label="breadcrumbs">
      <ul>
        <li>
          <router-link to="/">Inicio</router-link>
        </li>
        <li class="is-active">
          <a href="#">Noticias</a>
        </li>
      </ul>
    </nav>

    <!-- Header and Search Section -->
    <div class="section pt-4 pb-5">
      <!-- Filters -->
      <div class="box">
        <div class="columns is-multiline">
          <!-- Author Search -->
          <div class="column is-4">
            <div class="field">
              <label class="label">Autor</label>
              <div class="control has-icons-left">
                <input
                  class="input"
                  type="text"
                  v-model="filters.author"
                  placeholder="Buscar por nombre de autor"
                >
                <span class="icon is-left">
                  <i class="fas fa-user"></i>
                </span>
              </div>
            </div>
          </div>

          <!-- Date Range -->
          <div class="column is-4">
            <div class="field">
              <label class="label">Publicados desde</label>
              <div class="control">
                <input
                  class="input"
                  type="date"
                  v-model="filters.published_from"
                >
              </div>
            </div>
          </div>

          <div class="column is-4">
            <div class="field">
              <label class="label">Publicados hasta</label>
              <div class="control">
                <input
                  class="input"
                  type="date"
                  v-model="filters.published_to"
                >
              </div>
            </div>
          </div>

          <!-- Per Page Selection - New Column -->
          <div class="column is-4">
            <div class="field">
              <label class="label">Noticias por página</label>
              <div class="control">
                <div class="select is-fullwidth">
                  <select v-model="perPage" @change="handlePerPageChange">
                    <option :value="5">5</option>
                    <option :value="10">10</option>
                    <option :value="15">15</option>
                    <option :value="20">20</option>
                    <option :value="25">25</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <!-- Search Button -->
          <div class="column is-12">
            <div class="field is-grouped">
              <div class="control">
                <button
                  class="button is-light"
                  @click="resetFilters"
                >
                  Limpiar filtros
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State (unchanged) -->
      <div v-if="loading" class="has-text-centered my-6">
        <div class="button is-loading is-white is-large"></div>
        <p class="subtitle mt-4">Cargando noticias...</p>
      </div>

      <!-- Error State (unchanged) -->
      <div v-if="error" class="notification is-danger">
        <button class="delete" @click="error = null"></button>
        <p class="has-text-weight-semibold">{{ error }}</p>
        <button class="button is-danger is-light mt-3" @click="fetchNews">
          Reintentar
        </button>
      </div>

      <!-- Empty State (unchanged) -->
      <div v-if="!loading && !error && !news.length" class="has-text-centered my-6">
        <div class="box p-6 has-background-light">
          <span class="icon is-large">
            <i class="fas fa-newspaper fa-2x"></i>
          </span>
          <p class="subtitle mt-4">No se encontraron noticias.</p>
        </div>
      </div>

      <!-- News List (unchanged) -->
      <div v-if="news.length" class="columns is-multiline mt-4">
        <div v-for="article in news"
             :key="article.id"
             class="column is-12 mb-4">
          <div class="card">
            <div class="card-content">
              <div class="media">
                <div class="media-content">
                  <p class="title is-4">{{ article.title }}</p>
                  <p class="subtitle is-6">
                    <span class="icon">
                      <i class="fas fa-user"></i>
                    </span>
                    {{ article.author }}
                  </p>
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
                  <span class="icon">
                    <i class="fas fa-book-open"></i>
                  </span>
                  <span>Leer artículo</span>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination (unchanged) -->
      <nav class="pagination is-centered mt-6" role="navigation" aria-label="pagination">
        <button
          class="pagination-previous"
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
        >
          Previous
        </button>
        <button
          class="pagination-next"
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
        >
          Siguiente
        </button>
        <ul class="pagination-list">
          <template v-for="(page, index) in paginationItems" :key="index">
            <li v-if="typeof page === 'number'">
              <a
                class="pagination-link"
                :class="{ 'is-current': page === currentPage }"
                @click="changePage(page)"
              >
                {{ page }}
              </a>
            </li>
            <li v-else>
              <span class="pagination-ellipsis">&hellip;</span>
            </li>
          </template>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useNewsStore } from '../stores/news';
import { storeToRefs } from 'pinia';

const store = useNewsStore();
const { news, loading, error, totalItems } = storeToRefs(store);

const currentPage = ref(1);
const perPage = ref(10); // Default value set to 10

const filters = ref({
    author: '',
    published_from: '',
    published_to: '',
    page: 1,
    per_page: perPage.value
});

// Computed properties for pagination
const totalPages = computed(() => Math.ceil(totalItems.value / perPage.value));

const paginationItems = computed(() => {
    if (totalPages.value <= 7) {
        return Array.from({ length: totalPages.value }, (_, i) => i + 1);
    }

    const items = [];
    if (currentPage.value <= 3) {
        // Show first 5 pages + ellipsis + last page
        for (let i = 1; i <= 5; i++) items.push(i);
        items.push('...');
        items.push(totalPages.value);
    } else if (currentPage.value >= totalPages.value - 2) {
        // Show first page + ellipsis + last 5 pages
        items.push(1);
        items.push('...');
        for (let i = totalPages.value - 4; i <= totalPages.value; i++) items.push(i);
    } else {
        // Show first page + ellipsis + current-1, current, current+1 + ellipsis + last page
        items.push(1);
        items.push('...');
        for (let i = currentPage.value - 1; i <= currentPage.value + 1; i++) items.push(i);
        items.push('...');
        items.push(totalPages.value);
    }
    return items;
});

// Methods
const fetchNews = async () => {
    try {
        // Update per_page in filters when fetching
        filters.value.per_page = perPage.value;
        await store.fetchNews({
            ...filters.value,
            page: currentPage.value,
            per_page: perPage.value
        });
    } catch (e) {
        console.error('Failed to fetch news:', e);
    }
};

const handleSearch = () => {
    currentPage.value = 1;
    fetchNews();
};

const handlePerPageChange = () => {
    // Reset to first page when changing per page
    currentPage.value = 1;
    fetchNews();
};

const resetFilters = () => {
    filters.value = {
        author: '',
        published_from: '',
        published_to: '',
        page: 1,
        per_page: 10
    };
    perPage.value = 10;
    currentPage.value = 1;
    fetchNews();
};

const changePage = (page) => {
    currentPage.value = page;
    fetchNews();
};

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
};

// Watch for filter changes
watch([() => filters.value.author, () => filters.value.published_from, () => filters.value.published_to],
    () => {
        // Debounce author search
        if (debounceTimeout.value) clearTimeout(debounceTimeout.value);
        debounceTimeout.value = setTimeout(() => {
            handleSearch();
        }, 300);
    }
);

const debounceTimeout = ref(null);

onMounted(() => {
    fetchNews();
});
</script>

<style scoped>
.card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.pagination-link.is-current {
    background-color: #485fc7;
    border-color: #485fc7;
}

.media-content {
    overflow: hidden;
}

.content {
    white-space: pre-line;
}
</style>
