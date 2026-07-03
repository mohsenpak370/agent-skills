import type { ProductListResponse } from '~/types/product'

function xmlEscape(value: string) {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;')
}

function urlEntry(location: string, priority: string) {
  return [
    '  <url>',
    `    <loc>${xmlEscape(location)}</loc>`,
    '    <changefreq>daily</changefreq>',
    `    <priority>${priority}</priority>`,
    '  </url>',
  ].join('\n')
}

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const siteUrl = config.public.siteUrl.replace(/\/$/, '')
  const urls = [urlEntry(`${siteUrl}/products`, '1.0')]

  try {
    const response = await $fetch<ProductListResponse>(`${config.public.apiBase}/products/`, {
      query: { page: 1, pageSize: 100, category: 'all', sortBy: 'featured' },
    })

    urls.push(
      ...response.data.map((product) => urlEntry(`${siteUrl}/products/${product.id}`, '0.8')),
    )
  } catch {
    // Keep sitemap available even if the product API is temporarily down.
  }

  setHeader(event, 'content-type', 'application/xml; charset=utf-8')

  return [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ...urls,
    '</urlset>',
  ].join('\n')
})
