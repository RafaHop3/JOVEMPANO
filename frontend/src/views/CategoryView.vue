<template>
  <div class="flex flex-col gap-8">

    <!-- ── Category Header ──────────────────────────────────────────────────── -->
    <div
      class="flex items-center gap-5 pb-5 fade-up"
      :style="`border-bottom: 2px solid ${catColor};`"
    >
      <span class="text-5xl leading-none">{{ emoji }}</span>
      <div class="flex-1 min-w-0">
        <h1 class="font-editorial text-3xl md:text-4xl font-bold" style="color: var(--text-primary);">
          {{ category }}
        </h1>
        <p class="text-sm mt-1" style="color: var(--text-muted);">
          Notícias ao vivo · Fonte: G1 Globo
        </p>
      </div>
      <!-- Live badge -->
      <div class="flex items-center gap-2 flex-shrink-0">
        <span
          class="pulse-live w-2 h-2 rounded-full"
          :style="`background: ${catColor}; display: inline-block;`"
        ></span>
        <span class="font-mono-jp text-xs font-bold" :style="`color: ${catColor};`">AO VIVO</span>
      </div>
    </div>

    <!-- ── Loading Skeletons ─────────────────────────────────────────────────── -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="i in 9" :key="i" class="skeleton" style="height: 280px;"></div>
    </div>

    <!-- ── News Grid ─────────────────────────────────────────────────────────── -->
    <div
      v-else-if="articles.length > 0"
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
    >
      <FeedCard
        v-for="(item, i) in articles"
        :key="item.id"
        :article="item"
        class="fade-up"
        :style="`animation-delay: ${Math.min(i * 60, 400)}ms; opacity: 0;`"
      />
    </div>

    <!-- ── Empty State ───────────────────────────────────────────────────────── -->
    <div v-else class="text-center py-24" style="color: var(--text-muted);">
      <span class="text-6xl block mb-6">📡</span>
      <p class="text-lg mb-2 font-semibold" style="color: var(--text-primary);">
        Sem notícias no momento
      </p>
      <p class="text-sm mb-6">
        Não foi possível carregar o feed de <strong>{{ category }}</strong>.
      </p>
      <button
        id="btn-retry"
        @click="load"
        class="px-6 py-3 rounded-xl font-bold text-sm transition-opacity hover:opacity-80"
        style="background: var(--bg-card); border: 1px solid var(--border); color: var(--text-primary);"
      >
        ↻ Tentar Novamente
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
// import { useHead } from '@unhead/vue'
import FeedCard from '../components/FeedCard.vue'

const props = defineProps({
  category:  { type: String, required: true },
  slug:      { type: String, required: true },
  emoji:     { type: String, default: '📰' },
  catColor:  { type: String, default: 'var(--brand)' },
})

// ── SEO ───────────────────────────────────────────────────────────────────────
/*
useHead(
  computed(() => ({
    title: `${props.category} — JovemPano`,
    meta: [
      { name: 'description', content: `As últimas notícias de ${props.category} em tempo real.` },
    ],
  }))
)
*/

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const articles = ref([])
const loading  = ref(true)

async function load() {
  loading.value = true
  articles.value = []
  try {
    const res = await fetch(`${API_BASE}/feeds/${props.slug}`)
    if (res.ok) articles.value = await res.json()
  } catch (e) {
    console.warn(`[CategoryView] feed "${props.slug}" failed`, e)
  } finally {
    loading.value = false
  }
}

onMounted(load)
// Reload when navigating between category pages (same component, different props)
watch(() => props.slug, load)
</script>
