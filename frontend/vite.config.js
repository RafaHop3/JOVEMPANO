import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue(),
  ],
  build: {
    target: 'esnext',
    minify: 'terser',    // Using terser for more robust minification
    sourcemap: true,    // Keeping sourcemaps for now to help in case of production issues
    cssCodeSplit: true,
  }
})
