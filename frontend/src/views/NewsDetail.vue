<template>
  <div class="max-w-3xl mx-auto">

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
        class="flex items-center gap-2 text-sm mb-8 transition-colors hover:opacity-100"
        style="color: var(--text-muted);"
      >
        ← Voltar
      </button>

      <!-- Category + Date -->
      <div class="flex items-center gap-3 flex-wrap mb-4">
        <span
          class="text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-full"
          :style="`background: ${catBg}; color: ${catColor};`"
        >{{ article.category || 'Geral' }}</span>
        <time class="font-mono-jp text-xs" style="color: var(--text-muted);">
          {{ formatDate(article.created_at) }}
        </time>
      </div>

      <!-- Title -->
      <h1 class="font-editorial text-3xl md:text-4xl font-bold leading-tight mb-8"
          style="color: var(--text-primary);">
        {{ article.title }}
      </h1>

      <!-- Hero Image -->
      <div v-if="article.image_url" class="w-full rounded-2xl overflow-hidden mb-8" style="max-height: 420px;">
        <img
          :src="article.image_url"
          :alt="article.title"
          class="w-full h-full object-cover"
          style="max-height: 420px;"
        />
      </div>

      <!-- Divider -->
      <hr style="border-color: var(--border); margin-bottom: 2rem;" />

      <!-- Content (HTML from Quill editor) -->
      <div class="article-content" v-html="article.content"></div>

      <!-- Footer bar -->
      <div
        class="mt-12 pt-6 flex items-center justify-between flex-wrap gap-4"
        style="border-top: 1px solid var(--border);"
      >
        <router-link to="/" class="text-sm font-semibold transition-colors hover:opacity-80" style="color: var(--brand);">
          ← Voltar ao Início
        </router-link>
        <span class="font-mono-jp text-xs" style="color: var(--text-muted);">
          Publicado em {{ formatDate(article.created_at) }}
        </span>
      </div>

    </article>

    <!-- ── Not Found ─────────────────────────────────────────────────────────── -->
    <div v-else class="text-center py-24" style="color: var(--text-muted);">
      <span class="text-6xl block mb-6">🔍</span>
      <h1 class="text-2xl font-bold mb-3" style="color: var(--text-primary);">Notícia não encontrada</h1>
      <p class="mb-6">Esta matéria pode ter sido removida ou o link está incorreto.</p>
      <router-link
        to="/"
        class="inline-block px-6 py-3 rounded-xl font-bold text-sm transition-colors"
        style="background: var(--brand); color: white;"
      >
        ← Voltar ao Início
      </router-link>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useHead } from '@unhead/vue'

const route   = useRoute()
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const article = ref(null)
const loading = ref(true)

// ── SEO ───────────────────────────────────────────────────────────────────────
useHead(
  computed(() => ({
    title: article.value
      ? `${article.value.title} — JovemPano`
      : 'Matéria — JovemPano',
    meta: article.value
      ? [{ name: 'description', content: article.value.content?.replace(/<[^>]*>/g, '').slice(0, 155) }]
      : [],
  }))
)

// ── Category colors ────────────────────────────────────────────────────────────
const CAT_COLORS = {
  'Política':       { color: 'var(--cat-politica)',       bg: 'var(--cat-politica-bg)' },
  'Economia':       { color: 'var(--cat-economia)',       bg: 'var(--cat-economia-bg)' },
  'Esportes':       { color: 'var(--cat-esportes)',       bg: 'var(--cat-esportes-bg)' },
  'Tecnologia':     { color: 'var(--cat-tecnologia)',     bg: 'var(--cat-tecnologia-bg)' },
  'Mundo':          { color: 'var(--cat-mundo)',          bg: 'var(--cat-mundo-bg)' },
  'Entretenimento': { color: 'var(--cat-entretenimento)', bg: 'var(--cat-entretenimento-bg)' },
  'Geral':          { color: 'var(--cat-geral)',          bg: 'var(--cat-geral-bg)' },
}
const catColor = computed(() => CAT_COLORS[article.value?.category]?.color || 'var(--cat-geral)')
const catBg    = computed(() => CAT_COLORS[article.value?.category]?.bg    || 'var(--cat-geral-bg)')

// ── Helpers ───────────────────────────────────────────────────────────────────
const formatDate = (d) => {
  if (!d) return ''
  try {
    return new Date(d).toLocaleString('pt-BR', {
      day: '2-digit', month: 'long', year: 'numeric',
      hour: '2-digit', minute: '2-digit',
    })
  } catch { return '' }
}

// ── Lifecycle ─────────────────────────────────────────────────────────────────
onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE}/news/${route.params.id}`)
    if (res.ok) {
      article.value = await res.json()
    }
  } catch (e) {
    console.warn('[NewsDetail] fetch failed', e)
  } finally {
    loading.value = false
  }
})
</script>
