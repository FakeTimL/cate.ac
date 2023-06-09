import 'fomantic-ui-css/semantic.min.css';

import { createApp } from 'vue';
import FomanticUI from 'vue-fomantic-ui';
import App from './App.vue';

const app = createApp(App);
app.use(FomanticUI);
app.mount('#app');
