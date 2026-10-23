<template>
  <div v-if="isAdminRoute" class="admin-layout">
    <router-view />
  </div>
  <div v-else class="min-h-screen bg-[#030508] text-[#c8d6e3] flex flex-col justify-between">

    <!-- ═══════ HEADER (Orbe Systems Cyber-Glass) ═══════ -->
    <header
      class="sticky top-0 z-50 transition-all duration-300 border-b border-cyan-500/20 bg-[#030508]/85 backdrop-blur-xl shadow-lg"
    >
      <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between gap-4">

        <!-- Left: Live terminal indicator + Date -->
        <div class="flex-1 flex flex-col justify-center min-w-0">
          <div class="flex items-center gap-2">
            <span class="pulse-live w-2 h-2 rounded-full flex-shrink-0 bg-neon-cyan"></span>
            <span class="text-[10px] font-mono font-extrabold tracking-widest uppercase text-neon-cyan">
              AO VIVO // RADAR 24/7
            </span>
          </div>
          <span class="text-[10px] font-mono uppercase tracking-widest text-slate-400 truncate">
            {{ formattedDate }}
          </span>
        </div>

        <!-- Center: Logo Orbe Systems Cyber Aesthetic -->
        <div class="flex-shrink-0 flex justify-center">
          <router-link to="/" class="flex items-center gap-3 group transition-transform hover:scale-105" aria-label="Orbe News JovemPano">
            <div
              class="w-9 h-9 rounded-xl flex items-center justify-center text-black font-black text-sm bg-gradient-to-tr from-cyan-400 to-sky-400 shadow-neon-cyan border border-cyan-300"
            >
              JP
            </div>
            <div class="flex flex-col">
              <span class="text-xl sm:text-2xl font-black font-editorial tracking-tight text-white leading-none">
                Jovem<span class="text-neon-cyan">Pano</span>
              </span>
              <span class="text-[9px] font-mono text-cyan-400/80 tracking-widest uppercase mt-0.5">
                Powered by Orbe Systems
              </span>
            </div>
          </router-link>
        </div>

        <!-- Right: Official Orbe Systems Hub Link -->
        <div class="flex-1 flex justify-end items-center gap-3">
          <a
            href="https://orbesystems.com.br"
            target="_blank"
            rel="noopener noreferrer"
            class="hidden sm:inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-mono text-cyan-300 hover:text-white border border-cyan-500/30 hover:border-cyan-400 bg-cyan-950/40 transition-all"
          >
            <span>Orbe Systems Hub</span>
            <span class="text-neon-cyan font-bold">↗</span>
          </a>
        </div>

      </div>
    </header>

    <!-- ═══════ CATEGORY NAV (Void Glyphs no lugar de emojis) ═══════ -->
    <nav
      class="sticky z-40 transition-all duration-300 border-b border-cyan-500/15 bg-[#050811]/90 backdrop-blur-md"
      style="top: 64px;"
    >
      <div class="max-w-7xl mx-auto px-3 sm:px-4">
        <div class="flex overflow-x-auto scrollbar-hide justify-start md:justify-center gap-2 py-1.5">
          <router-link
            v-for="btn in navButtons"
            :key="btn.path"
            :to="btn.path"
            :id="`nav-${btn.label.toLowerCase()}`"
            :class="['tab-btn', isActive(btn.path) ? 'active' : '']"
            :style="isActive(btn.path) ? `color: ${btn.color}; border-color: ${btn.color}40;` : ''"
          >
            <!-- Void Glyph 3D/Canvas no lugar de emoji -->
            <VoidGlyph :shape="btn.voidShape" :color="btn.color" :size="18" />
            <span>{{ btn.label }}</span>
          </router-link>
        </div>
      </div>
    </nav>

    <!-- ═══════ MAIN VIEW ═══════ -->
    <main class="max-w-7xl mx-auto px-4 py-8 flex-1 w-full">
      <router-view />
    </main>

    <!-- ═══════ FOOTER (Orbe Systems Style) ═══════ -->
    <footer
      class="mt-20 border-t border-cyan-500/20 bg-[#020306]/95 backdrop-blur-xl"
    >
      <div class="max-w-7xl mx-auto px-4 py-10 flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="flex flex-col sm:flex-row items-center gap-4 text-center sm:text-left">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center text-black text-xs font-black bg-neon-cyan shadow-neon-cyan">
            JP
          </div>
          <div>
            <div class="font-bold text-base text-white font-editorial">
              Jovem<span class="text-neon-cyan">Pano</span>
              <span class="text-xs font-mono text-slate-400 font-normal ml-2">// Orbe Systems Protocol</span>
            </div>
            <p class="text-xs text-slate-400 font-mono mt-0.5">
              Hub Tecnológico: notícias em tempo real, curadoria editorial e automação SecDevOps.
            </p>
          </div>
        </div>

        <!-- Badges & Links -->
        <div class="flex flex-col items-center md:items-end gap-2 text-xs font-mono text-slate-400">
          <div class="flex items-center gap-3 flex-wrap justify-center">
            <a href="https://orbesystems.com.br" target="_blank" rel="noopener noreferrer" class="hover:text-neon-cyan transition-colors">
              orbesystems.com.br
            </a>
            <span class="text-slate-600">·</span>
            <a href="https://inho.orbesystems.com.br" target="_blank" rel="noopener noreferrer" class="hover:text-neon-cyan transition-colors">
              inho.orbesystems.com.br
            </a>
            <span class="text-slate-600">·</span>
            <a href="https://orbesystems.com.br/privacidade" target="_blank" rel="noopener noreferrer" class="hover:text-neon-cyan transition-colors">
              Privacidade (LGPD)
            </a>
            <span class="text-slate-600">·</span>
            <a href="https://orbesystems.com.br/termos" target="_blank" rel="noopener noreferrer" class="hover:text-neon-cyan transition-colors">
              Termos
            </a>
          </div>
          <p class="text-[11px] text-slate-500">
            © {{ year }} Orbe Systems Technologies · Todos os direitos reservados.
          </p>
        </div>
      </div>
    </footer>

    <!-- Cookie Banner LGPD Art. 8º -->
    <CookieBanner />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import CookieBanner from './components/CookieBanner.vue'
import VoidGlyph from './components/VoidGlyph.vue'

const route = useRoute()
const year = new Date().getFullYear()

const isAdminRoute = computed(() => route?.path === '/admin')

// Nav Buttons: todos usando formas geométricas de Voids no lugar de emotions
const navButtons = [
  { path: '/',           label: 'Início',     voidShape: 'cluster',  color: '#00fff5' },
  { path: '/politica',   label: 'Política',   voidShape: 'shield',   color: '#f43f5e' },
  { path: '/economia',   label: 'Economia',   voidShape: 'pix-dre',  color: '#10b981' },
  { path: '/esportes',   label: 'Esportes',   voidShape: 'daw',      color: '#f59e0b' },
  { path: '/tecnologia', label: 'Tecnologia', voidShape: 'nvme',     color: '#00fff5' },
  { path: '/mundo',      label: 'Mundo',      voidShape: 'globe',    color: '#3b82f6' },
  { path: '/positivas',  label: 'Positivas',  voidShape: 'positive', color: '#10b981' },
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
