<script setup lang="ts">
import type { Product } from '~/types/product'

defineProps<{
  product: Product
  cartQuantity: number
  isBusy: boolean
}>()

defineEmits<{
  addToCart: [productId: number]
}>()
</script>

<template>
  <article class="grid gap-5 lg:grid-cols-[minmax(0,0.98fr)_minmax(340px,0.82fr)]" aria-labelledby="product-title">
    <div class="threadline-fade-up relative overflow-hidden border border-white/15 bg-zinc-950 shadow-[0_24px_80px_rgba(0,0,0,0.32)]">
      <img v-if="product.imageUrl" class="aspect-[4/5] size-full object-cover transition duration-700 hover:scale-105" :src="product.imageUrl" :alt="product.name">
      <div v-else class="flex aspect-[4/5] size-full items-center justify-center bg-[radial-gradient(circle_at_50%_20%,rgba(159,214,255,0.18),transparent_18rem)] text-sm font-bold uppercase tracking-[0.18em] text-zinc-300">
        Image coming soon
      </div>
      <div class="absolute left-4 top-4 threadline-chip bg-zinc-950/70 backdrop-blur-md">{{ product.category }} edit</div>
    </div>

    <section class="threadline-fade-up threadline-delay-1 threadline-panel space-y-7 p-5 sm:p-7" aria-label="Product information">
      <UButton to="/products#catalog" color="neutral" variant="ghost" icon="i-lucide-arrow-left" class="w-fit cursor-pointer">
        Back to catalog
      </UButton>
      <div>
        <p class="threadline-label">{{ product.category }} edit</p>
        <h1 id="product-title" class="threadline-heading-lg mt-4">{{ product.name }}</h1>
        <div class="mt-5 flex flex-wrap items-end gap-3">
          <p class="text-4xl font-black tracking-[-0.05em] text-threadline-fog">${{ product.price }}</p>
          <span v-if="cartQuantity" class="threadline-chip border-threadline-blue text-threadline-blue">{{ cartQuantity }} in bag</span>
        </div>
        <p class="mt-5 text-base leading-7 text-zinc-200">{{ product.description }}</p>
      </div>

      <div class="threadline-card-muted p-4 sm:p-5">
        <div class="flex flex-col gap-3">
          <UButton block color="neutral" size="xl" class="cursor-pointer bg-threadline-fog text-zinc-950 hover:bg-white disabled:cursor-not-allowed disabled:bg-white/20 disabled:text-white/45" :loading="isBusy" :disabled="isBusy" :aria-label="`Add ${product.name} to bag`" @click="$emit('addToCart', product.id)">
            {{ cartQuantity ? `Add more (${cartQuantity} in bag)` : 'Add to bag' }}
          </UButton>
          <div class="flex flex-wrap items-center justify-between gap-3 text-sm font-semibold text-zinc-200">
            <span>In stock and ready to ship</span>
            <NuxtLink to="#cart" class="threadline-link text-xs uppercase tracking-[0.16em]">Review bag</NuxtLink>
          </div>
        </div>
        <p class="mt-4 text-xs uppercase tracking-[0.16em] text-zinc-300">Complimentary returns and private support included.</p>
      </div>

      <dl class="grid gap-3 sm:grid-cols-3">
        <div class="threadline-card-muted p-4">
          <dt class="text-xs font-bold uppercase tracking-[0.18em] text-threadline-blue">Fit</dt>
          <dd class="mt-3 font-semibold text-threadline-fog">Relaxed atelier fit</dd>
        </div>
        <div class="threadline-card-muted p-4">
          <dt class="text-xs font-bold uppercase tracking-[0.18em] text-threadline-blue">Care</dt>
          <dd class="mt-3 font-semibold text-threadline-fog">Machine wash cold</dd>
        </div>
        <div class="threadline-card-muted p-4">
          <dt class="text-xs font-bold uppercase tracking-[0.18em] text-threadline-blue">Delivery</dt>
          <dd class="mt-3 font-semibold text-threadline-fog">30-day free returns</dd>
        </div>
      </dl>
    </section>
  </article>
</template>
