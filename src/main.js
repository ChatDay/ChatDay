import { createApp } from 'vue';
import App from './App.vue'; // App.vue 파일은 현재 src 폴더 안에 있습니다.
import router from './router/index'; // 라우터 경로는 그대로 유지

const app = createApp(App);
app.use(router);
app.mount('#app');