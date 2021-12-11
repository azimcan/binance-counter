import Vue from 'vue';
import VueRouter from 'vue-router';
import Symbols from '../components/Symbols.vue';

Vue.use(VueRouter);

export default new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/symbols',
      name: 'Symbols',
      component: Symbols,
    },
  ],
});
