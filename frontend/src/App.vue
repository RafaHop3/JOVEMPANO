<template>
  <div class="min-h-screen">
    <header class="border-b border-slate-800 bg-slate-900/50 backdrop-blur sticky top-0 z-50">
      <div class="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
        <router-link to="/" class="hover:opacity-80 transition-opacity">
          <h1 class="text-2xl font-extrabold text-white tracking-tight">Jovem<span class="text-rose-600">Pano</span></h1>
        </router-link>
        <nav class="flex gap-4">
          <router-link to="/" class="text-sm font-semibold text-slate-400 hover:text-white transition-colors">Notícias</router-link>
          <router-link to="/admin" class="text-sm font-semibold text-slate-400 hover:text-rose-500 transition-colors">Painel Admin</router-link>
        </nav>
      </div>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-8">
      <router-view></router-view>
    </main>
  </div>
</template>
