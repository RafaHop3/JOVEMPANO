<template>
  <div class="relative w-full rounded-2xl glass-magnetic overflow-hidden border border-cyan-500/30 p-6 md:p-8 shadow-neon-cyan">
    <!-- Cyberpunk grid overlay & glow -->
    <div class="absolute inset-0 bg-gradient-to-r from-cyan-950/20 via-transparent to-blue-950/30 pointer-events-none"></div>
    <div class="absolute top-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20"></div>

    <div class="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
      <!-- Left side: Information, Badges & CTAs -->
      <div class="lg:col-span-7 flex flex-col gap-4">
        <!-- Tagline / Homologation -->
        <div class="flex items-center gap-3 flex-wrap">
          <span class="inline-flex items-center gap-2 px-3 py-1 rounded-md text-[11px] font-mono font-bold tracking-widest uppercase bg-cyan-950/60 text-neon-cyan border border-cyan-500/30">
            <span class="w-2 h-2 rounded-full bg-neon-cyan animate-pulse"></span>
            PRODUTO HOMOLOGADO // ORBE SYSTEMS
          </span>
          <span class="text-xs font-mono text-slate-400">
            [ SECDEVOPS PROTOCOL v4.2 ]
          </span>
        </div>

        <!-- Main Title -->
        <div>
          <h2 class="text-2xl sm:text-3xl lg:text-4xl font-extrabold font-editorial text-white tracking-tight">
            INHO <span class="text-transparent bg-clip-text bg-gradient-to-r from-neon-cyan via-sky-400 to-emerald-400">Business Engine</span>
          </h2>
          <p class="text-sm sm:text-base text-slate-300 mt-2 leading-relaxed">
            A plataforma definitiva de automação contábil para empresas: conciliação bancária <strong class="text-neon-cyan">PIX instantânea</strong>, emissão de <strong class="text-emerald-400">DRE em tempo real</strong> e auditoria tributária com isolamento criptográfico MultiFernet.
          </p>
        </div>

        <!-- Key Metrics Cards -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
          <div class="p-3 rounded-xl bg-slate-950/60 border border-cyan-500/20 flex flex-col">
            <span class="text-[10px] font-mono uppercase text-slate-400">Latência PIX</span>
            <span class="text-lg font-black font-mono text-neon-cyan mt-0.5">&lt; 1s</span>
            <span class="text-[9px] text-slate-500">Conciliação direta</span>
          </div>

          <div class="p-3 rounded-xl bg-slate-950/60 border border-emerald-500/20 flex flex-col">
            <span class="text-[10px] font-mono uppercase text-slate-400">Precisão DRE</span>
            <span class="text-lg font-black font-mono text-emerald-400 mt-0.5">99.8%</span>
            <span class="text-[9px] text-slate-500">Auditoria contábil</span>
          </div>

          <div class="p-3 rounded-xl bg-slate-950/60 border border-sky-500/20 flex flex-col">
            <span class="text-[10px] font-mono uppercase text-slate-400">Arquitetura</span>
            <span class="text-lg font-black font-mono text-sky-400 mt-0.5">Zero Lock-in</span>
            <span class="text-[9px] text-slate-500">Exportação aberta</span>
          </div>

          <div class="p-3 rounded-xl bg-slate-950/60 border border-purple-500/20 flex flex-col">
            <span class="text-[10px] font-mono uppercase text-slate-400">Segurança</span>
            <span class="text-lg font-black font-mono text-purple-400 mt-0.5">MultiFernet</span>
            <span class="text-[9px] text-slate-500">Isolamento total</span>
          </div>
        </div>

        <!-- Call to actions -->
        <div class="flex items-center gap-4 flex-wrap pt-2">
          <a
            href="https://inho.orbesystems.com.br"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-2 px-6 py-3 rounded-xl font-bold text-sm bg-gradient-to-r from-neon-cyan to-sky-500 text-black shadow-neon-cyan hover:brightness-110 transition-all hover:scale-[1.02] cursor-pointer"
          >
            <span>Acessar o INHO</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
          </a>

          <a
            href="https://orbesystems.com.br"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-2 px-5 py-3 rounded-xl font-mono text-xs font-semibold text-slate-300 hover:text-neon-cyan border border-slate-700 hover:border-cyan-500/50 bg-slate-900/40 transition-all"
          >
            <span>Hub Orbe Systems ↗</span>
          </a>
        </div>
      </div>

      <!-- Right side: Interactive 3D Void Canvas (PIX + DRE) -->
      <div class="lg:col-span-5 h-64 sm:h-72 lg:h-80 rounded-xl relative border border-cyan-500/20 bg-slate-950/80 overflow-hidden flex flex-col justify-end p-4 group">
        <!-- 3D WebGL Three.js Void -->
        <div class="absolute inset-0 z-0">
          <InhoVoidCanvas accent-color="#00fff5" secondary-color="#10b981" :particle-count="5000" />
        </div>

        <!-- Glass overlay badge -->
        <div class="relative z-10 p-3 rounded-lg bg-black/75 border border-cyan-500/30 backdrop-blur-md">
          <div class="flex items-center justify-between text-[10px] font-mono uppercase text-neon-cyan">
            <span>Void 3D // inho-pix-dre</span>
            <span class="text-emerald-400">Online 60 FPS</span>
          </div>
          <p class="text-[11px] text-slate-300 mt-1 font-mono">
            Nuvem de partículas reativa em Three.js simulando marcadores PIX e espectro contábil.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import InhoVoidCanvas from './InhoVoidCanvas.vue'
</script>
