<template>
  <div style="background: var(--bg-base); min-height: 100vh;">

    <!-- ═══════ HEADER ═══════ -->
    <header class="sticky top-0 z-50" style="background: var(--bg-surface); border-bottom: 1px solid var(--border); backdrop-filter: blur(12px);">
      <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">

        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-3 group" aria-label="JovemPano — Início">
          <div
            class="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 transition-transform group-hover:scale-95"
            style="background: var(--brand);"
          >
            <span class="text-white font-black text-sm select-none">JP</span>
          </div>
          <h1 class="text-xl font-black tracking-tight leading-none">
            <span style="color: var(--text-primary);">Jovem</span><span style="color: var(--brand);">Pano</span>
          </h1>
        </router-link>

        <!-- Live indicator + Date (desktop) -->
        <div class="hidden md:flex items-center gap-5">
          <div class="flex items-center gap-2">
            <span
              class="pulse-live w-2 h-2 rounded-full flex-shrink-0"
              style="background: var(--brand); display: inline-block;"
            ></span>
            <span class="font-mono-jp text-xs font-medium" style="color: var(--brand);">AO VIVO</span>
          </div>
          <span class="font-mono-jp text-xs" style="color: var(--text-muted);">{{ formattedDate }}</span>
        </div>

      </div>
    </header>

    <!-- ═══════ CATEGORY NAV ═══════ -->
    <nav
      class="sticky z-40"
      style="top: 57px; background: var(--bg-surface); border-bottom: 1px solid var(--border);"
    >
      <div class="max-w-7xl mx-auto px-2">
        <div class="flex overflow-x-auto scrollbar-hide">
          <router-link
            v-for="btn in navButtons"
            :key="btn.path"
            :to="btn.path"
            :id="`nav-${btn.label.toLowerCase()}`"
            :class="['tab-btn', isActive(btn.path) ? 'active' : '']"
            :style="isActive(btn.path) ? `color: ${btn.color};` : ''"
          >
            <span>{{ btn.emoji }}</span>{{ btn.label }}
          </router-link>

          <!-- Admin link (al right, muted) -->
          <router-link
            to="/admin"
            id="nav-admin"
            class="tab-btn ml-auto"
            :class="isActive('/admin') ? 'active' : ''"
            style="opacity: 0.45;"
          >
            ⚙️ Admin
          </router-link>
        </div>
      </div>
    </nav>

    <!-- ═══════ MAIN ═══════ -->
    <main class="max-w-7xl mx-auto px-4 py-8">
      <router-view />
    </main>

    <!-- ═══════ FOOTER ═══════ -->
    <footer class="mt-20" style="background: var(--bg-surface); border-top: 1px solid var(--border);">
      <div class="max-w-7xl mx-auto px-4 py-8 flex flex-col md:flex-row justify-between items-center gap-3">
        <div class="flex items-center gap-2">
          <span class="font-black text-lg" style="color: var(--text-primary);">
            Jovem<span style="color: var(--brand);">Pano</span>
          </span>
          <span class="text-xs" style="color: var(--text-muted);">— Notícias em Tempo Real</span>
        </div>
        <p class="text-xs text-center" style="color: var(--text-muted);">
          © {{ year }} JovemPano · Conteúdo de terceiros via RSS · Desenvolvido por Antigravity
        </p>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const year = new Date().getFullYear()

const navButtons = [
  { path: '/',           label: 'Início',     emoji: '🏠', color: 'var(--brand)' },
  { path: '/politica',   label: 'Política',   emoji: '🏛️', color: 'var(--cat-politica)' },
  { path: '/economia',   label: 'Economia',   emoji: '📈', color: 'var(--cat-economia)' },
  { path: '/esportes',   label: 'Esportes',   emoji: '⚽', color: 'var(--cat-esportes)' },
  { path: '/tecnologia', label: 'Tecnologia', emoji: '💻', color: 'var(--cat-tecnologia)' },
  { path: '/mundo',      label: 'Mundo',      emoji: '🌐', color: 'var(--cat-mundo)' },
]

const isActive = (path) => {
  if (!route?.path) return false
  return route.path === path
}

const formattedDate = computed(() =>
  new Date().toLocaleDateString('pt-BR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
)
</script>
