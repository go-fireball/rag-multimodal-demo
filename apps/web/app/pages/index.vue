<template>
  <main class="p-6 max-w-3xl mx-auto space-y-4">
    <h1 class="text-2xl font-bold">Multimodal RAG PoC</h1>
    <form @submit.prevent="run">
      <input v-model="q" class="border p-2 w-full" placeholder="Ask a question"/>
      <label class="block mt-2"><input type="checkbox" v-model="wantFigures"/> Include figures</label>
      <button class="mt-2 px-4 py-2 bg-black text-white">Search</button>
    </form>
    <section v-if="answer" class="prose whitespace-pre-wrap">{{ answer }}</section>
    <section v-if="hits && hits.length">
      <h2 class="font-semibold mt-6">Text hits</h2>
      <ul>
        <li v-for="h in hits" :key="h.chunk_id" class="border p-2 my-2">
          <div class="text-xs opacity-70">doc: {{ h.doc_id }} p: {{ h.page }} score: {{ h.score?.toFixed?.(3) }}</div>
          <div class="mt-1">{{ h.text?.slice(0, 280) }}…</div>
        </li>
      </ul>
      <h2 class="font-semibold mt-6" v-if="figs && figs.length">Figure hits</h2>
      <ul>
        <li v-for="f in figs" :key="f.figure_id" class="border p-2 my-2">
          <div class="text-xs opacity-70">doc: {{ f.doc_id }} p: {{ f.page }} score: {{ f.score?.toFixed?.(3) }}</div>
          <div class="mt-1">{{ f.caption_dense }}</div>
          <img v-if="f.thumb_uri" :src="f.thumb_uri" class="mt-2 max-h-48" alt=""/>
        </li>
      </ul>
    </section>
  </main>
</template>


<script setup lang="ts">
const q = ref("")
const wantFigures = ref(true)
const answer = ref("")
const hits = ref<any[]>([])
const figs = ref<any[]>([])


async function run() {
  const res = await $fetch("http://localhost:8000/query", {
    method: "POST",
    body: {query: q.value, want_figures: wantFigures.value}
  })
  answer.value = (res as any).answer
  hits.value = (res as any).text_hits
  figs.value = (res as any).figure_hits
}
</script>


<style>
.prose {
  white-space: pre-wrap;
}
</style>