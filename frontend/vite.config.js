import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  // Simplified build without manualChunks to prevent Rollup binding errors
  build: {
    target: 'esnext',
    minify: 'terser',
    sourcemap: false,
  }
})
