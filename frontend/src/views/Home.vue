<template>
  <div class="flex flex-col gap-10">

    <!-- ═══════ BREAKING TICKER ═══════ -->
    <BreakingTicker :headlines="tickerHeadlines" />

    <!-- ═══════ HERO SECTION ═══════ -->
    <section>
      <!-- Loading skeletons -->
      <div v-if="heroLoading" class="grid gap-4" style="grid-template-columns: 3fr 2fr;">
        <div class="skeleton" style="min-height: 460px;"></div>
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
        <!-- Mobile: stacked; Desktop: sidebar layout -->
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
      <div v-else class="flex flex-col items-center justify-center py-20" style="color: var(--text-muted);">
        <span class="text-5xl mb-4">📭</span>
        <p>Nenhum destaque publicado ainda.</p>
        <router-link to="/admin" class="mt-3 text-sm underline" style="color: var(--brand);">
          Publicar uma notícia →
        </router-link>
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

      <!-- Feed loading -->
      <div v-if="feedLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="i in 6" :key="i" class="skeleton" style="height: 280px;"></div>
      </div>

      <!-- Feed grid -->
      <div
        v-else-if="currentFeed.length > 0"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 fade-up"
      >
        <FeedCard
          v-for="item in currentFeed"
          :key="item.id"
          :article="item"
        />
      </div>

      <!-- No results for admin tab -->
      <div
        v-else-if="activeTab === 'admin' && adminNews.length === 0"
        class="text-center py-16"
        style="color: var(--text-muted);"
      >
        <span class="text-5xl block mb-4">📭</span>
        <p class="mb-3">Nenhuma notícia publicada ainda.</p>
        <router-link to="/admin" class="text-sm underline" style="color: var(--brand);">
          Ir para o painel →
        </router-link>
      </div>

      <!-- Feed empty state -->
      <div v-else class="text-center py-16" style="color: var(--text-muted);">
        <span class="text-5xl block mb-4">📡</span>
        <p>Não foi possível carregar as notícias agora. Tente novamente.</p>
        <button @click="refreshFeed" class="mt-4 text-sm underline" style="color: var(--brand);">
          Tentar novamente
        </button>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
// import { useHead } from '@unhead/vue'
import NewsCard from '../components/NewsCard.vue'
import FeedCard from '../components/FeedCard.vue'
import BreakingTicker from '../components/BreakingTicker.vue'

// useHead({
//   title: 'JovemPano — Notícias em Tempo Real',
//   meta: [
//     {
//       name: 'description',
//       content: 'Acompanhe as notícias mais importantes do Brasil e do mundo, em tempo real.',
//     },
//   ],
// })

const API_BASE = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL) || 'http://localhost:8000'

// ── State ─────────────────────────────────────────────────────────────────────
const adminNews   = ref([])
const heroLoading = ref(true)
const feedLoading = ref(false)
const activeTab   = ref('geral')
const feedCache   = ref({})       // { tabId: article[] }
const tickerHeadlines = ref([])

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
  if (adminNews.value.length > 0) return adminNews.value.slice(0, 3)
  // Fallback: map RSS articles to the article shape
  const geral = feedCache.value['geral'] || []
  return geral.slice(0, 3).map(f => ({
    id:         f.id,
    title:      f.title,
    content:    f.summary,
    image_url:  f.image_url,
    category:   f.category,
    created_at: f.published_at || new Date().toISOString(),
    link:       f.link,
    external:   true,
  }))
})

const currentFeed = computed(() => {
  if (activeTab.value === 'admin') return adminNews.value
  return feedCache.value[activeTab.value] || []
})

// ── Data fetching ─────────────────────────────────────────────────────────────
async function fetchAdminNews() {
  try {
    const res = await fetch(`${API_BASE}/news/`)
    if (res.ok) adminNews.value = await res.json()
  } catch (e) {
    console.warn('[Home] admin news fetch failed', e)
  } finally {
    heroLoading.value = false
  }
}

async function fetchFeed(slug) {
  if (feedCache.value[slug]) return  // already cached
  feedLoading.value = true
  try {
    const res = await fetch(`${API_BASE}/feeds/${slug}`)
    if (res.ok) {
      feedCache.value[slug] = await res.json()
      // Populate ticker from geral feed
      if (slug === 'geral') {
        tickerHeadlines.value = (feedCache.value['geral'] || [])
          .map(a => a.title)
          .slice(0, 20)
      }
    } else {
      feedCache.value[slug] = []
    }
  } catch (e) {
    console.warn(`[Home] feed "${slug}" fetch failed`, e)
    feedCache.value[slug] = []
  } finally {
    feedLoading.value = false
  }
}

async function switchTab(tabId) {
  activeTab.value = tabId
  if (tabId !== 'admin') await fetchFeed(tabId)
}

function refreshFeed() {
  if (activeTab.value === 'admin') {
    fetchAdminNews()
  } else {
    delete feedCache.value[activeTab.value]
    fetchFeed(activeTab.value)
  }
}

// ── Lifecycle ─────────────────────────────────────────────────────────────────
onMounted(async () => {
  // Fetch both simultaneously on load
  await Promise.all([fetchAdminNews(), fetchFeed('geral')])
})
</script>
