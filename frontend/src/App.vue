<template>
  <div v-if="isAdminRoute" class="admin-layout">
    <router-view />
  </div>
  <div v-else style="background: var(--bg-base); min-height: 100vh;">

    <!-- ═══════ HEADER ═══════ -->
    <header class="sticky top-0 z-50 transition-all duration-300" style="background: rgba(9,9,11,0.9); border-bottom: 1px solid var(--border); backdrop-filter: blur(16px);">
      <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        
        <!-- Left: Live indicator + Date -->
        <div class="flex-1 flex flex-col justify-center">
          <div class="flex items-center gap-2">
            <span class="pulse-live w-2 h-2 rounded-full" style="background: var(--brand);"></span>
            <span class="font-mono-jp text-[10px] font-bold tracking-widest uppercase" style="color: var(--brand);">Ao Vivo</span>
          </div>
          <span class="font-mono-jp text-[10px] uppercase tracking-widest" style="color: var(--text-muted); line-height: 1;">{{ formattedDate }}</span>
        </div>

        <!-- Center: Logo -->
        <div class="flex-shrink-0 flex justify-center">
          <router-link to="/" class="flex items-center gap-2 group transition-transform hover:scale-105" aria-label="JovemPano">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center text-white font-black text-sm shadow-lg shadow-violet-500/20" style="background: linear-gradient(135deg, var(--brand), #ec4899);">
              JP
            </div>
            <h1 class="text-2xl font-black tracking-tight leading-none pt-0.5">
              <span style="color: var(--text-primary);">Jovem</span><span style="color: var(--brand);">Pano</span>
            </h1>
          </router-link>
        </div>

        <!-- Right: Spacer for perfect centering -->
        <div class="flex-1 hidden md:block"></div>
        
      </div>
    </header>

    <!-- ═══════ CATEGORY NAV ═══════ -->
    <nav
      class="sticky z-40 transition-all duration-300"
      style="top: 64px; background: rgba(9,9,11,0.9); border-bottom: 1px solid var(--border); backdrop-filter: blur(16px);"
    >
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex overflow-x-auto scrollbar-hide justify-center gap-2 py-1">
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
          © {{ year }} JovemPano · Conteúdo de terceiros via RSS · Desenvolvido por OrbeSystems
        </p>
      </div>
    </footer>

    <!-- Cookie Banner -->
    <CookieBanner />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import CookieBanner from './components/CookieBanner.vue'

const route = useRoute()
const year = new Date().getFullYear()

const isAdminRoute = computed(() => route?.path === '/admin')

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
