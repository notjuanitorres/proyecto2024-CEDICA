import { defineStore } from 'pinia';

export const useNewsStore = defineStore('news', {
  state: () => ({
    news: [],
    loading: false,
    error: null,
    totalItems: 0,
    article: {},
  }),

  actions: {
    async fetchNews(params) {
      this.loading = true;
      this.error = null;

      try {
        const queryParams = new URLSearchParams();

        if (params.author) queryParams.append('author', params.author);
        if (params.published_from) queryParams.append('published_from', params.published_from);
        if (params.published_to) queryParams.append('published_to', params.published_to);
        if (params.page) queryParams.append('page', params.page);
        if (params.per_page) queryParams.append('per_page', params.per_page);

        const apiUrl = import.meta.env.VITE_API_BASE_URL || "https://admin-grupo19.proyecto2024.linti.unlp.edu.ar/api"
        const url = `${apiUrl}/articles?${queryParams.toString()}`;

        const response = await fetch(url);

        if (!response.ok) {
          throw new Error('Failed to fetch news');
        }

        const data = await response.json();

        this.news = data.data;
        this.totalItems = data.total;

      } catch (error) {
        this.error = 'Error al obtener las noticias';
      } finally {
        this.loading = false;
      }
    },

    async fetchArticle(id) {
      this.loading = true;
      this.error = null;
      this.article = {};

      try {
        const apiUrl = import.meta.env.VITE_API_BASE_URL  || "https://admin-grupo19.proyecto2024.linti.unlp.edu.ar/api"
        const url = `${apiUrl}/articles/${id}`;

        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('No se pudo cargar el artículo');
        }

        this.article = await response.json();
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});
