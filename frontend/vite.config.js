import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  optimizeDeps: {
    include: ['quill'],
  },
  build: {
    rollupOptions: {
      output: {
        // Separate Quill into its own chunk so it doesn't pollute the main bundle
        manualChunks: {
          quill: ['quill'],
        },
      },
    },
  },
})
