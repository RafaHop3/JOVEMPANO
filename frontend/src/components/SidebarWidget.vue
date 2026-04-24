<template>
  <aside class="w-full sticky top-24 flex flex-col gap-5">

    <!-- Ad / Publicidade — Aero glass panel -->
    <div
      class="rounded-2xl p-6 text-center"
      style="
        background: linear-gradient(135deg,
          rgba(180,225,255,0.70) 0%,
          rgba(255,255,255,0.80) 50%,
          rgba(200,240,220,0.60) 100%
        );
        border: 1px solid rgba(255,255,255,0.70);
        backdrop-filter: blur(12px) saturate(160%);
        box-shadow: 0 2px 0 rgba(255,255,255,0.85) inset, 0 8px 28px rgba(30,100,200,0.10);
      "
    >
      <span class="text-xs uppercase tracking-widest font-bold mb-2 block" style="color: var(--text-muted);">Publicidade</span>
      <div
        class="w-full h-64 rounded-xl flex items-center justify-center"
        style="
          background: rgba(255,255,255,0.50);
          border: 2px dashed rgba(30,144,255,0.25);
        "
      >
        <!-- Aero decorative bubbles -->
        <div class="flex flex-col items-center gap-2">
          <div class="flex gap-3">
            <div class="w-8 h-8 rounded-full float-bubble" style="background: rgba(30,144,255,0.15); border: 1px solid rgba(30,144,255,0.25); animation-delay: 0s;"></div>
            <div class="w-5 h-5 rounded-full float-bubble" style="background: rgba(115,217,54,0.15); border: 1px solid rgba(115,217,54,0.25); animation-delay: 0.8s; margin-top: 12px;"></div>
            <div class="w-6 h-6 rounded-full float-bubble" style="background: rgba(90,200,250,0.15); border: 1px solid rgba(90,200,250,0.25); animation-delay: 1.6s;"></div>
          </div>
          <p class="font-bold text-sm" style="color: var(--text-muted);">Espaço Premium</p>
        </div>
      </div>
    </div>

    <!-- Em Alta / Trending — Aero glass -->
    <div
      class="rounded-2xl p-5"
      style="
        background: rgba(255,255,255,0.68);
        border: 1px solid rgba(255,255,255,0.70);
        backdrop-filter: blur(14px) saturate(170%);
        box-shadow: 0 2px 0 rgba(255,255,255,0.90) inset, 0 6px 24px rgba(30,100,200,0.09);
      "
    >
      <div class="flex items-center justify-between mb-4">
        <h4 class="text-base font-extrabold flex items-center gap-2" style="color: var(--text-primary);">
          <!-- Aero accent bar -->
          <span
            class="w-1.5 h-4 rounded-full"
            style="background: linear-gradient(180deg, #5ac8fa, #1e90ff);"
          ></span>
          Em Alta
        </h4>
        <button
          @click="fetchTrending"
          :disabled="loading"
          class="transition-all p-1.5 rounded-full disabled:opacity-40"
          style="color: var(--text-muted); background: rgba(30,144,255,0.08); border: 1px solid rgba(30,144,255,0.15);"
          title="Atualizar"
        >
          <svg :class="{'animate-spin': loading}" width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
        </button>
      </div>

      <!-- Loading skeletons -->
      <ul v-if="loading" class="flex flex-col gap-4">
        <li v-for="i in 3" :key="i" class="border-b pb-3 last:border-0 last:pb-0" style="border-color: rgba(30,144,255,0.10);">
          <div class="flex flex-col gap-2">
            <div class="skeleton h-3.5 w-full"></div>
            <div class="skeleton h-3.5 w-3/4"></div>
          </div>
        </li>
      </ul>

      <!-- Trending list -->
      <ul v-else-if="trendingNews.length > 0" class="flex flex-col gap-4 fade-up">
        <li
          v-for="news in trendingNews"
          :key="news.id"
          class="border-b pb-3 last:border-0 last:pb-0"
          style="border-color: rgba(30,144,255,0.10);"
        >
          <router-link
            :to="`/news/${news.id}`"
            class="text-sm font-semibold line-clamp-2 transition-colors"
            style="color: var(--text-secondary);"
            onmouseover="this.style.color='var(--brand)'"
            onmouseout="this.style.color='var(--text-secondary)'"
          >
            {{ news.title }}
          </router-link>
        </li>
      </ul>

      <p v-else class="text-sm" style="color: var(--text-muted);">Nenhuma notícia em alta no momento.</p>
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
