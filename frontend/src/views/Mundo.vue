<template>
  <div>
    <div class="mb-10">
      <div class="flex items-center gap-3 mb-2">
        <span class="w-10 h-10 bg-sky-600 rounded-lg flex items-center justify-center text-white text-xl">🌍</span>
        <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight">Mundo</h1>
      </div>
      <p class="text-slate-500 text-lg">Os acontecimentos mais relevantes ao redor do globo.</p>
      <div class="h-px bg-gradient-to-r from-sky-500 via-sky-200 to-transparent mt-4"></div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <article v-for="(item, i) in articles" :key="i" class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm hover:shadow-lg transition-all group">
        <div class="h-44 overflow-hidden bg-gradient-to-br from-sky-100 to-blue-50 flex items-center justify-center">
          <span class="text-6xl">{{ item.emoji }}</span>
        </div>
        <div class="p-5">
          <span class="text-xs font-bold text-sky-600 uppercase tracking-wider">{{ item.tag }}</span>
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
  { tag: 'Europa', emoji: '🇪🇺', title: 'União Europeia aprova acordo climático histórico com metas para 2035', summary: 'O pacto obriga os 27 membros a reduzir emissões de carbono em 65% em relação aos níveis de 1990, com sanções financeiras para quem descumprir.', date: '27 Mar 2026 · 16:00' },
  { tag: 'Ásia', emoji: '🌏', title: 'Japão e Coreia do Sul assinam tratado de cooperação tecnológica inédito', summary: 'O acordo prevê investimentos conjuntos de US$ 30 bilhões em semicondutores e inteligência artificial nos próximos cinco anos.', date: '27 Mar 2026 · 07:00' },
  { tag: 'África', emoji: '🌍', title: 'Nigéria inaugura o maior parque solar do continente africano', summary: 'Com capacidade para abastecer 2 milhões de residências, a usina de 1,2 GW representa um marco na transição energética do maior país da África.', date: '26 Mar 2026 · 12:30' },
  { tag: 'Américas', emoji: '🌎', title: 'Acordo comercial entre Mercosul e Canadá é finalizado após 8 anos de negociação', summary: 'O tratado elimina tarifas sobre 92% dos produtos e abre caminho para o maior corredor comercial entre América do Sul e América do Norte.', date: '25 Mar 2026 · 19:00' },
]
</script>
