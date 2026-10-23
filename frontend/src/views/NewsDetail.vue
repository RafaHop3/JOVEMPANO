<template>
  <div class="max-w-3xl mx-auto pb-12">
    <!-- ── Progress Bar ──────────────────────────────────────────────────────── -->
    <div
      class="fixed top-0 left-0 h-1 z-50 transition-all duration-150 ease-out bg-neon-cyan shadow-[0_0_10px_#00fff5]"
      :style="{ width: `${scrollProgress}%` }"
    ></div>

    <!-- ── Loading ──────────────────────────────────────────────────────────── -->
    <div v-if="loading" class="flex flex-col gap-6">
      <div class="skeleton" style="height: 380px;"></div>
      <div class="skeleton" style="height: 32px; width: 70%;"></div>
      <div class="skeleton" style="height: 14px; width: 40%;"></div>
      <div class="flex flex-col gap-3 mt-2">
        <div v-for="i in 8" :key="i" class="skeleton" style="height: 14px;"></div>
      </div>
    </div>

    <!-- ── Article ───────────────────────────────────────────────────────────── -->
    <article v-else-if="article" class="fade-up">

      <!-- Back -->
      <button
        id="btn-back"
        @click="$router.back()"
        class="flex items-center gap-2 text-xs font-mono mb-8 text-slate-400 hover:text-neon-cyan transition-colors"
      >
        ← Voltar ao radar
      </button>

      <!-- Category + Date -->
      <div class="flex items-center gap-3 flex-wrap mb-4">
        <span
          class="text-[10px] font-mono font-black uppercase tracking-widest px-3 py-1 rounded-md border border-cyan-500/30"
          :style="`background: ${catBg}; color: ${catColor};`"
        >{{ article.category || 'Geral' }}</span>
        <time class="font-mono text-xs text-slate-400">
          {{ formatDate(article.created_at) }}
        </time>
      </div>

      <!-- Title -->
      <h1 class="font-editorial text-3xl md:text-4xl font-bold leading-tight mb-8 text-white">
        {{ article.title }}
      </h1>

      <!-- Hero Image -->
      <div v-if="article.image_url" class="w-full rounded-2xl overflow-hidden mb-8 border border-cyan-500/20 bg-slate-950" style="max-height: 420px;">
        <img
          :src="article.image_url"
          :alt="article.title"
          class="w-full h-full object-cover"
          style="max-height: 420px;"
        />
      </div>

      <!-- Divider -->
      <div class="w-full h-px bg-cyan-500/20 mb-8"></div>

      <!-- Content -->
      <div class="article-content leading-relaxed" v-html="sanitizedContent"></div>

      <!-- Bottom link to Orbe Systems -->
      <div class="mt-12 p-6 rounded-2xl border border-cyan-500/20 bg-slate-950/60 flex flex-col sm:flex-row justify-between items-center gap-4">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-neon-cyan text-black font-black flex items-center justify-center text-xs">
            JP
          </div>
          <div>
            <div class="text-sm font-bold text-white font-editorial">Central Orbe Systems</div>
            <p class="text-xs text-slate-400 font-mono">Tecnologia, inovação contábil e cibersegurança.</p>
          </div>
        </div>
        <a
          href="https://orbesystems.com.br"
          target="_blank"
          rel="noopener noreferrer"
          class="px-4 py-2 rounded-lg font-mono text-xs font-bold text-black bg-neon-cyan hover:brightness-110 shadow-neon-cyan transition-all"
        >
          Explorar Soluções ↗
        </a>
      </div>

    </article>

    <!-- ── Error ─────────────────────────────────────────────────────────────── -->
    <div v-else class="text-center py-24 text-slate-400 rounded-2xl border border-cyan-500/20 bg-slate-950/40">
      <p class="text-base font-semibold text-white mb-2">Matéria não encontrada</p>
      <p class="text-xs text-slate-400 mb-6">A publicação pode ter sido arquivada ou removida.</p>
      <router-link to="/" class="text-xs font-mono text-neon-cyan hover:underline">
        ← Voltar ao início
      </router-link>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const API_BASE = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL) || 'http://localhost:8000'

const article = ref(null)
const loading = ref(true)
const scrollProgress = ref(0)

const CAT_COLORS = {
  'Política':       { color: '#f43f5e', bg: 'rgba(244, 63, 94, 0.15)' },
  'Politica':       { color: '#f43f5e', bg: 'rgba(244, 63, 94, 0.15)' },
  'Economia':       { color: '#10b981', bg: 'rgba(16, 185, 129, 0.15)' },
  'Esportes':       { color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.15)' },
  'Tecnologia':     { color: '#00fff5', bg: 'rgba(0, 255, 245, 0.15)' },
  'Mundo':          { color: '#3b82f6', bg: 'rgba(59, 130, 246, 0.15)' },
  'Entretenimento': { color: '#a855f7', bg: 'rgba(168, 85, 247, 0.15)' },
  'Geral':          { color: '#7eb8e0', bg: 'rgba(126, 184, 224, 0.15)' },
}

const catColor = computed(() => CAT_COLORS[article.value?.category]?.color || '#00fff5')
const catBg    = computed(() => CAT_COLORS[article.value?.category]?.bg    || 'rgba(0, 255, 245, 0.15)')

const sanitizedContent = computed(() => {
  return article.value?.content || ''
})

const formatDate = (d) => {
  if (!d) return ''
  try {
    return new Date(d).toLocaleDateString('pt-BR', {
      day: '2-digit', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit'
    })
  } catch { return '' }
}

const handleScroll = () => {
  const total = document.documentElement.scrollHeight - window.innerHeight
  if (total > 0) {
    scrollProgress.value = (window.scrollY / total) * 100
  }
}

onMounted(async () => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  try {
    const res = await fetch(`${API_BASE}/news/${route.params.id}`)
    if (res.ok) {
      article.value = await res.json()
    }
  } catch (e) {
    console.warn('[NewsDetail] error loading article', e)
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
