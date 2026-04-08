<template>
  <div class="flex flex-col gap-12">
    <!-- Hero Section / Latest -->
    <section>
      <h2 class="text-3xl font-bold text-slate-900 dark:text-white mb-8 border-l-4 border-rose-600 pl-4">Destaques do Dia</h2>
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-3 gap-6 animate-pulse">
        <div v-for="i in 3" :key="i" class="h-64 bg-slate-100 dark:bg-slate-900 rounded-xl"></div>
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <NewsCard v-for="item in latestNews" :key="item.id" :article="item" />
      </div>
    </section>

    <!-- Categorized Columns Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
      
      <!-- Politics Column -->
      <section class="flex flex-col gap-6">
        <div class="flex items-center gap-2 border-b-2 border-slate-100 dark:border-slate-800 pb-2">
          <span class="text-xl">🏛️</span>
          <h3 class="text-xl font-black text-slate-900 dark:text-white uppercase tracking-tighter">Política</h3>
        </div>
        <div v-if="politics.length === 0" class="text-slate-400 text-sm py-4 italic">Nenhuma notícia de política no momento.</div>
        <div v-else class="flex flex-col gap-4">
          <NewsCard v-for="item in politics" :key="item.id" :article="item" variant="compact" />
        </div>
      </section>

      <!-- Economy Column -->
      <section class="flex flex-col gap-6">
        <div class="flex items-center gap-2 border-b-2 border-slate-100 dark:border-slate-800 pb-2">
          <span class="text-xl">📈</span>
          <h3 class="text-xl font-black text-slate-900 dark:text-white uppercase tracking-tighter">Economia</h3>
        </div>
        <div v-if="economy.length === 0" class="text-slate-400 text-sm py-4 italic">Nenhuma notícia de economia no momento.</div>
        <div v-else class="flex flex-col gap-4">
          <NewsCard v-for="item in economy" :key="item.id" :article="item" variant="compact" />
        </div>
      </section>

      <!-- World/Tech Column -->
      <section class="flex flex-col gap-6">
        <div class="flex items-center gap-2 border-b-2 border-slate-100 dark:border-slate-800 pb-2">
          <span class="text-xl">🌐</span>
          <h3 class="text-xl font-black text-slate-900 dark:text-white uppercase tracking-tighter">Mundo & Tech</h3>
        </div>
        <div v-if="worldAndTech.length === 0" class="text-slate-400 text-sm py-4 italic">Nenhuma notícia de mundo ou tech.</div>
        <div v-else class="flex flex-col gap-4">
          <NewsCard v-for="item in worldAndTech" :key="item.id" :article="item" variant="compact" />
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useHead } from '@unhead/vue'
import NewsCard from '../components/NewsCard.vue'

useHead({
  title: 'JOVEMPANO - Notícias em Tempo Real',
  meta: [
    { name: 'description', content: 'Acompanhe as notícias mais quentes, sem filtros e de forma ultra rápida.' }
  ]
})

const allNews = ref([])
const loading = ref(true)

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const latestNews = computed(() => allNews.value.slice(0, 6))
const politics = computed(() => allNews.value.filter(n => n.category === 'Política').slice(0, 5))
const economy = computed(() => allNews.value.filter(n => n.category === 'Economia').slice(0, 5))
const worldAndTech = computed(() => allNews.value.filter(n => ['Mundo', 'Tecnologia'].includes(n.category)).slice(0, 5))

onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE}/news/`)
    allNews.value = await res.json()
  } catch (error) {
    console.error("Failed to fetch news:", error)
  } finally {
    loading.value = false
  }
})
</script>
