<template>
  <div class="flex flex-col gap-10">

    <!-- ═══════ BREAKING TICKER ═══════ -->
    <BreakingTicker :headlines="tickerHeadlines" />

    <!-- ═══════ HERO SECTION ═══════ -->
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

      <!-- Empty hero -->
      <div v-else class="flex flex-col items-center justify-center py-20 px-4 text-center" style="color: var(--text-muted);">
        <span class="text-5xl mb-4">📭</span>
        <p class="max-w-md">Nenhum destaque editorial ainda. Quando a equipe publicar matérias, elas aparecerão aqui.</p>
        <p class="mt-2 text-sm max-w-md">Enquanto isso, use as abas abaixo para acompanhar o feed ao vivo (RSS) atualizado continuamente.</p>
      </div>
    </section>

    <!-- ═══════ LIVE NEWS — RSS BY CATEGORY ═══════ -->
    <section>
      <!-- Section header -->
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center gap-3">
          <span class="pulse-live w-2.5 h-2.5 rounded-full" style="background: var(--brand); display: inline-block;"></span>
          <h2 class="text-xl font-bold" style="color: var(--text-primary);">Notícias ao Vivo</h2>
          <span class="font-mono-jp text-xs px-2 py-0.5 rounded" style="background: var(--brand-glow); color: var(--brand);">
            RSS
          </span>
        </div>
        <button
          id="btn-refresh-feed"
          @click="refreshFeed"
          :disabled="feedLoading"
          class="text-xs px-3 py-1.5 rounded-full border transition-all hover:border-white/20 disabled:opacity-40"
          style="color: var(--text-muted); border-color: var(--border);"
        >
          {{ feedLoading ? '...' : '↻ Atualizar' }}
        </button>
      </div>

      <!-- Category tabs -->
      <div style="border-bottom: 1px solid var(--border);" class="flex overflow-x-auto scrollbar-hide mb-6">
        <button
          v-for="tab in feedTabs"
          :key="tab.id"
          :id="`tab-${tab.id}`"
          @click="switchTab(tab.id)"
          :class="['tab-btn', activeTab === tab.id ? 'active' : '']"
          :style="activeTab === tab.id ? `color: ${tab.color};` : ''"
        >
          {{ tab.emoji }} {{ tab.label }}
        </button>
      </div>

      <!-- Feed grid -->
      <div
        v-if="currentFeed.length > 0"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 fade-up"
      >
        <FeedCard
          v-for="item in currentFeed"
          :key="item.id"
          :article="item"
        />
      </div>

      <!-- Initial Loading -->
      <div v-if="feedLoading && currentFeed.length === 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="i in 6" :key="i" class="skeleton" style="height: 280px;"></div>
      </div>

      <!-- Empty states -->
      <div
        v-else-if="activeTab === 'admin' && adminNews.length === 0"
        class="text-center py-16 px-4"
        style="color: var(--text-muted);"
      >
        <span class="text-5xl block mb-4">📭</span>
        <p class="mb-2 max-w-md mx-auto">Nenhuma notícia editorial publicada ainda. O painel de publicação é acessado apenas pela URL <span class="font-mono text-xs" style="color: var(--text-secondary);">/admin</span>.</p>
      </div>

      <div v-else-if="currentFeed.length === 0 && !feedLoading" class="text-center py-16" style="color: var(--text-muted);">
        <span class="text-5xl block mb-4">📡</span>
        <p>Não foi possível carregar as notícias agora. Tente novamente.</p>
        <button @click="refreshFeed" class="mt-4 text-sm underline" style="color: var(--brand);">
          Tentar novamente
        </button>
      </div>

      <!-- INFINITE SCROLL SENTINEL & LOADING -->
      <div ref="sentinel" class="py-10 flex flex-col items-center justify-center">
        <div v-if="feedLoading && currentFeed.length > 0" class="flex items-center gap-2" style="color: var(--text-muted);">
          <div class="w-4 h-4 rounded-full border-2 border-t-transparent animate-spin" style="border-color: var(--brand); border-top-color: transparent;"></div>
          <span class="text-sm">Descobrindo mais notícias...</span>
        </div>
        <div v-else-if="!hasMore && currentFeed.length > 0" class="text-xs italic" style="color: var(--text-muted);">
          Você chegou ao fim do feed.
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

const API_BASE = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL) || 'http://localhost:8000'

// ── State ─────────────────────────────────────────────────────────────────────
const adminNews   = ref([])
const heroLoading = ref(true)
const feedLoading = ref(false)
const activeTab   = ref('geral')
const feedCache   = ref({})       // { tabId: article[] }
const feedPages   = ref({})       // { tabId: currentPage }
const hasMoreMap  = ref({})       // { tabId: boolean }
const tickerHeadlines = ref([])
const sentinel    = ref(null)

let observer = null

// ── Tab definitions ────────────────────────────────────────────────────────────
const feedTabs = [
  { id: 'admin',     label: 'Publicados',  emoji: '📌', color: 'var(--brand)' },
  { id: 'geral',     label: 'Últimas',     emoji: '🔥', color: 'var(--cat-esportes)' },
  { id: 'politica',  label: 'Política',    emoji: '🏛️', color: 'var(--cat-politica)' },
  { id: 'economia',  label: 'Economia',    emoji: '📈', color: 'var(--cat-economia)' },
  { id: 'esportes',  label: 'Esportes',    emoji: '⚽', color: 'var(--cat-esportes)' },
  { id: 'tecnologia',label: 'Tecnologia',  emoji: '💻', color: 'var(--cat-tecnologia)' },
  { id: 'mundo',     label: 'Mundo',       emoji: '🌐', color: 'var(--cat-mundo)' },
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
      
      // If we got fewer items than the limit, assume no more items
      if (data.length < 12) {
        hasMoreMap.value[slug] = false
      } else {
        hasMoreMap.value[slug] = true
      }

      // Ticker from geral
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

function refreshFeed() {
  if (activeTab.value === 'admin') {
    fetchAdminNews()
  } else {
    feedCache.value[activeTab.value] = []
    hasMoreMap.value[activeTab.value] = true
    fetchFeed(activeTab.value)
  }
}

// ── Infinite Scroll Observer ──────────────────────────────────────────────────
function setupObserver() {
  if (observer) observer.disconnect()
  
  observer = new IntersectionObserver((entries) => {
    const entry = entries[0]
    if (entry.isIntersecting && hasMore.value && !feedLoading.value) {
      fetchFeed(activeTab.value, true)
    }
  }, { threshold: 0.1 })
  
  if (sentinel.value) observer.observe(sentinel.value)
}

// ── Lifecycle ─────────────────────────────────────────────────────────────────
onMounted(async () => {
  await Promise.all([fetchAdminNews(), fetchFeed('geral')])
  setupObserver()
})

onUnmounted(() => {
  if (observer) observer.disconnect()
})

watch(activeTab, () => {
  // Reset observer or re-check sentinel on tab change
  setTimeout(setupObserver, 100)
})
</script>

<style scoped>
.tab-btn {
  @apply px-4 py-3 text-sm font-medium transition-all whitespace-nowrap border-b-2 border-transparent;
  color: var(--text-muted);
}
.tab-btn:hover {
  color: var(--text-primary);
}
.tab-btn.active {
  border-color: currentColor;
}
.animate-spin {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
