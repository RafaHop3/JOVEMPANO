<template>
  <aside class="w-full sticky top-24">
    <!-- Ad space or Monetization -->
    <div class="bg-gradient-to-br from-rose-900/20 to-slate-100 dark:from-rose-900/40 dark:to-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 mb-6 text-center shadow-lg">
<template>
  <aside class="w-full sticky top-24">
    <!-- Ad space or Monetization -->
    <div class="bg-gradient-to-br from-rose-900/20 to-slate-100 dark:from-rose-900/40 dark:to-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 mb-6 text-center shadow-lg">
      <span class="text-xs text-slate-400 dark:text-slate-500 uppercase tracking-widest font-bold mb-2 block">Publicidade</span>
      <div class="w-full h-64 bg-slate-200/50 dark:bg-slate-800/50 rounded flex items-center justify-center border border-dashed border-slate-300 dark:border-slate-700">
        <p class="text-slate-500 font-medium">Espaço Premium</p>
      </div>
    </div>
    
    <!-- Top Read / Trending -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm dark:shadow-xl">
      <div class="flex items-center justify-between mb-4">
        <h4 class="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <span class="w-1.5 h-4 bg-rose-600 rounded"></span> Em Alta
        </h4>
        <button @click="fetchTrending" :disabled="loading" class="text-slate-400 hover:text-rose-500 transition-colors p-1 rounded-full disabled:opacity-50" title="Atualizar">
          <svg :class="{'animate-spin': loading}" width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
        </button>
      </div>
      <ul v-if="loading" class="flex flex-col gap-4">
        <li v-for="i in 3" :key="i" class="border-b border-light-200 dark:border-slate-800 pb-3 last:border-0 last:pb-0">
          <div class="flex flex-col gap-2">
            <div class="skeleton h-3.5 w-full"></div>
            <div class="skeleton h-3.5 w-3/4"></div>
          </div>
        </li>
      </ul>
      <ul v-else-if="trendingNews.length > 0" class="flex flex-col gap-4 fade-up">
        <li v-for="news in trendingNews" :key="news.id" class="border-b border-light-200 dark:border-slate-800 pb-3 last:border-0 last:pb-0">
          <router-link :to="`/news/${news.id}`" class="text-slate-700 dark:text-slate-300 hover:text-rose-500 transition-colors text-sm font-medium line-clamp-2">
            {{ news.title }}
          </router-link>
        </li>
      </ul>
      <p v-else class="text-sm text-slate-500">Nenhuma notícia em alta no momento.</p>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_BASE = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL) || 'http://localhost:8000'
const trendingNews = ref([])
const loading = ref(true)

async function fetchTrending() {
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/news/trending`)
    if (res.ok) {
      trendingNews.value = await res.json()
    }
  } catch (e) {
    console.warn('[SidebarWidget] failed to fetch trending news', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchTrending()
})
</script>
