<script setup lang="ts">
import type { CartResponse } from '~/types/cart'

const props = defineProps<{
  cart: CartResponse
  isBusy: boolean
  errorMessage: string
}>()

const emit = defineEmits<{
  updateQuantity: [itemId: number, quantity: number]
  removeItem: [itemId: number]
  clearCart: []
}>()

const hasItems = computed(() => props.cart.items.length > 0)

function decreaseQuantity(itemId: number, quantity: number) {
  if (quantity <= 1) {
    emit('removeItem', itemId)
    return
  }
  emit('updateQuantity', itemId, quantity - 1)
}
</script>

<template>
  <aside aria-labelledby="cart-title">
    <div class="threadline-dark-panel sticky top-24 space-y-5 p-5">
      <div class="flex items-start justify-between gap-4">
        <div>
          <p class="threadline-label">Private order</p>
          <h2 id="cart-title" class="mt-1 text-3xl font-black tracking-[-0.05em] text-threadline-fog">Bag</h2>
          <p class="mt-2 text-sm leading-6 text-zinc-300">Your selected pieces stay saved on this device.</p>
        </div>
        <span class="inline-flex min-w-10 justify-center border border-white/15 bg-white/10 px-3 py-2 text-sm font-black text-threadline-fog" aria-label="Items in cart">{{ cart.summary.itemCount }}</span>
      </div>

      <UAlert v-if="errorMessage" color="error" variant="soft" icon="i-lucide-alert-circle" :description="errorMessage" role="alert" />

      <div v-if="!hasItems" class="border border-dashed border-white/20 bg-white/[0.04] p-5">
        <p class="font-black text-threadline-fog">Your edit is empty.</p>
        <p class="mt-2 text-sm leading-6 text-zinc-200">Add pieces to build a private selection before checkout.</p>
        <NuxtLink to="/products#catalog" class="threadline-button-secondary mt-5 h-10 px-4">Browse catalog</NuxtLink>
      </div>

      <ul v-else class="space-y-4" aria-label="Cart items">
        <li v-for="item in cart.items" :key="item.id" class="flex gap-3 border border-white/10 bg-white/[0.04] p-3 transition hover:border-white/20 hover:bg-white/[0.065]">
          <img
            v-if="item.product.imageUrl"
            class="size-16 object-cover"
            :src="item.product.imageUrl"
            :alt="item.product.name"
            loading="lazy"
          >
          <div class="min-w-0 flex-1">
            <div class="flex items-start justify-between gap-3">
              <h3 class="line-clamp-2 text-sm font-bold text-threadline-fog">{{ item.product.name }}</h3>
              <p class="shrink-0 text-sm font-black text-threadline-fog">${{ item.lineTotal }}</p>
            </div>
            <p class="mt-1 text-xs text-zinc-300">${{ item.product.price }} each</p>
            <div class="mt-3 flex flex-wrap items-center gap-2">
              <UButtonGroup size="xs" :aria-label="`Quantity for ${item.product.name}`">
              <UButton
                color="neutral"
                variant="outline"
                icon="i-lucide-minus"
                class="cursor-pointer disabled:cursor-not-allowed"
                :disabled="isBusy"
                :aria-label="`Decrease ${item.product.name}`"
                @click="decreaseQuantity(item.id, item.quantity)"
                />
                <UBadge color="neutral" variant="outline" class="min-w-9 justify-center rounded-none">{{ item.quantity }}</UBadge>
                <UButton
                color="neutral"
                variant="outline"
                icon="i-lucide-plus"
                class="cursor-pointer disabled:cursor-not-allowed"
                :disabled="isBusy || item.quantity >= 99"
                :aria-label="`Increase ${item.product.name}`"
                @click="$emit('updateQuantity', item.id, item.quantity + 1)"
              />
            </UButtonGroup>
              <UButton color="neutral" variant="ghost" size="xs" class="cursor-pointer disabled:cursor-not-allowed" :disabled="isBusy" :aria-label="`Remove ${item.product.name} from bag`" @click="$emit('removeItem', item.id)">
                Remove
              </UButton>
            </div>
          </div>
        </li>
      </ul>

      <div class="h-px bg-white/10" />

      <div class="flex items-center justify-between text-sm" aria-live="polite">
        <span class="text-zinc-200">Subtotal</span>
        <strong class="text-2xl tracking-[-0.04em] text-threadline-fog">${{ cart.summary.subtotal }}</strong>
      </div>

      <UButton block color="neutral" size="lg" class="cursor-pointer bg-threadline-fog text-zinc-950 hover:bg-white disabled:cursor-not-allowed disabled:bg-white/20 disabled:text-white/45" :disabled="!hasItems || isBusy" :loading="isBusy">
        Continue to checkout
      </UButton>
      <UButton v-if="hasItems" block color="neutral" variant="ghost" class="cursor-pointer disabled:cursor-not-allowed" :disabled="isBusy" @click="$emit('clearCart')">
        Clear cart
      </UButton>
      <p class="text-xs leading-5 text-zinc-300">Taxes and delivery are calculated at checkout. Returns are complimentary for 30 days.</p>
    </div>
  </aside>
</template>
