import { fileURLToPath, URL } from 'node:url';

import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  base: '/',
  publicDir: false,
  build: {
    outDir: 'build',
    assetsDir: 'static',
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks: {
          semantic: ['fomantic-ui-css/semantic.min.css'],
          katex: ['katex'],
          hljs: ['highlight.js'],
        },
      },
    },
  },
});
