<script setup lang="ts">
import type { Product } from '~/types/product'

defineProps<{
  products: Product[]
  cartQuantities: Record<number, number>
  isBusy: boolean
}>()

defineEmits<{
  addToCart: [productId: number]
}>()
</script>

<template>
  <section class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3" aria-label="Products">
    <article v-for="product in products" :key="product.id" class="threadline-card threadline-fade-up threadline-hover-lift group flex min-h-full flex-col">
      <NuxtLink :to="`/products/${product.id}`" class="relative block aspect-[4/5] overflow-hidden bg-zinc-900" :aria-label="`View details for ${product.name}`">
        <img
          v-if="product.imageUrl"
          class="size-full object-cover transition duration-700 group-hover:scale-105"
          :src="product.imageUrl"
          :alt="product.name"
          loading="lazy"
        >
        <div v-else class="flex size-full items-center justify-center bg-[radial-gradient(circle_at_50%_20%,rgba(159,214,255,0.18),transparent_18rem)] text-sm font-bold uppercase tracking-[0.18em] text-zinc-300">
          Image coming soon
        </div>
        <div class="threadline-chip absolute left-3 top-3 bg-zinc-950/70 backdrop-blur-md">{{ product.category }}</div>
        <div v-if="cartQuantities[product.id]" class="absolute bottom-3 right-3 border border-threadline-blue bg-zinc-950/78 px-3 py-2 text-[11px] font-black uppercase tracking-[0.16em] text-threadline-blue backdrop-blur-md">
          {{ cartQuantities[product.id] }} in bag
        </div>
      </NuxtLink>

      <div class="flex flex-1 flex-col p-5">
        <div class="flex items-center justify-between gap-3 text-[11px] font-bold uppercase tracking-[0.2em] text-zinc-300">
          <span>Ready to ship</span>
          <span class="text-threadline-blue">Atelier</span>
        </div>
        <h2 class="mt-4 text-2xl font-black leading-tight tracking-[-0.05em] text-threadline-fog">
          <NuxtLink class="threadline-link" :to="`/products/${product.id}`">{{ product.name }}</NuxtLink>
        </h2>
        <p class="mt-3 line-clamp-3 text-sm leading-6 text-zinc-200">{{ product.description }}</p>

        <div class="mt-auto space-y-4 pt-6">
          <div class="flex items-end justify-between gap-3">
            <p class="text-2xl font-black tracking-[-0.04em] text-threadline-fog">${{ product.price }}</p>
            <NuxtLink :to="`/products/${product.id}`" class="threadline-link text-xs font-bold uppercase tracking-[0.16em] text-zinc-200">Details</NuxtLink>
          </div>
          <UButton
            block
            color="neutral"
            variant="solid"
            size="lg"
            class="cursor-pointer bg-threadline-fog text-zinc-950 hover:bg-white disabled:cursor-not-allowed disabled:bg-white/20 disabled:text-white/45"
            :loading="isBusy"
            :disabled="isBusy"
            :aria-label="`Add ${product.name} to bag`"
            @click="$emit('addToCart', product.id)"
          >
            {{ cartQuantities[product.id] ? `Add more (${cartQuantities[product.id]})` : 'Add to bag' }}
          </UButton>
        </div>
      </div>
    </article>
  </section>
</template>
