import json
import uuid
from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Cart, CartItem, Product


MAX_CART_ITEM_QUANTITY = 99
PRODUCT_SORT_OPTIONS = {
    "featured": "name",
    "priceAsc": "price",
    "priceDesc": "-price",
    "newest": "-created_at",
}


def _positive_int_query_param(request: HttpRequest, name: str, default: int, maximum: int | None = None) -> int:
    raw_value = request.GET.get(name, str(default))

    try:
        value = int(raw_value)
    except ValueError:
        raise ValueError(f"{name} must be a number.")

    value = max(value, 1)
    if maximum is not None:
        value = min(value, maximum)
    return value


def _product_payload(product: Product) -> dict:
    return {
        "id": product.id,
        "name": product.name,
        "category": product.category,
        "description": product.description,
        "price": str(product.price),
        "imageUrl": product.image_url,
        "isAvailable": product.is_available,
    }


def product_list(request: HttpRequest) -> JsonResponse:
    try:
        page = _positive_int_query_param(request, "page", 1)
        page_size = _positive_int_query_param(request, "pageSize", 20, maximum=100)
    except ValueError as error:
        return JsonResponse(
            {"error": {"code": "INVALID_QUERY", "message": str(error)}},
            status=400,
        )

    category = request.GET.get("category", "all")
    sort_by = request.GET.get("sortBy", "featured")

    if category != "all" and category not in dict(Product.CATEGORY_CHOICES):
        return JsonResponse(
            {"error": {"code": "INVALID_CATEGORY", "message": "category is not supported."}},
            status=400,
        )
    if sort_by not in PRODUCT_SORT_OPTIONS:
        return JsonResponse(
            {"error": {"code": "INVALID_SORT", "message": "sortBy is not supported."}},
            status=400,
        )

    queryset = Product.objects.filter(is_available=True)
    if category != "all":
        queryset = queryset.filter(category=category)
    queryset = queryset.order_by(PRODUCT_SORT_OPTIONS[sort_by], "name")
    paginator = Paginator(queryset, page_size)
    products_page = paginator.get_page(page)

    return JsonResponse(
        {
            "data": [
                _product_payload(product)
                for product in products_page.object_list
            ],
            "pagination": {
                "page": products_page.number,
                "pageSize": page_size,
                "totalItems": paginator.count,
                "totalPages": paginator.num_pages,
            },
        }
    )


def product_detail(request: HttpRequest, product_id: int) -> JsonResponse:
    try:
        product = Product.objects.get(id=product_id, is_available=True)
    except Product.DoesNotExist:
        return _error_response("PRODUCT_NOT_FOUND", "Product was not found.", 404)

    return JsonResponse(_product_payload(product))


def _error_response(code: str, message: str, status: int) -> JsonResponse:
    return JsonResponse({"error": {"code": code, "message": message}}, status=status)


def _request_body(request: HttpRequest) -> dict:
    try:
        body = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        raise ValueError("Request body must be valid JSON.")

    if not isinstance(body, dict):
        raise ValueError("Request body must be a JSON object.")
    return body


def _quantity(value: object, default: int = 1) -> int:
    if value is None:
        return default

    try:
        quantity = int(value)
    except (TypeError, ValueError):
        raise ValueError("quantity must be a number.")

    if quantity < 1 or quantity > MAX_CART_ITEM_QUANTITY:
        raise ValueError(f"quantity must be between 1 and {MAX_CART_ITEM_QUANTITY}.")
    return quantity


def _cart_token_from_request(request: HttpRequest, body: dict | None = None) -> str:
    token = request.GET.get("cartId") or request.headers.get("X-Cart-Id")
    if body is not None:
        token = body.get("cartId") or token

    if token is None or token == "":
        return uuid.uuid4().hex
    if not isinstance(token, str) or len(token) > 64:
        raise ValueError("cartId must be a string with at most 64 characters.")
    return token


def _get_or_create_cart(token: str) -> Cart:
    cart, _created = Cart.objects.get_or_create(token=token)
    return cart


def _cart_payload(cart: Cart) -> dict:
    items = cart.items.select_related("product")
    subtotal = Decimal("0.00")
    data = []

    for item in items:
        product = item.product
        line_total = product.price * item.quantity
        subtotal += line_total
        data.append(
            {
                "id": item.id,
                "quantity": item.quantity,
                "lineTotal": str(line_total),
                "product": _product_payload(product),
            }
        )

    return {
        "cartId": cart.token,
        "items": data,
        "summary": {
            "itemCount": sum(item["quantity"] for item in data),
            "subtotal": str(subtotal),
        },
    }


@csrf_exempt
@require_http_methods(["GET", "DELETE"])
def cart_detail(request: HttpRequest) -> JsonResponse:
    try:
        token = _cart_token_from_request(request)
    except ValueError as error:
        return _error_response("INVALID_CART", str(error), 400)

    cart = _get_or_create_cart(token)

    if request.method == "DELETE":
        cart.items.all().delete()

    return JsonResponse(_cart_payload(cart))


@csrf_exempt
@require_http_methods(["POST"])
def cart_items(request: HttpRequest) -> JsonResponse:
    try:
        body = _request_body(request)
        token = _cart_token_from_request(request, body)
        product_id = int(body.get("productId"))
        quantity = _quantity(body.get("quantity"), default=1)
    except (TypeError, ValueError) as error:
        return _error_response("INVALID_CART_ITEM", str(error), 400)

    try:
        product = Product.objects.get(id=product_id, is_available=True)
    except Product.DoesNotExist:
        return _error_response("PRODUCT_NOT_FOUND", "Product was not found.", 404)

    cart = _get_or_create_cart(token)
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": quantity},
    )

    if not created:
        item.quantity = min(item.quantity + quantity, MAX_CART_ITEM_QUANTITY)
        item.save(update_fields=["quantity", "updated_at"])

    cart.save(update_fields=["updated_at"])
    return JsonResponse(_cart_payload(cart), status=201)


@csrf_exempt
@require_http_methods(["PATCH", "DELETE"])
def cart_item_detail(request: HttpRequest, item_id: int) -> JsonResponse:
    try:
        body = _request_body(request) if request.method == "PATCH" else {}
        token = _cart_token_from_request(request, body)
        cart = Cart.objects.get(token=token)
        item = cart.items.get(id=item_id)
    except ValueError as error:
        return _error_response("INVALID_CART_ITEM", str(error), 400)
    except ObjectDoesNotExist:
        return _error_response("CART_ITEM_NOT_FOUND", "Cart item was not found.", 404)

    if request.method == "DELETE":
        item.delete()
    else:
        try:
            item.quantity = _quantity(body.get("quantity"))
        except ValueError as error:
            return _error_response("INVALID_CART_ITEM", str(error), 400)
        item.save(update_fields=["quantity", "updated_at"])

    cart.save(update_fields=["updated_at"])
    return JsonResponse(_cart_payload(cart))
