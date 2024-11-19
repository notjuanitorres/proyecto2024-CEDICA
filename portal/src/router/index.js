import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/nosotros',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/noticias',
      name: 'news',
      component: () => import('../views/NewsView.vue'),
    },
    {
    path: '/noticia/:id',
    name: 'news-detail',
    component: () => import('../views/NewsDetailView.vue'),
    props: true
  }
  ],
})

export default router
