<script setup lang="ts">
defineProps<{
  itemCount: number
}>()
</script>

<template>
  <header class="threadline-header">
    <NuxtLink class="threadline-hover-lift inline-flex items-center gap-3 text-threadline-fog" to="/products" aria-label="Threadline Atelier home">
      <span class="threadline-metal inline-flex size-10 items-center justify-center border border-white/20 text-xs font-black tracking-[-0.04em] text-zinc-950">TL</span>
      <span class="leading-none">
        <span class="threadline-wordmark block text-sm font-black">Threadline</span>
        <span class="block text-[10px] uppercase tracking-[0.28em] text-threadline-blue">Atelier</span>
      </span>
    </NuxtLink>

    <nav class="hidden items-center gap-7 text-[11px] font-bold uppercase tracking-[0.22em] text-zinc-200 sm:flex" aria-label="Main navigation">
      <NuxtLink class="threadline-link" to="/products#categories">Edits</NuxtLink>
      <NuxtLink class="threadline-link" to="/products#catalog">Catalog</NuxtLink>
      <NuxtLink class="threadline-link" to="#cart">Bag</NuxtLink>
    </nav>

    <NuxtLink
      to="#cart"
      class="threadline-button-primary threadline-hover-lift h-11 gap-3 px-4 shadow-[0_12px_40px_rgba(159,214,255,0.12)]"
      :aria-label="`Bag with ${itemCount} items`"
    >
      <span class="hidden sm:inline">Bag</span>
      <span class="inline-flex min-w-6 justify-center border border-zinc-950/15 bg-zinc-950 px-1.5 py-0.5 text-[11px] text-threadline-fog">{{ itemCount }}</span>
    </NuxtLink>
  </header>
</template>
