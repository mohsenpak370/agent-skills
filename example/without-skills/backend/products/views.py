import json
import uuid
from decimal import Decimal

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .models import Cart, CartItem, Product


def _product_payload(product):
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "brand": product.brand,
        "size": product.size,
        "color": product.color,
        "price": str(product.price),
        "image_url": product.image_url,
        "featured": product.featured,
    }


@require_GET
def product_list(request):
    products = Product.objects.filter(is_available=True)

    category = request.GET.get("category")
    search = request.GET.get("search")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    featured = request.GET.get("featured")
    sort = request.GET.get("sort", "name")

    if category:
        products = products.filter(category=category)
    if search:
        products = products.filter(
            Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(brand__icontains=search)
            | Q(color__icontains=search)
        )
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if featured == "true":
        products = products.filter(featured=True)

    sort_options = {
        "name": "name",
        "newest": "-created_at",
        "price_asc": "price",
        "price_desc": "-price",
    }
    products = products.order_by(sort_options.get(sort, "name"))
    return JsonResponse({"products": [_product_payload(product) for product in products]})


@require_GET
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id, is_available=True)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found."}, status=404)

    related_products = Product.objects.filter(
        category=product.category,
        is_available=True,
    ).exclude(id=product.id).order_by("name")[:4]

    return JsonResponse(
        {
            "product": _product_payload(product),
            "related_products": [_product_payload(related_product) for related_product in related_products],
        }
    )


@require_GET
def category_list(request):
    categories = []
    for value, label in Product.Category.choices:
        categories.append(
            {
                "value": value,
                "label": label,
                "count": Product.objects.filter(category=value, is_available=True).count(),
            }
        )
    return JsonResponse({"categories": categories})


def _get_or_create_cart(request):
    cart_id = request.headers.get("X-Cart-Id")
    if cart_id:
        try:
            return Cart.objects.get(id=uuid.UUID(cart_id))
        except (Cart.DoesNotExist, ValueError):
            pass

    return Cart.objects.create(id=uuid.uuid4())


def _cart_payload(cart):
    items = []
    total_items = 0
    total_price = Decimal("0.00")

    cart_items = cart.items.select_related("product").filter(product__is_available=True)
    for item in cart_items:
        line_total = item.product.price * item.quantity
        total_items += item.quantity
        total_price += line_total
        items.append(
            {
                "product": {
                    **_product_payload(item.product),
                },
                "quantity": item.quantity,
                "line_total": str(line_total),
            }
        )

    return {
        "cart_id": str(cart.id),
        "items": items,
        "total_items": total_items,
        "total_price": str(total_price),
    }


def _json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None


@require_GET
def cart_detail(request):
    cart = _get_or_create_cart(request)
    return JsonResponse(_cart_payload(cart))


@csrf_exempt
@require_POST
def add_cart_item(request):
    body = _json_body(request)
    if body is None:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    product_id = body.get("product_id")
    try:
        quantity = int(body.get("quantity", 1))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Quantity must be a number."}, status=400)
    if quantity < 1:
        return JsonResponse({"error": "Quantity must be at least 1."}, status=400)

    try:
        product = Product.objects.get(id=product_id, is_available=True)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found."}, status=404)

    cart = _get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    item.quantity = quantity if created else item.quantity + quantity
    item.save(update_fields=["quantity"])

    return JsonResponse(_cart_payload(cart), status=201)


@csrf_exempt
@require_POST
def increase_cart_item(request, product_id):
    cart = _get_or_create_cart(request)
    try:
        item = CartItem.objects.get(cart=cart, product_id=product_id, product__is_available=True)
    except CartItem.DoesNotExist:
        return JsonResponse({"error": "Cart item not found."}, status=404)

    item.quantity += 1
    item.save(update_fields=["quantity"])
    return JsonResponse(_cart_payload(cart))


@csrf_exempt
@require_POST
def decrease_cart_item(request, product_id):
    cart = _get_or_create_cart(request)
    try:
        item = CartItem.objects.get(cart=cart, product_id=product_id, product__is_available=True)
    except CartItem.DoesNotExist:
        return JsonResponse({"error": "Cart item not found."}, status=404)

    if item.quantity == 1:
        item.delete()
    else:
        item.quantity -= 1
        item.save(update_fields=["quantity"])

    return JsonResponse(_cart_payload(cart))


@csrf_exempt
@require_http_methods(["DELETE"])
def remove_cart_item(request, product_id):
    cart = _get_or_create_cart(request)
    CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    return JsonResponse(_cart_payload(cart))


@csrf_exempt
@require_POST
def clear_cart(request):
    cart = _get_or_create_cart(request)
    cart.items.all().delete()
    return JsonResponse(_cart_payload(cart))
