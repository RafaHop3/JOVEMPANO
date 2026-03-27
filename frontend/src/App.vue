<template>
  <div class="min-h-screen bg-white relative">
    <!-- ═══════ JELLYFISH BACKGROUND ANIMATION ═══════ -->
    <JellyfishBg />

    <!-- ═══════ SIDE DECORATIONS (Gold) ═══════ -->
    <!-- Left Side -->
    <div class="fixed left-0 top-0 w-10 h-full z-40 pointer-events-none hidden xl:block">
      <div class="h-full w-full bg-gradient-to-b from-amber-50/60 via-white/30 to-amber-50/60 border-r border-amber-200/40 flex flex-col items-center justify-between py-8">
        <div class="flex flex-col items-center gap-1">
          <div class="w-px h-20 bg-gradient-to-b from-transparent via-amber-400/50 to-transparent"></div>
          <div class="w-2 h-2 bg-amber-400/60 rounded-full"></div>
          <div class="w-px h-8 bg-amber-300/40"></div>
          <div class="w-1.5 h-1.5 bg-amber-500/50 rotate-45"></div>
          <div class="w-px h-8 bg-amber-300/40"></div>
          <div class="w-2 h-2 bg-amber-400/60 rounded-full"></div>
          <div class="w-px h-20 bg-gradient-to-b from-transparent via-amber-400/50 to-transparent"></div>
        </div>
        <div class="flex flex-col items-center gap-3">
          <div class="w-1 h-1 bg-amber-300/40 rounded-full"></div>
          <div class="w-px h-12 bg-amber-200/30"></div>
          <div class="w-1.5 h-1.5 bg-amber-400/40 rotate-45"></div>
          <div class="w-px h-12 bg-amber-200/30"></div>
          <div class="w-1 h-1 bg-amber-300/40 rounded-full"></div>
        </div>
        <div class="flex flex-col items-center gap-1">
          <div class="w-px h-20 bg-gradient-to-b from-transparent via-amber-400/50 to-transparent"></div>
          <div class="w-2 h-2 bg-amber-400/60 rounded-full"></div>
          <div class="w-px h-8 bg-amber-300/40"></div>
          <div class="w-1.5 h-1.5 bg-amber-500/50 rotate-45"></div>
          <div class="w-px h-8 bg-amber-300/40"></div>
          <div class="w-2 h-2 bg-amber-400/60 rounded-full"></div>
          <div class="w-px h-20 bg-gradient-to-b from-transparent via-amber-400/50 to-transparent"></div>
        </div>
      </div>
    </div>
    
    <!-- Right Side -->
    <div class="fixed right-0 top-0 w-10 h-full z-40 pointer-events-none hidden xl:block">
      <div class="h-full w-full bg-gradient-to-b from-amber-50/60 via-white/30 to-amber-50/60 border-l border-amber-200/40 flex flex-col items-center justify-between py-8">
        <div class="flex flex-col items-center gap-1">
          <div class="w-px h-20 bg-gradient-to-b from-transparent via-amber-400/50 to-transparent"></div>
          <div class="w-2 h-2 bg-amber-400/60 rounded-full"></div>
          <div class="w-px h-8 bg-amber-300/40"></div>
          <div class="w-1.5 h-1.5 bg-amber-500/50 rotate-45"></div>
          <div class="w-px h-8 bg-amber-300/40"></div>
          <div class="w-2 h-2 bg-amber-400/60 rounded-full"></div>
          <div class="w-px h-20 bg-gradient-to-b from-transparent via-amber-400/50 to-transparent"></div>
        </div>
        <div class="flex flex-col items-center gap-3">
          <div class="w-1 h-1 bg-amber-300/40 rounded-full"></div>
          <div class="w-px h-12 bg-amber-200/30"></div>
          <div class="w-1.5 h-1.5 bg-amber-400/40 rotate-45"></div>
          <div class="w-px h-12 bg-amber-200/30"></div>
          <div class="w-1 h-1 bg-amber-300/40 rounded-full"></div>
        </div>
        <div class="flex flex-col items-center gap-1">
          <div class="w-px h-20 bg-gradient-to-b from-transparent via-amber-400/50 to-transparent"></div>
          <div class="w-2 h-2 bg-amber-400/60 rounded-full"></div>
          <div class="w-px h-8 bg-amber-300/40"></div>
          <div class="w-1.5 h-1.5 bg-amber-500/50 rotate-45"></div>
          <div class="w-px h-8 bg-amber-300/40"></div>
          <div class="w-2 h-2 bg-amber-400/60 rounded-full"></div>
          <div class="w-px h-20 bg-gradient-to-b from-transparent via-amber-400/50 to-transparent"></div>
        </div>
      </div>
    </div>

    <!-- ═══════ HEADER ═══════ -->
    <header class="border-b border-slate-200 bg-white/95 backdrop-blur sticky top-0 z-50 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <!-- Brand with Logo -->
        <router-link to="/" class="flex items-center gap-3 hover:opacity-90 transition-opacity">
          <img src="/images/logo.png" alt="JovemPano" class="w-10 h-10 object-contain" />
          <h1 class="text-2xl font-extrabold tracking-tight">
            <span class="text-blue-600">Jovem</span><span class="text-amber-500">Pano</span>
          </h1>
        </router-link>
        <span class="text-xs text-slate-400 hidden md:block font-mono">{{ formattedDate }}</span>
      </div>
    </header>

    <!-- ═══════ CLASSIC NAVIGATION BAR ═══════ -->
    <nav class="bg-white/90 backdrop-blur border-b border-slate-200 shadow-sm sticky top-[57px] z-40">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex items-center gap-1 overflow-x-auto scrollbar-hide py-1">
          <router-link 
            v-for="btn in navButtons" 
            :key="btn.path" 
            :to="btn.path"
            :class="[
              'nav-btn flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-semibold transition-all whitespace-nowrap border',
              isActive(btn.path) 
                ? `${btn.activeBg} ${btn.activeText} border-current shadow-sm` 
                : 'text-slate-600 hover:text-slate-900 border-transparent hover:bg-slate-50 hover:border-slate-200'
            ]"
          >
            <span class="text-base">{{ btn.icon }}</span>
            {{ btn.label }}
          </router-link>
        </div>
      </div>
    </nav>

    <!-- ═══════ MAIN CONTENT ═══════ -->
    <main class="max-w-7xl mx-auto px-4 py-10 relative z-10">
      <router-view></router-view>
    </main>

    <!-- ═══════ FOOTER ═══════ -->
    <footer class="bg-white border-t border-slate-200 mt-16 relative z-10">
      <div class="max-w-7xl mx-auto px-4 py-8">
        <div class="flex flex-col md:flex-row justify-between items-center gap-4">
          <div class="flex items-center gap-3">
            <img src="/images/logo.png" alt="JovemPano" class="w-8 h-8 object-contain opacity-70" />
            <div>
              <h3 class="text-lg font-extrabold"><span class="text-blue-600">Jovem</span><span class="text-amber-500">Pano</span></h3>
              <p class="text-xs text-slate-400 mt-0.5">Informação sem filtro, com a velocidade que o Brasil exige.</p>
            </div>
          </div>
          <div class="flex gap-6">
            <router-link v-for="btn in navButtons" :key="btn.path" :to="btn.path" class="text-xs text-slate-400 hover:text-blue-600 transition-colors font-medium uppercase tracking-wider">
              {{ btn.label }}
            </router-link>
          </div>
        </div>
        <div class="mt-6 pt-4 border-t border-slate-100 flex justify-between items-center">
          <p class="text-xs text-slate-300">© 2026 JovemPano. Todos os direitos reservados.</p>
          <div class="flex gap-1">
            <div class="w-1.5 h-1.5 bg-blue-300 rotate-45"></div>
            <div class="w-1.5 h-1.5 bg-amber-400 rotate-45"></div>
            <div class="w-1.5 h-1.5 bg-blue-500 rotate-45"></div>
          </div>
        </div>
      </div>
    </footer>

    <CookieBanner />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import CookieBanner from './components/CookieBanner.vue'
import JellyfishBg from './components/JellyfishBg.vue'

const route = useRoute()

const navButtons = [
  { path: '/',               icon: '🏠', label: 'Início',         activeBg: 'bg-blue-50',     activeText: 'text-blue-700' },
  { path: '/politica',       icon: '🏛️', label: 'Política',       activeBg: 'bg-rose-50',     activeText: 'text-rose-700' },
  { path: '/economia',       icon: '📈', label: 'Economia',       activeBg: 'bg-amber-50',    activeText: 'text-amber-700' },
  { path: '/esportes',       icon: '⚽', label: 'Esportes',       activeBg: 'bg-emerald-50',  activeText: 'text-emerald-700' },
  { path: '/tecnologia',     icon: '💻', label: 'Tecnologia',     activeBg: 'bg-violet-50',   activeText: 'text-violet-700' },
  { path: '/entretenimento', icon: '🎬', label: 'Entretenimento', activeBg: 'bg-pink-50',     activeText: 'text-pink-700' },
  { path: '/mundo',          icon: '🌍', label: 'Mundo',          activeBg: 'bg-sky-50',      activeText: 'text-sky-700' },
]

const isActive = (path) => route.path === path

const formattedDate = computed(() => {
  return new Date().toLocaleDateString('pt-BR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
})
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.nav-btn {
  position: relative;
}
.nav-btn::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 50%;
  transform: translateX(-50%) scaleX(0);
  width: 60%;
  height: 2px;
  background: currentColor;
  transition: transform 0.3s ease;
  border-radius: 2px;
}
.nav-btn:hover::after,
.nav-btn.router-link-exact-active::after {
  transform: translateX(-50%) scaleX(1);
}
</style>
