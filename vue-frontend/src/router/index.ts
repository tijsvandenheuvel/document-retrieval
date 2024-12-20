import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
        },
        {
            path: '/search',
            name: 'search',
            component: () => import('../views/SearchView.vue')
          },
        {
            path: '/documents',
            name: 'documents',
            component: () => import('../views/DocumentsView.vue')
          },
    ]})

export default router