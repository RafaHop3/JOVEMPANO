<template>
  <div class="flex flex-col gap-10">

    <!-- ═══════ BREAKING TICKER (Orbe Systems Cyber Ticker) ═══════ -->
    <BreakingTicker :headlines="tickerHeadlines" />

    <!-- ═══════ DESTAQUE DE PROPAGANDA PRIMÁRIA: INHO BUSINESS ENGINE ═══════ -->
    <section class="fade-up">
      <InhoPromoBanner />
    </section>

    <!-- ═══════ HERO SECTION (Destaques Editoriais) ═══════ -->
    <section>
      <!-- Loading skeletons -->
      <div v-if="heroLoading" class="grid gap-4" style="grid-template-columns: 3fr 2fr;">
        <div class="skeleton" style="min-height: 320px;"></div>
        <div class="flex flex-col gap-4">
          <div class="skeleton flex-1"></div>
          <div class="skeleton flex-1"></div>
        </div>
      </div>

      <!-- Hero grid: 1 featured + 2 secondary -->
      <div
        v-else-if="heroArticles.length > 0"
        class="grid gap-4 fade-up"
        style="grid-template-columns: 1fr; grid-template-rows: auto;"
      >
        <div class="grid gap-4 lg:grid-cols-5">
          <div class="lg:col-span-3">
            <NewsCard :article="heroArticles[0]" variant="hero" />
          </div>
          <div class="lg:col-span-2 flex flex-col gap-4">
            <NewsCard
              v-for="a in heroArticles.slice(1, 3)"
              :key="a.id"
              :article="a"
              variant="secondary"
              class="flex-1"
            />
          </div>
        </div>
      </div>

      <!-- Empty hero com Void Scanner -->
      <div v-else class="flex flex-col items-center justify-center py-16 px-4 text-center rounded-2xl border border-cyan-500/20 bg-slate-950/40 text-slate-400">
        <VoidGlyph shape="scanner" size="52" color="#00fff5" class="mb-4" />
        <p class="max-w-md font-medium text-slate-200">Radar editorial aguardando novas publicações.</p>
        <p class="mt-2 text-xs text-slate-400 max-w-md">Utilize o feed ao vivo em tempo real abaixo com monitoramento contínuo.</p>
      </div>
    </section>

    <!-- ═══════ LIVE NEWS — RSS POR CATEGORIA COM VOIDS ═══════ -->
    <section>
      <!-- Section header -->
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center gap-3">
          <span class="pulse-live w-2.5 h-2.5 rounded-full bg-neon-cyan inline-block"></span>
          <h2 class="text-xl font-bold font-editorial text-white tracking-wide">
            Radar em Tempo Real
          </h2>
          <span class="font-mono text-[11px] px-2 py-0.5 rounded bg-cyan-950/80 text-neon-cyan border border-cyan-500/30">
            FEED DINÂMICO
          </span>
        </div>
        <button
          id="btn-refresh-feed"
          @click="refreshFeed"
          :disabled="feedLoading"
          class="text-xs font-mono px-3.5 py-1.5 rounded-lg border border-cyan-500/30 text-cyan-300 hover:text-white hover:border-cyan-400 bg-cyan-950/40 transition-all disabled:opacity-40"
        >
          {{ feedLoading ? 'Sincronizando...' : '↻ Atualizar' }}
        </button>
      </div>

      <!-- Category tabs com VOID GLYPHS -->
      <div class="flex overflow-x-auto scrollbar-hide gap-2 pb-2 mb-6 border-b border-cyan-500/20">
        <button
          v-for="tab in feedTabs"
          :key="tab.id"
          :id="`tab-${tab.id}`"
          @click="switchTab(tab.id)"
          :class="['tab-btn', activeTab === tab.id ? 'active' : '']"
          :style="activeTab === tab.id ? `color: ${tab.color}; border-color: ${tab.color}50;` : ''"
        >
          <VoidGlyph :shape="tab.voidShape" :color="tab.color" :size="16" />
          <span>{{ tab.label }}</span>
        </button>
      </div>

      <!-- Feed grid -->
      <div
        v-if="currentFeed.length > 0"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 fade-up"
      >
        <FeedCard
          v-for="item in currentFeed"
          :key="item.id"
          :article="item"
        />
      </div>

      <!-- Initial Loading -->
      <div v-if="feedLoading && currentFeed.length === 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        <div v-for="i in 6" :key="i" class="skeleton" style="height: 280px;"></div>
      </div>

      <!-- Empty states com Void Scanner no lugar de emojis -->
      <div
        v-else-if="activeTab === 'admin' && adminNews.length === 0"
        class="text-center py-16 px-4 rounded-2xl border border-cyan-500/20 bg-slate-950/40 text-slate-400"
      >
        <VoidGlyph shape="shield" size="52" color="#00fff5" class="mb-4" />
        <p class="mb-2 max-w-md mx-auto text-slate-200">Nenhuma notícia editorial publicada ainda.</p>
        <p class="text-xs text-slate-400">Acesse o terminal editorial autenticado em <span class="font-mono text-cyan-400">/admin</span>.</p>
      </div>

      <div
        v-else-if="currentFeed.length === 0 && !feedLoading"
        class="text-center py-16 rounded-2xl border border-cyan-500/20 bg-slate-950/40 text-slate-400"
      >
        <VoidGlyph shape="scanner" size="52" color="#00fff5" class="mb-4" />
        <p class="text-slate-200">Não foi possível sincronizar o feed no momento.</p>
        <button @click="refreshFeed" class="mt-4 text-xs font-mono text-neon-cyan hover:underline">
          ↻ Tentar nova sincronização
        </button>
      </div>

      <!-- INFINITE SCROLL SENTINEL & LOADING -->
      <div ref="sentinel" class="py-10 flex flex-col items-center justify-center">
        <div v-if="feedLoading && currentFeed.length > 0" class="flex items-center gap-3 text-cyan-400 font-mono text-xs">
          <div class="w-4 h-4 rounded-full border-2 border-t-transparent border-cyan-400 animate-spin"></div>
          <span>Sincronizando mais notícias pelo radar...</span>
        </div>
        <div v-else-if="!hasMore && currentFeed.length > 0" class="text-xs font-mono text-slate-500 italic">
          [ FIM DA LINHA DO RADAR ]
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import NewsCard from '../components/NewsCard.vue'
import FeedCard from '../components/FeedCard.vue'
import BreakingTicker from '../components/BreakingTicker.vue'
import InhoPromoBanner from '../components/InhoPromoBanner.vue'
import VoidGlyph from '../components/VoidGlyph.vue'

const API_BASE = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL) || 'http://localhost:8000'

// ── State ─────────────────────────────────────────────────────────────────────
const adminNews   = ref([])
const heroLoading = ref(true)
const feedLoading = ref(false)
const activeTab   = ref('geral')
const feedCache   = ref({})
const feedPages   = ref({})
const hasMoreMap  = ref({})
const tickerHeadlines = ref([])
const sentinel    = ref(null)

let observer = null

// ── Tab definitions com VOIDS no lugar de emotions ────────────────────────────
const feedTabs = [
  { id: 'admin',     label: 'Editoriais',  voidShape: 'shield',   color: '#00fff5' },
  { id: 'geral',     label: 'Últimas',     voidShape: 'cluster',  color: '#7eb8e0' },
  { id: 'politica',  label: 'Política',    voidShape: 'shield',   color: '#f43f5e' },
  { id: 'economia',  label: 'Economia',    voidShape: 'pix-dre',  color: '#10b981' },
  { id: 'esportes',  label: 'Esportes',    voidShape: 'daw',      color: '#f59e0b' },
  { id: 'tecnologia',label: 'Tecnologia',  voidShape: 'nvme',     color: '#00fff5' },
  { id: 'mundo',     label: 'Mundo',       voidShape: 'globe',    color: '#3b82f6' },
]

// ── Computed ──────────────────────────────────────────────────────────────────
const heroArticles = computed(() => {
  const geral = feedCache.value['geral'] || []
  if (geral.length > 0) {
    return geral.slice(0, 3).map(f => ({
      id: f.id,
      title: f.title,
      content: f.summary,
      image_url: f.image_url,
      category: f.category,
      created_at: f.published_at || new Date().toISOString(),
      link: f.link,
      external: true,
      source: f.source
    }))
  }
  return adminNews.value.slice(0, 3)
})

const currentFeed = computed(() => {
  if (activeTab.value === 'admin') return adminNews.value
  return feedCache.value[activeTab.value] || []
})

const hasMore = computed(() => {
  if (activeTab.value === 'admin') return false
  return hasMoreMap.value[activeTab.value] !== false
})

// ── Data fetching ─────────────────────────────────────────────────────────────
async function fetchAdminNews() {
  try {
    const res = await fetch(`${API_BASE}/news/`)
    if (res.ok) adminNews.value = await res.json()
  } catch (e) {
    console.error('[Home] admin news fetch failed', e)
  } finally {
    heroLoading.value = false
  }
}

async function fetchFeed(slug, isLoadMore = false) {
  if (feedLoading.value) return
  
  const page = isLoadMore ? (feedPages.value[slug] || 1) + 1 : 1
  feedLoading.value = true
  
  try {
    const res = await fetch(`${API_BASE}/feeds/${slug}?page=${page}&limit=12`)
    if (res.ok) {
      const data = await res.json()
      
      if (isLoadMore) {
        feedCache.value[slug] = [...(feedCache.value[slug] || []), ...data]
        feedPages.value[slug] = page
      } else {
        feedCache.value[slug] = data
        feedPages.value[slug] = 1
      }
      
      if (data.length < 12) {
        hasMoreMap.value[slug] = false
      } else {
        hasMoreMap.value[slug] = true
      }

      if (slug === 'geral' && !isLoadMore) {
        tickerHeadlines.value = data.map(a => a.title).slice(0, 20)
      }
    }
  } catch (e) {
    console.error(`[Home] feed "${slug}" fetch failed`, e)
  } finally {
    feedLoading.value = false
  }
}

async function switchTab(tabId) {
  activeTab.value = tabId
  if (tabId !== 'admin' && (!feedCache.value[tabId] || feedCache.value[tabId].length === 0)) {
    await fetchFeed(tabId)
  }
}

async function refreshFeed() {
  if (activeTab.value === 'admin') {
    heroLoading.value = true
    await fetchAdminNews()
  } else {
    await fetchFeed(activeTab.value, false)
  }
}

onMounted(async () => {
  await Promise.all([
    fetchAdminNews(),
    fetchFeed('geral')
  ])

  // Infinite scroll
  observer = new IntersectionObserver((entries) => {
    const [entry] = entries
    if (entry.isIntersecting && !feedLoading.value && hasMore.value && activeTab.value !== 'admin') {
      fetchFeed(activeTab.value, true)
    }
  }, { threshold: 0.1 })

  if (sentinel.value) {
    observer.observe(sentinel.value)
  }
})

onUnmounted(() => {
  if (observer) observer.disconnect()
})
</script>
