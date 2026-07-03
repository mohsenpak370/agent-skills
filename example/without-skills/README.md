# Django + Nuxt Products Page

Simple full-stack clothing shop with a Django backend API, SQLite database, Nuxt UI, Tailwind CSS, product filters, sorting, product detail pages, and cart.

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_products
python manage.py runserver
```

The products API is available at:

```text
http://127.0.0.1:8000/api/products/
http://127.0.0.1:8000/api/products/<product_id>/
```

Product filters are supported with query parameters:

```text
http://127.0.0.1:8000/api/products/?category=women&sort=price_asc&search=dress
```

Categories are available at:

```text
http://127.0.0.1:8000/api/categories/
```

The cart API is available at:

```text
GET    http://127.0.0.1:8000/api/cart/
POST   http://127.0.0.1:8000/api/cart/items/
POST   http://127.0.0.1:8000/api/cart/items/<product_id>/increase/
POST   http://127.0.0.1:8000/api/cart/items/<product_id>/decrease/
DELETE http://127.0.0.1:8000/api/cart/items/<product_id>/
POST   http://127.0.0.1:8000/api/cart/clear/
```

The frontend stores the anonymous `cart_id` in browser `localStorage` and sends it to Django with the `X-Cart-Id` header.

## Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend uses Nuxt UI and Tailwind CSS. Use Node `24.11.0` or newer before running `npm install`.

The landing page is available at:

```text
http://localhost:3000/
```

The products and cart page is available at:

```text
http://localhost:3000/products
```

To use a different API URL, set `NUXT_PUBLIC_API_BASE`:

```bash
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000/api npm run dev
```
