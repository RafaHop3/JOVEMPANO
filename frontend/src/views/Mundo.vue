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

    <!-- Notícia especial: Tabela Comparativa -->
    <article class="bg-white border border-sky-200 rounded-2xl overflow-hidden shadow-md mb-8">
      <div class="bg-gradient-to-r from-sky-700 to-blue-900 px-6 py-5">
        <span class="inline-block text-xs font-bold text-sky-200 uppercase tracking-widest mb-2 border border-sky-400/40 rounded px-2 py-0.5">Análise Internacional</span>
        <h2 class="text-2xl font-extrabold text-white leading-tight">Comparação – Irã x Monarquias do Golfo (com questão LGBT)</h2>
        <p class="text-sky-200 text-sm mt-1">04 Abr 2026 · Redação JovemPano</p>
      </div>
      <div class="p-6">
        <p class="text-slate-600 text-sm leading-relaxed mb-6">
          Uma análise comparativa entre o Irã e as principais monarquias do Golfo Pérsico revela diferenças e semelhanças surpreendentes em seis dimensões políticas e sociais: eleições, parlamento, presença feminina na mídia, mulheres no volante, representação judaica e direitos LGBT.
        </p>
        <!-- Tabela responsiva -->
        <div class="overflow-x-auto rounded-xl border border-slate-200">
          <table class="w-full text-sm border-collapse">
            <thead>
              <tr class="bg-slate-900 text-white">
                <th class="px-3 py-3 text-left font-bold border-r border-slate-700 min-w-[90px]">País</th>
                <th class="px-3 py-3 text-center font-bold border-r border-slate-700 min-w-[120px]">Eleição p/ Chefe de Estado</th>
                <th class="px-3 py-3 text-center font-bold border-r border-slate-700 min-w-[120px]">Parlamento Eleito (c/ mulheres)</th>
                <th class="px-3 py-3 text-center font-bold border-r border-slate-700 min-w-[120px]">Mulheres na TV/Mídia</th>
                <th class="px-3 py-3 text-center font-bold border-r border-slate-700 min-w-[100px]">Mulheres Dirigem</th>
                <th class="px-3 py-3 text-center font-bold border-r border-slate-700 min-w-[100px]">Judeus no Parlamento</th>
                <th class="px-3 py-3 text-center font-bold min-w-[130px]">Homossexualidade (legalidade)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, i) in comparisonData" :key="i" :class="i % 2 === 0 ? 'bg-white' : 'bg-slate-50'" class="border-t border-slate-200 hover:bg-sky-50 transition-colors">
                <td class="px-3 py-3 font-bold text-slate-900 border-r border-slate-200">{{ row.country }}</td>
                <td class="px-3 py-3 border-r border-slate-200">
                  <span :class="row.election.ok ? 'text-emerald-700' : 'text-rose-600'" class="flex items-start gap-1 text-xs">
                    <span>{{ row.election.ok ? '✅' : '❌' }}</span>
                    <span>{{ row.election.text }}</span>
                  </span>
                </td>
                <td class="px-3 py-3 border-r border-slate-200">
                  <span :class="row.parliament.ok ? 'text-emerald-700' : 'text-rose-600'" class="flex items-start gap-1 text-xs">
                    <span>{{ row.parliament.ok ? '✅' : '❌' }}</span>
                    <span>{{ row.parliament.text }}</span>
                  </span>
                </td>
                <td class="px-3 py-3 border-r border-slate-200">
                  <span class="text-emerald-700 flex items-start gap-1 text-xs">
                    <span>✅</span>
                    <span>{{ row.womenmedia }}</span>
                  </span>
                </td>
                <td class="px-3 py-3 border-r border-slate-200">
                  <span :class="row.womendrive.ok ? 'text-emerald-700' : 'text-rose-600'" class="flex items-start gap-1 text-xs">
                    <span>{{ row.womendrive.ok ? '✅' : '❌' }}</span>
                    <span>{{ row.womendrive.text }}</span>
                  </span>
                </td>
                <td class="px-3 py-3 border-r border-slate-200">
                  <span :class="row.jewish.ok ? 'text-emerald-700' : 'text-rose-600'" class="flex items-start gap-1 text-xs">
                    <span>{{ row.jewish.ok ? '✅' : '❌' }}</span>
                    <span>{{ row.jewish.text }}</span>
                  </span>
                </td>
                <td class="px-3 py-3">
                  <span class="text-rose-700 flex items-start gap-1 text-xs">
                    <span>❌</span>
                    <span>{{ row.lgbt }}</span>
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="text-xs text-slate-400 mt-4 italic">Fonte: Redação JovemPano com base em dados públicos internacionais · 04 Abr 2026</p>
      </div>
    </article>

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
const comparisonData = [
  {
    country: 'Irã',
    election: { ok: true, text: 'Eleição presidencial direta, mas poder limitado frente ao Líder Supremo.' },
    parliament: { ok: true, text: 'Mulheres têm assentos, mas em número reduzido.' },
    womenmedia: 'Presentes em telejornais e programas, com regras rígidas.',
    womendrive: { ok: true, text: 'Sempre puderam dirigir.' },
    jewish: { ok: true, text: '1 assento reservado para judeus.' },
    lgbt: 'Criminalizada; pode levar à prisão ou pena de morte.'
  },
  {
    country: 'Arábia Saudita',
    election: { ok: false, text: 'Rei governa por sucessão.' },
    parliament: { ok: false, text: 'Não há parlamento eleito; apenas conselho consultivo nomeado.' },
    womenmedia: 'Mulheres na TV desde os anos 2010, mas com restrições religiosas.',
    womendrive: { ok: true, text: 'Desde 2018.' },
    jewish: { ok: false, text: 'Não há representação judaica.' },
    lgbt: 'Criminalizada; punições severas, incluindo pena de morte.'
  },
  {
    country: 'Bahrein',
    election: { ok: false, text: 'Rei governa por sucessão.' },
    parliament: { ok: true, text: 'Parlamento eleito desde 2002, com mulheres.' },
    womenmedia: 'Mulheres apresentam programas e telejornais.',
    womendrive: { ok: true, text: 'Sim, há décadas.' },
    jewish: { ok: false, text: 'Não há representação judaica.' },
    lgbt: 'Criminalizada; punições legais, mas aplicação menos rígida.'
  },
  {
    country: 'Kuwait',
    election: { ok: false, text: 'Emir governa por sucessão.' },
    parliament: { ok: true, text: 'Parlamento eleito, mulheres desde 2009.' },
    womenmedia: 'Mulheres em programas de entretenimento e notícias.',
    womendrive: { ok: true, text: 'Sim, desde os anos 1960.' },
    jewish: { ok: false, text: 'Não há representação judaica.' },
    lgbt: 'Criminalizada; prisão e multas.'
  },
  {
    country: 'Omã',
    election: { ok: false, text: 'Sultão governa por sucessão.' },
    parliament: { ok: true, text: 'Conselho Consultivo com algumas mulheres, poder limitado.' },
    womenmedia: 'Mulheres na mídia, em menor número.',
    womendrive: { ok: true, text: 'Sim.' },
    jewish: { ok: false, text: 'Não há representação judaica.' },
    lgbt: 'Criminalizada; prisão prevista em lei.'
  },
  {
    country: 'Qatar',
    election: { ok: false, text: 'Emir governa por sucessão.' },
    parliament: { ok: false, text: 'Parlamento com participação mínima de mulheres.' },
    womenmedia: 'Mulheres na TV, mas sob regras conservadoras.',
    womendrive: { ok: true, text: 'Sim.' },
    jewish: { ok: false, text: 'Não há representação judaica.' },
    lgbt: 'Criminalizada; prisão e multas.'
  },
  {
    country: 'EAU',
    election: { ok: false, text: 'Presidente escolhido entre emires.' },
    parliament: { ok: true, text: 'Parlamento com 50% de assentos reservados para mulheres.' },
    womenmedia: 'Forte presença feminina em telejornais e programas culturais.',
    womendrive: { ok: true, text: 'Sim, inclusive em corridas automobilísticas.' },
    jewish: { ok: false, text: 'Não há representação judaica.' },
    lgbt: 'Criminalizada; leis severas, mas em áreas cosmopolitas (Dubai, Abu Dhabi) há maior tolerância social.'
  }
]

const articles = [
  { tag: 'Europa', emoji: '🇪🇺', title: 'União Europeia aprova acordo climático histórico com metas para 2035', summary: 'O pacto obriga os 27 membros a reduzir emissões de carbono em 65% em relação aos níveis de 1990, com sanções financeiras para quem descumprir.', date: '27 Mar 2026 · 16:00' },
  { tag: 'Ásia', emoji: '🌏', title: 'Japão e Coreia do Sul assinam tratado de cooperação tecnológica inédito', summary: 'O acordo prevê investimentos conjuntos de US$ 30 bilhões em semicondutores e inteligência artificial nos próximos cinco anos.', date: '27 Mar 2026 · 07:00' },
  { tag: 'África', emoji: '🌍', title: 'Nigéria inaugura o maior parque solar do continente africano', summary: 'Com capacidade para abastecer 2 milhões de residências, a usina de 1,2 GW representa um marco na transição energética do maior país da África.', date: '26 Mar 2026 · 12:30' },
  { tag: 'Américas', emoji: '🌎', title: 'Acordo comercial entre Mercosul e Canadá é finalizado após 8 anos de negociação', summary: 'O tratado elimina tarifas sobre 92% dos produtos e abre caminho para o maior corredor comercial entre América do Sul e América do Norte.', date: '25 Mar 2026 · 19:00' },
]
</script>
