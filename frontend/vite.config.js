import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  build: {
    target: 'esnext',
    minify: 'terser',    // Using terser for more robust minification
    sourcemap: true,    // Keeping sourcemaps for now to help in case of production issues
    cssCodeSplit: true,
  }
})
