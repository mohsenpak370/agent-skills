<script setup lang="ts">
import type { ProductCategory, ProductSortOption } from '~/types/product'

const props = defineProps<{
  categories: ProductCategory[]
  sortOptions: ProductSortOption[]
  category: ProductCategory['value']
  sortBy: ProductSortOption['value']
  totalItems: number
}>()

const emit = defineEmits<{
  updateCategory: [category: ProductCategory['value']]
  updateSort: [sortBy: ProductSortOption['value']]
}>()

const categoryModel = computed({
  get: () => props.category,
  set: (value) => emit('updateCategory', value as ProductCategory['value']),
})

const sortModel = computed({
  get: () => props.sortBy,
  set: (value) => emit('updateSort', value as ProductSortOption['value']),
})
</script>

<template>
  <section class="threadline-panel grid gap-4 p-4 sm:grid-cols-[1fr_190px_230px] sm:items-end" aria-label="Catalog filters">
    <div>
      <p class="threadline-label">Showing</p>
      <p class="mt-1 text-2xl font-black tracking-[-0.04em] text-threadline-fog">{{ totalItems }} pieces</p>
      <p class="mt-1 text-sm text-zinc-300">Refine the edit without leaving the catalog.</p>
    </div>

    <UFormField label="Category">
      <USelect v-model="categoryModel" :items="categories" class="w-full cursor-pointer" />
    </UFormField>

    <UFormField label="Sort">
      <USelect v-model="sortModel" :items="sortOptions" class="w-full cursor-pointer" />
    </UFormField>
  </section>
</template>
