import FomanticUI from 'vue-fomantic-ui';
import 'fomantic-ui-css/semantic.min.css';
import 'katex';
import 'katex/dist/katex.min.css';
import 'highlight.js';
import 'highlight.js/styles/github.css';

// import '@/assets/geometry.css';
// import '@/assets/styles.css';

import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from './pages/LandingPage.vue';
import TopicsPage from './pages/TopicsPage.vue';
import FeedbackPage from './pages/FeedbackPage.vue';
import AboutPage from './pages/AboutPage.vue';
import ExamplePage from './pages/ExamplePage.vue';
import NotFoundPage from './pages/NotFoundPage.vue';
import App from './App.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: LandingPage },
    { path: '/topics', component: TopicsPage },
    { path: '/feedback', component: FeedbackPage },
    { path: '/about', component: AboutPage },
    { path: '/example', component: ExamplePage }, // An example page of Vue.js
    // See: https://router.vuejs.org/guide/essentials/dynamic-matching.html#catch-all-404-not-found-route
    { path: '/:pathMatch(.*)*', component: NotFoundPage },
  ],
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

const app = createApp(App);
app.use(FomanticUI);
app.use(router);
app.mount('#app');
