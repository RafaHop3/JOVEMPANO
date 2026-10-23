<template>
  <div class="flex flex-col gap-8">

    <!-- ── Category Header com Void Glyph no lugar de emoji ───────────────── -->
    <div
      class="flex items-center gap-5 pb-5 fade-up border-b"
      :style="{ borderColor: `${catColor}50` }"
    >
      <!-- Big Animated Void Glyph -->
      <VoidGlyph :shape="voidShape" :color="catColor" :size="48" />

      <div class="flex-1 min-w-0">
        <h1 class="font-editorial text-3xl md:text-4xl font-bold text-white tracking-tight">
          {{ category }}
        </h1>
        <p class="text-xs sm:text-sm mt-1 font-mono text-slate-400">
          Radar em tempo real // Fontes agregadas e curadoria editorial
        </p>
      </div>

      <!-- Live badge -->
      <div class="flex items-center gap-2 flex-shrink-0">
        <span
          class="pulse-live w-2 h-2 rounded-full inline-block"
          :style="{ background: catColor }"
        ></span>
        <span class="font-mono text-xs font-bold tracking-wider" :style="{ color: catColor }">AO VIVO</span>
      </div>
    </div>

    <!-- ── Loading Skeletons ─────────────────────────────────────────────────── -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <div v-for="i in 9" :key="i" class="skeleton" style="height: 280px;"></div>
    </div>

    <!-- ── News Grid ─────────────────────────────────────────────────────────── -->
    <div
      v-else-if="articles.length > 0"
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5"
    >
      <FeedCard
        v-for="(item, i) in articles"
        :key="item.id"
        :article="item"
        class="fade-up"
        :style="`animation-delay: ${Math.min(i * 50, 400)}ms;`"
      />
    </div>

    <!-- ── Empty State com Void Scanner ──────────────────────────────────────── -->
    <div v-else class="text-center py-20 px-4 rounded-2xl border border-cyan-500/20 bg-slate-950/40 text-slate-400">
      <VoidGlyph shape="scanner" size="56" :color="catColor" class="mb-4" />
      <p class="text-base mb-1 font-semibold text-white">
        Sem transmissões no radar de {{ category }}
      </p>
      <p class="text-xs text-slate-400 mb-6">
        Não foi possível recuperar dados das fontes RSS para esta categoria.
      </p>
      <button
        id="btn-retry"
        @click="load"
        class="px-5 py-2.5 rounded-xl font-mono text-xs font-bold transition-all border border-cyan-500/40 bg-cyan-950/50 text-neon-cyan hover:bg-cyan-900/50"
      >
        ↻ Tentar Novamente
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import FeedCard from '../components/FeedCard.vue'
import VoidGlyph from '../components/VoidGlyph.vue'

const props = defineProps({
  category:  { type: String, required: true },
  slug:      { type: String, required: true },
  voidShape: { type: String, default: 'cluster' },
  catColor:  { type: String, default: '#00fff5' },
})

const API_BASE = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL) || 'http://localhost:8000'

const articles = ref([])
const loading  = ref(true)

const shapeMap = {
  'politica': 'shield',
  'economia': 'pix-dre',
  'esportes': 'daw',
  'tecnologia': 'nvme',
  'mundo': 'globe',
  'positivas': 'positive',
}

const voidShape = computed(() => props.voidShape || shapeMap[props.slug] || 'cluster')

async function load() {
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/feeds/${props.slug}?limit=18`)
    if (res.ok) {
      articles.value = await res.json()
    } else {
      articles.value = []
    }
  } catch (e) {
    console.warn(`[CategoryView] failed to load feed for ${props.slug}`, e)
    articles.value = []
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => props.slug, load)
</script>
