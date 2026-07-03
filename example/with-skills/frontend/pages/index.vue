<script setup lang="ts">
const config = useRuntimeConfig()

useSeoMeta({
  title: 'Luxury Fashion Edit',
  description: 'Shop Threadline Atelier, a refined luxury fashion edit of wardrobe pieces, accessories, quiet tailoring, and private client service.',
  robots: 'noindex, follow',
})

useHead({
  link: [
    { rel: 'canonical', href: `${config.public.siteUrl}/products` },
  ],
})

await navigateTo('/products')
</script>

<template>
  <p>Opening Threadline...</p>
</template>
