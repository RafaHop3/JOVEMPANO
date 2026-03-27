<template>
  <div>
    <div class="mb-10">
      <div class="flex items-center gap-3 mb-2">
        <span class="w-10 h-10 bg-violet-600 rounded-lg flex items-center justify-center text-white text-xl">💻</span>
        <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight">Tecnologia</h1>
      </div>
      <p class="text-slate-500 text-lg">Inovação, inteligência artificial e as tendências que transformam o futuro.</p>
      <div class="h-px bg-gradient-to-r from-violet-500 via-violet-200 to-transparent mt-4"></div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <article v-for="(item, i) in articles" :key="i" class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm hover:shadow-lg transition-all group">
        <div class="h-44 overflow-hidden bg-gradient-to-br from-violet-100 to-slate-100 flex items-center justify-center">
          <span class="text-6xl">{{ item.emoji }}</span>
        </div>
        <div class="p-5">
          <span class="text-xs font-bold text-violet-600 uppercase tracking-wider">{{ item.tag }}</span>
          <h3 class="text-lg font-bold text-slate-900 mt-1 mb-2 leading-snug">{{ item.title }}</h3>
          <p class="text-slate-500 text-sm leading-relaxed line-clamp-3">{{ item.summary }}</p>
          <p class="text-xs text-slate-400 mt-3 font-mono">{{ item.date }}</p>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
const articles = [
  { tag: 'IA', emoji: '🤖', title: 'Google anuncia modelo de IA que supera médicos em diagnósticos', summary: 'O sistema Gemini Med alcançou 97% de acurácia em testes clínicos controlados, superando a média de especialistas humanos em radiologia e dermatologia.', date: '27 Mar 2026 · 15:00' },
  { tag: 'Startups', emoji: '🚀', title: 'Startup brasileira de energia limpa capta US$ 500 milhões em rodada Series C', summary: 'A empresa carioca Nova Watts, que desenvolve baterias de estado sólido, atraiu investimento de fundos globais e se tornou o mais novo unicórnio do país.', date: '27 Mar 2026 · 09:30' },
  { tag: 'Cibersegurança', emoji: '🔒', title: 'Brasil aprova marco regulatório de cibersegurança inspirado no modelo europeu', summary: 'A nova legislação obriga empresas que operam no país a manterem centros de resposta a incidentes e notificar vazamentos em até 72 horas.', date: '26 Mar 2026 · 14:00' },
  { tag: '5G', emoji: '📡', title: 'Cobertura 5G atinge 90% das capitais brasileiras antes do prazo previsto', summary: 'O avanço da infraestrutura superou as expectativas da Anatel. O próximo desafio é levar a tecnologia de quinta geração para o interior do país até 2028.', date: '25 Mar 2026 · 11:15' },
]
</script>
