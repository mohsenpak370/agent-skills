<template>
  <footer class="threadline-container border-t border-white/15 py-10 text-sm text-zinc-200">
    <div class="grid gap-8 md:grid-cols-[1.2fr_0.8fr] md:items-end">
      <div>
        <p class="threadline-wordmark text-xl font-black text-threadline-fog">Threadline</p>
        <p class="mt-3 max-w-2xl text-base leading-7">A cold-luxury wardrobe edit for customers who expect restraint, material quality, and service that disappears into the experience.</p>
      </div>

      <div class="grid gap-3 text-[11px] font-bold uppercase tracking-[0.22em] text-zinc-300 sm:grid-cols-3 md:text-right">
        <NuxtLink class="threadline-link" to="/products#catalog">New arrivals</NuxtLink>
        <NuxtLink class="threadline-link" to="/products#categories">Collections</NuxtLink>
        <NuxtLink class="threadline-link" to="#cart">Your bag</NuxtLink>
      </div>
    </div>

    <div class="mt-10 grid gap-3 border-t border-white/10 pt-5 text-xs uppercase tracking-[0.16em] text-zinc-300 sm:grid-cols-3">
      <p>Complimentary returns</p>
      <p class="sm:text-center">Private client support</p>
      <p class="sm:text-right">Threadline Atelier 2026</p>
    </div>
  </footer>
</template>
