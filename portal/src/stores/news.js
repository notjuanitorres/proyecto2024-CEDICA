import { defineStore } from 'pinia';

export const useNewsStore = defineStore('news', {
  state: () => ({
    news: [],
    loading: false,
    error: null,
    totalItems: 0
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

        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/articles?${queryParams.toString()}`);

        if (!response.ok) {
          throw new Error('Failed to fetch news');
        }

        const data = await response.json();
        this.news = data.data;

        this.totalItems = data.total;
      } catch {
        this.error = 'Error al obtener las noticias';
      } finally {
        this.loading = false;
      }
    }
  }
});
