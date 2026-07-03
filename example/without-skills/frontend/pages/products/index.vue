<script setup lang="ts">
type Product = {
  id: number
  name: string
  description: string
  category: string
  brand: string
  size: string
  color: string
  price: string
  image_url: string
  featured: boolean
}

type Category = {
  value: string
  label: string
  count: number
}

type CartItem = {
  product: Product
  quantity: number
  line_total: string
}

type Cart = {
  cart_id: string
  items: CartItem[]
  total_items: number
  total_price: string
}

type CartRequestOptions = {
  method?: 'GET' | 'POST' | 'DELETE'
  body?: unknown
  headers?: Record<string, string>
}

const route = useRoute()
const config = useRuntimeConfig()
const selectedCategory = ref(typeof route.query.category === 'string' ? route.query.category : '')
const search = ref(typeof route.query.search === 'string' ? route.query.search : '')
const sort = ref(typeof route.query.sort === 'string' ? route.query.sort : 'name')
const minPrice = ref('')
const maxPrice = ref('')
const cart = ref<Cart | null>(null)
const cartError = ref('')
const activeProductId = ref<number | null>(null)
const isClearing = ref(false)

const sortOptions = [
  { label: 'Name', value: 'name' },
  { label: 'Newest', value: 'newest' },
  { label: 'Price: low to high', value: 'price_asc' },
  { label: 'Price: high to low', value: 'price_desc' }
]

const productQuery = computed(() => ({
  category: selectedCategory.value || undefined,
  search: search.value || undefined,
  sort: sort.value,
  min_price: minPrice.value || undefined,
  max_price: maxPrice.value || undefined
}))

const { data, pending, error, refresh } = await useFetch<{ products: Product[] }>(
  `${config.public.apiBase}/products/`,
  {
    query: productQuery,
    watch: [productQuery],
    default: () => ({ products: [] })
  }
)

const { data: categoryData } = await useFetch<{ categories: Category[] }>(
  `${config.public.apiBase}/categories/`,
  { default: () => ({ categories: [] }) }
)

const products = computed(() => data.value?.products ?? [])
const categories = computed(() => categoryData.value?.categories ?? [])
const cartItems = computed(() => cart.value?.items ?? [])
const cartTotal = computed(() => cart.value?.total_price ?? '0.00')
const cartCount = computed(() => cart.value?.total_items ?? 0)

const activeCategoryLabel = computed(() => {
  return categories.value.find((category) => category.value === selectedCategory.value)?.label ?? 'All Clothing'
})

const quantitiesByProduct = computed(() => {
  return cartItems.value.reduce<Record<number, number>>((quantities, item) => {
    quantities[item.product.id] = item.quantity
    return quantities
  }, {})
})

watch(
  () => route.query,
  (query) => {
    selectedCategory.value = typeof query.category === 'string' ? query.category : ''
    search.value = typeof query.search === 'string' ? query.search : ''
    sort.value = typeof query.sort === 'string' ? query.sort : 'name'
  }
)

function getCartId() {
  return import.meta.client ? localStorage.getItem('cart_id') : null
}

function saveCartId(cartId: string) {
  if (import.meta.client) {
    localStorage.setItem('cart_id', cartId)
  }
}

function clearFilters() {
  selectedCategory.value = ''
  search.value = ''
  sort.value = 'name'
  minPrice.value = ''
  maxPrice.value = ''
}

async function cartRequest(path: string, options: CartRequestOptions = {}) {
  cartError.value = ''
  const cartId = getCartId()
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers
  }

  if (cartId) {
    headers['X-Cart-Id'] = cartId
  }

  const response = await $fetch<Cart>(`${config.public.apiBase}${path}`, {
    ...options,
    headers
  })

  cart.value = response
  saveCartId(response.cart_id)
  return response
}

async function loadCart() {
  try {
    await cartRequest('/cart/')
  } catch {
    cartError.value = 'Could not load your cart.'
  }
}

async function addToCart(productId: number) {
  activeProductId.value = productId
  try {
    await cartRequest('/cart/items/', {
      method: 'POST',
      body: { product_id: productId, quantity: 1 }
    })
  } catch {
    cartError.value = 'Could not add this product.'
  } finally {
    activeProductId.value = null
  }
}

async function increaseItem(productId: number) {
  activeProductId.value = productId
  try {
    await cartRequest(`/cart/items/${productId}/increase/`, { method: 'POST' })
  } catch {
    cartError.value = 'Could not increase quantity.'
  } finally {
    activeProductId.value = null
  }
}

async function decreaseItem(productId: number) {
  activeProductId.value = productId
  try {
    await cartRequest(`/cart/items/${productId}/decrease/`, { method: 'POST' })
  } catch {
    cartError.value = 'Could not decrease quantity.'
  } finally {
    activeProductId.value = null
  }
}

async function removeItem(productId: number) {
  activeProductId.value = productId
  try {
    await cartRequest(`/cart/items/${productId}/`, { method: 'DELETE' })
  } catch {
    cartError.value = 'Could not remove this product.'
  } finally {
    activeProductId.value = null
  }
}

async function clearCart() {
  isClearing.value = true
  try {
    await cartRequest('/cart/clear/', { method: 'POST' })
  } catch {
    cartError.value = 'Could not clear your cart.'
  } finally {
    isClearing.value = false
  }
}

onMounted(loadCart)
</script>

<template>
  <div class="min-h-screen text-stone-950">
    <SiteHeader :cart-count="cartCount" />

    <main>
      <div class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <section class="mb-8 flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p class="mb-4 inline-flex rounded-full bg-amber-100 px-4 py-2 text-xs font-bold uppercase tracking-[0.18em] text-amber-800">
              Online Clothing Shop
            </p>
            <h1 class="display-title text-5xl font-extrabold sm:text-7xl">
              {{ activeCategoryLabel }}
            </h1>
            <p class="mt-5 max-w-2xl text-lg leading-8 text-stone-600">
              Filter by category, search style names, sort by price, then add pieces to your cart.
            </p>
          </div>
          <p class="w-fit rounded-full bg-stone-950 px-4 py-2 text-sm font-bold text-white shadow-sm shadow-stone-900/10">
            {{ cartCount }} {{ cartCount === 1 ? 'item' : 'items' }} in cart
          </p>
        </section>

        <section class="grid gap-5 xl:grid-cols-[280px_minmax(0,1fr)_360px]">
          <aside class="surface-card h-fit rounded-[1.75rem] p-5 xl:sticky xl:top-24">
            <div class="mb-5 flex items-center justify-between gap-3">
              <div>
                <p class="text-xs font-bold uppercase tracking-[0.18em] text-amber-700">Filters</p>
                <h2 class="text-xl font-extrabold tracking-[-0.04em]">Refine styles</h2>
              </div>
              <button type="button" class="rounded-full px-3 py-1.5 text-sm font-bold text-amber-800 transition hover:bg-amber-100" @click="clearFilters">Reset</button>
            </div>

            <div class="grid gap-4 text-sm font-semibold text-stone-700">
              <label class="grid gap-2">
                <span>Search</span>
                <input v-model="search" class="rounded-2xl border border-stone-200 bg-white/85 px-4 py-3 text-stone-950 outline-none transition focus:border-amber-400 focus:ring-4 focus:ring-amber-100" placeholder="Dress, denim, hoodie...">
              </label>

              <label class="grid gap-2">
                <span>Sort by</span>
                <select v-model="sort" class="rounded-2xl border border-stone-200 bg-white/85 px-4 py-3 text-stone-950 outline-none transition focus:border-amber-400 focus:ring-4 focus:ring-amber-100">
                  <option v-for="option in sortOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
                </select>
              </label>

              <div class="grid grid-cols-2 gap-3">
                <label class="grid gap-2">
                  <span>Min price</span>
                  <input v-model="minPrice" type="number" min="0" class="rounded-2xl border border-stone-200 bg-white/85 px-4 py-3 text-stone-950 outline-none transition focus:border-amber-400 focus:ring-4 focus:ring-amber-100" placeholder="0">
                </label>
                <label class="grid gap-2">
                  <span>Max price</span>
                  <input v-model="maxPrice" type="number" min="0" class="rounded-2xl border border-stone-200 bg-white/85 px-4 py-3 text-stone-950 outline-none transition focus:border-amber-400 focus:ring-4 focus:ring-amber-100" placeholder="150">
                </label>
              </div>

              <div class="flex flex-wrap gap-2 pt-1">
                <button
                  type="button"
                  class="rounded-full px-3 py-2 text-sm font-bold transition"
                  :class="selectedCategory === '' ? 'bg-stone-950 text-white' : 'bg-stone-100 text-stone-700 hover:bg-stone-200'"
                  @click="selectedCategory = ''"
                >
                  All
                </button>
                <button
                  v-for="category in categories"
                  :key="category.value"
                  type="button"
                  class="rounded-full px-3 py-2 text-sm font-bold transition"
                  :class="selectedCategory === category.value ? 'bg-stone-950 text-white' : 'bg-stone-100 text-stone-700 hover:bg-stone-200'"
                  @click="selectedCategory = category.value"
                >
                  {{ category.label }}
                  <span class="ml-1 rounded-full bg-white/25 px-1.5 text-xs">{{ category.count }}</span>
                </button>
              </div>
            </div>
          </aside>

          <div>
            <div class="mb-4 flex items-center justify-between gap-3">
              <p class="font-bold text-stone-600">{{ products.length }} {{ products.length === 1 ? 'product' : 'products' }}</p>
              <button v-if="error" type="button" class="rounded-full bg-stone-950 px-4 py-2 text-sm font-bold text-white" @click="refresh()">Try again</button>
            </div>

            <div v-if="pending" class="surface-card rounded-[1.75rem] p-6">Loading products...</div>

            <div
              v-else-if="error"
              class="rounded-[1.75rem] border border-red-200 bg-red-50 p-5 text-red-900"
            >
              <p class="font-extrabold">Could not load products</p>
              <p class="mt-1 text-sm">Make sure the Django server is running on port 8000.</p>
            </div>

            <div v-else-if="products.length === 0" class="surface-card rounded-[1.75rem] p-6">No matching products. Try changing the filters.</div>

            <div v-else class="grid gap-5 md:grid-cols-2 2xl:grid-cols-3">
              <article
                v-for="product in products"
                :key="product.id"
                class="product-card overflow-hidden rounded-[1.75rem] transition hover:-translate-y-1"
              >
                <div class="relative">
                  <NuxtLink :to="`/products/${product.id}`" aria-label="View product details">
                    <img v-if="product.image_url" :src="product.image_url" :alt="product.name" class="h-64 w-full object-cover">
                    <div v-else class="flex h-64 items-center justify-center bg-stone-200 text-stone-500">No image</div>
                  </NuxtLink>
                  <span v-if="product.featured" class="absolute right-3 top-3 rounded-full bg-amber-300 px-3 py-1 text-xs font-bold text-stone-950">
                    Featured
                  </span>
                </div>

                <div class="p-5">
                  <p class="text-xs font-bold uppercase tracking-[0.16em] text-stone-500">
                    {{ product.brand }} / {{ product.color }} / {{ product.size }}
                  </p>
                  <NuxtLink :to="`/products/${product.id}`">
                    <h2 class="mt-2 text-xl font-extrabold tracking-[-0.04em] hover:text-amber-700">{{ product.name }}</h2>
                  </NuxtLink>
                  <p class="mt-2 line-clamp-2 text-sm leading-6 text-stone-600">{{ product.description }}</p>

                  <div class="mt-5 flex flex-wrap items-center justify-between gap-3">
                    <strong class="text-lg">${{ product.price }}</strong>
                    <NuxtLink :to="`/products/${product.id}`" class="text-sm font-bold text-stone-600 hover:text-stone-950">Details</NuxtLink>
                    <button
                      v-if="!quantitiesByProduct[product.id]"
                      type="button"
                      class="rounded-full bg-stone-950 px-4 py-2 text-sm font-bold text-white transition hover:bg-stone-800 disabled:cursor-wait disabled:opacity-60"
                      :disabled="activeProductId === product.id"
                      @click="addToCart(product.id)"
                    >
                      {{ activeProductId === product.id ? 'Adding...' : 'Add to cart' }}
                    </button>

                    <div v-else class="inline-flex overflow-hidden rounded-full border border-stone-200 bg-white">
                      <button class="px-3 py-2 font-bold disabled:opacity-50" :disabled="activeProductId === product.id" @click="decreaseItem(product.id)">-</button>
                      <span class="bg-stone-100 px-4 py-2 text-sm font-bold">{{ quantitiesByProduct[product.id] }}</span>
                      <button class="px-3 py-2 font-bold disabled:opacity-50" :disabled="activeProductId === product.id" @click="increaseItem(product.id)">+</button>
                    </div>
                  </div>
                </div>
              </article>
            </div>
          </div>

          <aside class="surface-card h-fit rounded-[1.75rem] p-5 xl:sticky xl:top-24">
            <div class="mb-5 flex items-center justify-between gap-3">
              <div>
                <p class="text-xs font-bold uppercase tracking-[0.18em] text-amber-700">Your Cart</p>
                <h2 class="text-xl font-extrabold tracking-[-0.04em]">Order summary</h2>
              </div>
              <strong>${{ cartTotal }}</strong>
            </div>

            <div v-if="cartError" class="mb-4 rounded-2xl border border-red-200 bg-red-50 p-3 text-sm font-semibold text-red-900">{{ cartError }}</div>

            <div v-if="cartItems.length === 0" class="rounded-2xl border border-dashed border-stone-300 bg-stone-100 p-5 text-center">
              <p class="font-extrabold">Cart is empty</p>
              <p class="mt-1 text-sm text-stone-600">Add clothing pieces to see them here.</p>
            </div>

            <div v-else class="grid gap-4">
              <article v-for="item in cartItems" :key="item.product.id" class="grid grid-cols-[4rem_1fr] gap-3">
                <img v-if="item.product.image_url" :src="item.product.image_url" :alt="item.product.name" class="h-16 w-16 rounded-2xl object-cover">
                <div v-else class="h-16 w-16 rounded-2xl bg-stone-200" />

                <div class="min-w-0">
                  <div class="flex items-start justify-between gap-2">
                    <h3 class="truncate font-extrabold">{{ item.product.name }}</h3>
                    <button class="text-xs font-bold text-amber-800 disabled:opacity-50" :disabled="activeProductId === item.product.id" @click="removeItem(item.product.id)">
                      Remove
                    </button>
                  </div>
                  <div class="mt-2 flex items-center justify-between gap-3">
                    <div class="inline-flex overflow-hidden rounded-full border border-stone-200 bg-white text-xs">
                      <button class="px-2.5 py-1.5 font-bold disabled:opacity-50" :disabled="activeProductId === item.product.id" @click="decreaseItem(item.product.id)">-</button>
                      <span class="bg-stone-100 px-3 py-1.5 font-bold">{{ item.quantity }}</span>
                      <button class="px-2.5 py-1.5 font-bold disabled:opacity-50" :disabled="activeProductId === item.product.id" @click="increaseItem(item.product.id)">+</button>
                    </div>
                    <strong>${{ item.line_total }}</strong>
                  </div>
                </div>
              </article>

              <div class="h-px bg-stone-200" />
              <div class="flex items-center justify-between text-lg font-extrabold">
                <span>Total</span>
                <strong>${{ cartTotal }}</strong>
              </div>
              <button class="w-full rounded-full bg-red-50 px-4 py-3 text-sm font-bold text-red-700 transition hover:bg-red-100 disabled:cursor-wait disabled:opacity-60" :disabled="isClearing" @click="clearCart">
                {{ isClearing ? 'Clearing...' : 'Clear cart' }}
              </button>
            </div>
          </aside>
        </section>
      </div>
    </main>

    <SiteFooter />
  </div>
</template>
