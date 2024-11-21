import { defineStore } from 'pinia';

export const useArticleStore = defineStore('singleNews',{
  state: () => ({
    article: {},
    loading: false,
    error: null
  }),
  actions: {
    async fetchArticle(id) {
      this.loading = true;
      this.error = null;
      this.article = {}
      try {
        const response = await fetch(`http://localhost:5000/api/articles/${id}`);
        if (!response.ok) {
          throw new Error('No se pudo cargar el artículo');
        }
        this.article = await response.json();
      } catch (e) {
        this.error = e.message;
        throw e;
      } finally {
        this.loading = false;
      }
    }
  }
});
