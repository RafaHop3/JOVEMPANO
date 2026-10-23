<template>
  <aside class="w-full sticky top-24 flex flex-col gap-5">

    <!-- Ad / Propaganda Primária INHO Business Compact Card -->
    <div
      class="rounded-2xl p-5 border border-cyan-500/30 bg-[#070d18]/90 backdrop-blur-xl shadow-lg relative overflow-hidden group"
    >
      <div class="absolute top-0 right-0 w-32 h-32 bg-cyan-500/10 rounded-full blur-2xl pointer-events-none"></div>

      <div class="flex items-center justify-between mb-3">
        <span class="text-[10px] font-mono uppercase tracking-widest font-bold text-neon-cyan flex items-center gap-1.5">
          <span class="w-1.5 h-1.5 rounded-full bg-neon-cyan animate-pulse"></span>
          DESTAQUE // ORBE SYSTEMS
        </span>
        <span class="text-[9px] font-mono text-slate-500">HOMOLOGADO</span>
      </div>

      <div class="space-y-2">
        <h4 class="text-base font-extrabold text-white font-editorial">
          INHO <span class="text-neon-cyan">Business</span>
        </h4>
        <p class="text-xs text-slate-300 leading-relaxed font-sans">
          Motor contábil inteligente com emissão imediata de DRE e conciliação bancária via PIX.
        </p>

        <!-- Micro stats -->
        <div class="grid grid-cols-2 gap-2 pt-2 text-[10px] font-mono">
          <div class="p-2 rounded bg-black/50 border border-cyan-500/20 text-center">
            <div class="text-neon-cyan font-bold">&lt; 1s</div>
            <div class="text-slate-400">Latência PIX</div>
          </div>
          <div class="p-2 rounded bg-black/50 border border-emerald-500/20 text-center">
            <div class="text-emerald-400 font-bold">99.8%</div>
            <div class="text-slate-400">DRE Real-time</div>
          </div>
        </div>

        <a
          href="https://inho.orbesystems.com.br"
          target="_blank"
          rel="noopener noreferrer"
          class="mt-3 block w-full py-2.5 rounded-lg text-center font-mono text-xs font-bold bg-gradient-to-r from-neon-cyan to-sky-500 text-black hover:brightness-110 shadow-neon-cyan transition-all"
        >
          Acessar inho.orbesystems.com.br ↗
        </a>
      </div>
    </div>

    <!-- Em Alta / Trending — Cyber Glass -->
    <div
      class="rounded-2xl p-5 border border-cyan-500/20 bg-[#070d18]/80 backdrop-blur-xl shadow-md"
    >
      <div class="flex items-center justify-between mb-4">
        <h4 class="text-sm font-bold flex items-center gap-2 text-white font-editorial">
          <span class="w-1.5 h-3.5 rounded-full bg-neon-cyan"></span>
          Radar em Alta
        </h4>
        <button
          @click="fetchTrending"
          :disabled="loading"
          class="transition-all p-1.5 rounded-md text-cyan-400 hover:text-white bg-cyan-950/40 border border-cyan-500/20 disabled:opacity-40"
          title="Atualizar"
        >
          <svg :class="{'animate-spin': loading}" width="12" height="12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
        </button>
      </div>

      <!-- Loading skeletons -->
      <ul v-if="loading" class="flex flex-col gap-3">
        <li v-for="i in 3" :key="i" class="border-b border-cyan-500/10 pb-3 last:border-0 last:pb-0">
          <div class="skeleton h-3.5 w-full"></div>
        </li>
      </ul>

      <!-- Trending list -->
      <ul v-else-if="trendingNews.length > 0" class="flex flex-col gap-3 fade-up">
        <li
          v-for="(news, idx) in trendingNews"
          :key="news.id"
          class="border-b border-cyan-500/10 pb-3 last:border-0 last:pb-0"
        >
          <router-link
            :to="`/news/${news.id}`"
            class="text-xs font-medium line-clamp-2 text-slate-300 hover:text-neon-cyan transition-colors flex items-start gap-2"
          >
            <span class="font-mono text-[10px] text-cyan-500 font-bold">[{{ String(idx + 1).padStart(2, '0') }}]</span>
            <span>{{ news.title }}</span>
          </router-link>
        </li>
      </ul>

      <p v-else class="text-xs text-slate-500 font-mono">Nenhuma matéria em alta no momento.</p>
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
