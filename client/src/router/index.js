import { createRouter, createWebHistory } from 'vue-router';
import Symbols from '../components/Symbols.vue';

const routes = [
  {
    path: '/symbols',
    name: 'Symbols',
    component: Symbols,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
