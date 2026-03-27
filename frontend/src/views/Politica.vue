<template>
  <div>
    <div class="mb-10">
      <div class="flex items-center gap-3 mb-2">
        <span class="w-10 h-10 bg-rose-600 rounded-lg flex items-center justify-center text-white text-xl">🏛️</span>
        <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight">Política</h1>
      </div>
      <p class="text-slate-500 text-lg">As últimas movimentações do cenário político nacional e internacional.</p>
      <div class="h-px bg-gradient-to-r from-rose-500 via-rose-200 to-transparent mt-4"></div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <article v-for="(item, i) in articles" :key="i" class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm hover:shadow-lg transition-all group">
        <div class="h-44 overflow-hidden">
          <img :src="item.image" :alt="item.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
        </div>
        <div class="p-5">
          <span class="text-xs font-bold text-rose-600 uppercase tracking-wider">{{ item.tag }}</span>
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
  { tag: 'Congresso', title: 'Senado aprova reforma tributária em segundo turno com placar apertado', summary: 'A votação histórica ocorreu após madrugada de negociações entre líderes partidários. O texto agora segue para promulgação e deverá entrar em vigor de forma gradual nos próximos anos.', image: '/images/news_politica.png', date: '27 Mar 2026 · 14:30' },
  { tag: 'Eleições', title: 'Pesquisa aponta empate técnico entre os dois principais candidatos para 2026', summary: 'Levantamento do instituto aponta cenário acirrado para o primeiro turno, com margem de erro de dois pontos percentuais. Indecisos representam 18% do eleitorado.', image: '/images/news_politica.png', date: '27 Mar 2026 · 10:15' },
  { tag: 'Diplomacia', title: 'Brasil assume presidência rotativa do Conselho de Segurança da ONU', summary: 'País promete pautar a reforma do órgão e ampliar o debate sobre segurança alimentar global durante o mandato de 30 dias. Chanceler discursa na abertura.', image: '/images/news_politica.png', date: '26 Mar 2026 · 18:00' },
  { tag: 'Legislação', title: 'Câmara derruba veto presidencial sobre lei de proteção de dados pessoais', summary: 'Com 342 votos favoráveis, deputados reverteram o veto do Executivo ao trecho que obrigava empresas de tecnologia a manter data centers em território nacional.', image: '/images/news_politica.png', date: '26 Mar 2026 · 09:45' },
]
</script>
