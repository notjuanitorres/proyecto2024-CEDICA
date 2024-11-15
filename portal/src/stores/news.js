// import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useNewsStore = defineStore('news', {
    state: () => ({
        news: [],
        loading: false,
        error: null
    }),

    actions: {
        async fetchNews() {
            try {
                this.news = [
                    {
                        id: 1,
                        publishDate: "20/02/2020",
                        title: "A title",
                        content: "News content here",
                    },
                    {
                        id: 2,
                        publishDate: "20/02/2020",
                        title: "A title",
                        content: "News content here",
                    },
                    {
                        id: 3,
                        publishDate: "20/02/2020",
                        title: "A title",
                        content: "News content here",
                    }
                ]
            }
            catch {
                this.error = "Erorr al obtener las noticias"
            }
            finally {
                this.loading = false;
            }
        }
    }
})
