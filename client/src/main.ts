import FomanticUI from 'vue-fomantic-ui';
import 'fomantic-ui-css/semantic.min.css';

// import '@/assets/geometry.css';
// import '@/assets/styles.css';

import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import LandingPage from './pages/LandingPage.vue';
import TopicsPage from './pages/TopicsPage.vue';
import TopicPage from './pages/TopicPage.vue';
import QuestionPage from './pages/QuestionPage.vue';
import SubmissionsPage from './pages/SubmissionsPage.vue';
import AttemptsPage from './pages/AttemptsPage.vue';
import FeedbackPage from './pages/FeedbackPage.vue';
import AboutPage from './pages/AboutPage.vue';
import NotFoundPage from './pages/NotFoundPage.vue';

// URL declarations.
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: LandingPage },
    { path: '/topics/', component: TopicsPage },
    { path: '/topic/:pk/', component: TopicPage, props: true },
    { path: '/question/:pk/', component: QuestionPage, props: true },
    { path: '/submissions/', component: SubmissionsPage },
    { path: '/attempts/', component: AttemptsPage },
    { path: '/feedback/', component: FeedbackPage },
    { path: '/about/', component: AboutPage },
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

// Entry point.
const app = createApp(App);
app.use(FomanticUI);
app.use(router);
app.mount('#app');
