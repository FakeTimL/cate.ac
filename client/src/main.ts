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
import QuestionPage from './pages/QuestionPage.vue';
import FeedbackPage from './pages/FeedbackPage.vue';
import AboutPage from './pages/AboutPage.vue';
import ExamplePage from './pages/ExamplePage.vue';
import App from './App.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: LandingPage }, // An example page of Vue.js
    { path: '/topics', component: QuestionPage },
    { path: '/feedback', component: FeedbackPage },
    { path: '/about', component: AboutPage },
    { path: '/example', component: ExamplePage }, // An example page of Vue.js
  ],
});

const app = createApp(App);
app.use(FomanticUI);
app.use(router);
app.mount('#app');
