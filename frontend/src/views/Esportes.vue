<template>
  <div>
    <div class="mb-10">
      <div class="flex items-center gap-3 mb-2">
        <span class="w-10 h-10 bg-emerald-600 rounded-lg flex items-center justify-center text-white text-xl">⚽</span>
        <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight">Esportes</h1>
      </div>
      <p class="text-slate-500 text-lg">Futebol, olimpíadas e tudo que move a paixão esportiva do Brasil.</p>
      <div class="h-px bg-gradient-to-r from-emerald-500 via-emerald-200 to-transparent mt-4"></div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <article v-for="(item, i) in articles" :key="i" class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm hover:shadow-lg transition-all group">
        <div class="h-44 overflow-hidden">
          <img :src="item.image" :alt="item.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
        </div>
        <div class="p-5">
          <span class="text-xs font-bold text-emerald-600 uppercase tracking-wider">{{ item.tag }}</span>
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
  { tag: 'Futebol', title: 'Flamengo conquista a Libertadores com gol nos acréscimos', summary: 'Em final eletrizante disputada em Buenos Aires, o Rubro-Negro marcou aos 47 minutos do segundo tempo e levantou a taça continental pela quarta vez na história.', image: '/images/news_esportes.png', date: '27 Mar 2026 · 23:30' },
  { tag: 'Olimpíadas', title: 'Rebeca Andrade é eleita a melhor ginasta do mundo pelo terceiro ano consecutivo', summary: 'A Federação Internacional de Ginástica reconheceu a brasileira após temporada dominante, com ouros no solo, salto e individual geral.', image: '/images/news_esportes.png', date: '27 Mar 2026 · 11:00' },
  { tag: 'NBA', title: 'Brasileiro Victor Wembanyama quebra recorde de triplos-duplos na NBA', summary: 'O pivô de 2,24m registrou seu 25º triplo-duplo na temporada, superando a marca histórica de Wilt Chamberlain estabelecida em 1968.', image: '/images/news_esportes.png', date: '26 Mar 2026 · 08:00' },
  { tag: 'Fórmula 1', title: 'Grande Prêmio do Brasil retorna a Interlagos com recorde de público', summary: 'Mais de 120 mil espectadores lotaram o autódromo de São Paulo para assistir à penúltima etapa do campeonato mundial, com brasileiros competindo pela primeira vez em uma década.', image: '/images/news_esportes.png', date: '25 Mar 2026 · 16:00' },
]
</script>
