export default defineNuxtConfig({
  compatibilityDate: '2025-01-01',
  modules: ['@nuxt/ui'],
  css: ['~/assets/main.css'],
  app: {
    head: {
      htmlAttrs: {
        lang: 'en',
      },
      titleTemplate: (title) => title ? `${title} | Threadline Atelier` : 'Threadline Atelier | Luxury Fashion Edit',
      meta: [
        { name: 'description', content: 'Shop Threadline Atelier, a cold-luxury fashion edit of refined wardrobe pieces, quiet tailoring, accessories, and private client service.' },
        { name: 'theme-color', content: '#09090b' },
        { property: 'og:site_name', content: 'Threadline Atelier' },
        { property: 'og:type', content: 'website' },
        { name: 'twitter:card', content: 'summary_large_image' },
      ],
    },
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000/api',
      siteUrl: process.env.NUXT_PUBLIC_SITE_URL || 'http://localhost:3000',
    },
  },
})
