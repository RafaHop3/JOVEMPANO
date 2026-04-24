<template>
  <div v-if="isAdminRoute" class="admin-layout">
    <router-view />
  </div>
  <div v-else class="min-h-screen">

    <!-- ═══════ HEADER (Aero Glass) ═══════ -->
    <header
      class="sticky top-0 z-50 transition-all duration-300"
      style="
        background: rgba(255, 255, 255, 0.70);
        border-bottom: 1px solid rgba(255,255,255,0.60);
        backdrop-filter: blur(20px) saturate(200%);
        -webkit-backdrop-filter: blur(20px) saturate(200%);
        box-shadow: 0 2px 0 rgba(255,255,255,0.9) inset, 0 4px 20px rgba(30,100,200,0.10);
      "
    >
      <div class="max-w-7xl mx-auto px-3 sm:px-4 h-16 flex items-center justify-between gap-2">

        <!-- Left: Live indicator + Date -->
        <div class="flex-1 flex flex-col justify-center min-w-0">
          <div class="flex items-center gap-2">
            <span class="pulse-live w-2.5 h-2.5 rounded-full flex-shrink-0" style="background: var(--brand); display: inline-block;"></span>
            <span class="text-[10px] font-extrabold tracking-widest uppercase" style="color: var(--brand);">Ao Vivo</span>
          </div>
          <span class="text-[10px] uppercase tracking-widest truncate pr-2" style="color: var(--text-muted); font-weight: 600; line-height: 1;">{{ formattedDate }}</span>
        </div>

        <!-- Center: Logo Aero Glossy -->
        <div class="flex-shrink-0 flex justify-center">
          <router-link to="/" class="flex items-center gap-2.5 group transition-transform hover:scale-105" aria-label="JovemPano">
            <div
              class="w-9 h-9 rounded-xl flex items-center justify-center text-white font-black text-sm"
              style="
                background: linear-gradient(180deg,
                  rgba(100,180,255,0.95) 0%,
                  rgba(30,144,255,0.90) 48%,
                  rgba(0,100,220,0.95) 49%,
                  rgba(0,80,200,1) 100%
                );
                box-shadow: 0 1px 0 rgba(255,255,255,0.8) inset, 0 4px 14px rgba(30,144,255,0.40);
                border: 1px solid rgba(100,180,255,0.5);
              "
            >JP</div>
            <h1 class="text-xl sm:text-2xl font-black tracking-tight leading-none pt-0.5">
              <span style="color: var(--text-primary);">Jovem</span><span style="color: var(--brand);">Pano</span>
            </h1>
          </router-link>
        </div>

        <!-- Right: Spacer -->
        <div class="flex-1"></div>

      </div>
    </header>

    <!-- ═══════ CATEGORY NAV (Aero frosted) ═══════ -->
    <nav
      class="sticky z-40 transition-all duration-300"
      style="
        top: 64px;
        background: rgba(255, 255, 255, 0.60);
        border-bottom: 1px solid rgba(255,255,255,0.55);
        backdrop-filter: blur(14px) saturate(180%);
        -webkit-backdrop-filter: blur(14px) saturate(180%);
        box-shadow: 0 1px 0 rgba(255,255,255,0.8) inset, 0 2px 12px rgba(30,100,200,0.07);
      "
    >
      <div class="max-w-7xl mx-auto px-3 sm:px-4">
        <div class="flex overflow-x-auto scrollbar-hide justify-start md:justify-center gap-2 py-1">
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

    <!-- ═══════ FOOTER (Aero glass) ═══════ -->
    <footer
      class="mt-20"
      style="
        background: rgba(255,255,255,0.65);
        border-top: 1px solid rgba(255,255,255,0.60);
        backdrop-filter: blur(16px);
        box-shadow: 0 -4px 20px rgba(30,100,200,0.06);
      "
    >
      <div class="max-w-7xl mx-auto px-4 py-8 flex flex-col md:flex-row justify-between items-center gap-3">
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 rounded-lg flex items-center justify-center text-white text-[10px] font-black"
            style="background: linear-gradient(180deg, #64b4ff 0%, #1e90ff 50%, #0050c8 100%);
                   box-shadow: 0 1px 0 rgba(255,255,255,0.7) inset;">JP</div>
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
