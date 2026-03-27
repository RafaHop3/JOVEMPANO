<template>
  <div>
    <div class="mb-10">
      <div class="flex items-center gap-3 mb-2">
        <span class="w-10 h-10 bg-amber-500 rounded-lg flex items-center justify-center text-white text-xl">📈</span>
        <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight">Economia</h1>
      </div>
      <p class="text-slate-500 text-lg">Mercados, finanças e os números que movem o Brasil e o mundo.</p>
      <div class="h-px bg-gradient-to-r from-amber-500 via-amber-200 to-transparent mt-4"></div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <article v-for="(item, i) in articles" :key="i" class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm hover:shadow-lg transition-all group">
        <div class="h-44 overflow-hidden">
          <img :src="item.image" :alt="item.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
        </div>
        <div class="p-5">
          <span class="text-xs font-bold text-amber-600 uppercase tracking-wider">{{ item.tag }}</span>
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
  { tag: 'Mercado', title: 'Ibovespa supera 150 mil pontos pela primeira vez na história', summary: 'O índice da bolsa brasileira atingiu o marco impulsionado pela entrada de capital estrangeiro e pela perspectiva de corte na taxa Selic nas próximas reuniões do Copom.', image: '/images/news_economia.png', date: '27 Mar 2026 · 17:00' },
  { tag: 'Câmbio', title: 'Dólar recua para R$ 4,85 com fluxo positivo de investimentos', summary: 'A moeda norte-americana acumula queda de 8% no trimestre, refletindo o aumento da confiança de investidores internacionais na economia brasileira.', image: '/images/news_economia.png', date: '27 Mar 2026 · 12:30' },
  { tag: 'Inflação', title: 'IPCA desacelera para 3,2% em 12 meses e aproxima meta do BC', summary: 'A inflação acumulada em 12 meses é a menor desde 2020, puxada pela queda nos preços de alimentos e combustíveis no período.', image: '/images/news_economia.png', date: '26 Mar 2026 · 09:00' },
  { tag: 'Emprego', title: 'Taxa de desemprego cai para 6,8% e atinge menor nível em 10 anos', summary: 'O setor de serviços e a construção civil lideraram a geração de postos de trabalho formais no último trimestre, segundo dados do IBGE.', image: '/images/news_economia.png', date: '25 Mar 2026 · 15:45' },
]
</script>
