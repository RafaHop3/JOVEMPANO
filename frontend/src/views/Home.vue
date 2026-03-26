<template>
  <div class="grid grid-cols-1 lg:grid-cols-[70%_30%] gap-8">
    <!-- Left Column (70%) -->
    <section>
      <h2 class="text-3xl font-bold text-slate-900 dark:text-white mb-8 border-b border-slate-200 dark:border-slate-800 pb-4">Últimas Publicações</h2>
      
      <div v-if="loading" class="text-slate-500 animate-pulse text-lg font-medium">Buscando transmissões...</div>
      
      <div v-else-if="news.length === 0" class="text-slate-500 bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-xl text-center shadow-lg">
        <p class="text-xl font-bold text-slate-900 dark:text-white mb-2">Nada por aqui ainda.</p>
        <p>A redação está dormindo ou o banco de dados está vazio.</p>
      </div>
      
      <div v-else>
        <NewsCard v-for="item in news" :key="item.id" :article="item" />
      </div>
    </section>

    <!-- Right Column (30%) -->
    <SidebarWidget />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useHead } from '@unhead/vue'
import NewsCard from '../components/NewsCard.vue'
import SidebarWidget from '../components/SidebarWidget.vue'

// Injeção de Tags de SEO via Unhead
useHead({
  title: 'JOVEMPANO - Notícias Essenciais',
  meta: [
    { name: 'description', content: 'Acompanhe as notícias mais quentes, sem filtros e de forma ultra rápida.' },
    { property: 'og:title', content: 'JOVEMPANO - Arquitetura Limpa' },
    { property: 'og:description', content: 'O portal premium, super veloz e protegido, para a nova geração.' },
    { name: 'twitter:card', content: 'summary_large_image' }
  ]
})

const news = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:8000/news/')
    news.value = await res.json()
  } catch (error) {
    console.error("Failed to fetch news:", error)
  } finally {
    loading.value = false
  }
})
</script>
