import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue(),
  ],
  build: {
    target: 'es2015',
    minify: false,      // Disabling minification for debugging production crash
    sourcemap: true,   // Enabling sourcemaps to see the real stack trace
    cssCodeSplit: true,
  }
})
