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
import App from './App.vue';
import LandingPage from './pages/LandingPage.vue';
import TopicsPage from './pages/TopicsPage.vue';
import TopicPage from './pages/TopicPage.vue';
import QuestionPage from './pages/QuestionPage.vue';
import FeedbackPage from './pages/FeedbackPage.vue';
import AboutPage from './pages/AboutPage.vue';
import ExamplePage from './pages/ExamplePage.vue'; // An example page of Vue.js.
import NotFoundPage from './pages/NotFoundPage.vue';

// URL declarations.
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: LandingPage },
    { path: '/topics', component: TopicsPage },
    { path: '/topic/:pk', component: TopicPage },
    { path: '/question/:pk', component: QuestionPage },
    { path: '/feedback', component: FeedbackPage },
    { path: '/about', component: AboutPage },
    { path: '/example', component: ExamplePage },
    // See: https://router.vuejs.org/guide/essentials/dynamic-matching.html#catch-all-404-not-found-route
    { path: '/:pathMatch(.*)*', component: NotFoundPage },
  ],
  // Jump to top when switching between pages.
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
