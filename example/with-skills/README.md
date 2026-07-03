# Django + Nuxt Products Demo

Simple two-part project:

- `backend`: Django API with clothing products, filtering, sorting, and a SQLite-backed cart
- `frontend`: Nuxt online-shop landing page at `/products` with categories, filters, sorting, cart, header, and footer

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

Useful API URLs:

- `GET http://127.0.0.1:8000/api/products/?category=women&sortBy=priceAsc`
- `GET http://127.0.0.1:8000/api/products/<product-id>/`
- `GET http://127.0.0.1:8000/api/cart/?cartId=<cart-id>`
- `POST http://127.0.0.1:8000/api/cart/items/`
- `PATCH http://127.0.0.1:8000/api/cart/items/<item-id>/`
- `DELETE http://127.0.0.1:8000/api/cart/items/<item-id>/`

The Nuxt client stores `cartId` in `localStorage`; Django stores the cart and cart items in SQLite.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Online shop page: `http://localhost:3000/products`

Product details page: `http://localhost:3000/products/1`

If the backend runs somewhere else, set `NUXT_PUBLIC_API_BASE`, for example:

```bash
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000/api npm run dev
```
