from decimal import Decimal

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .api_common import (
    InvalidRequest,
    active_cart,
    body,
    endpoint,
    positive,
    valid_product,
)
from .models import Cart, CartItem, Customer, Product


def cart_data(cart):
    items = []
    total = Decimal("0.00")

    queryset = (
        cart.cartitem_set
        .filter(status=True)
        .select_related("product")
        .order_by("pk")
    )

    for item in queryset:
        price = (
            item.product.sale_price
            if item.product
            else None
        )

        subtotal = (
            price * item.quantity
            if price is not None and item.quantity
            else None
        )

        if subtotal is not None:
            total += subtotal

        items.append({
            "id": item.pk,
            "product_id": item.product_id,
            "name": item.product.name if item.product else None,
            "quantity": item.quantity,
            "unit_price": (
                str(price) if price is not None else None
            ),
            "subtotal": (
                str(subtotal) if subtotal is not None else None
            ),
        })

    return {
        "id": cart.pk,
        "customer_id": cart.customer_id,
        "active": cart.status,
        "items": items,
        "total": str(total),
    }


@endpoint(["POST"])
def carts(request):
    data = body(request)

    customer = get_object_or_404(
        Customer,
        pk=positive(data.get("customer_id"), "customer_id"),
        status=True,
    )

    cart = Cart.objects.create(
        customer=customer,
        created_id=0,
    )

    return JsonResponse(cart_data(cart), status=201)


@endpoint(["GET"])
def cart_detail(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id)

    return JsonResponse(cart_data(cart))


@endpoint(["POST"])
@transaction.atomic
def cart_items(request, cart_id):
    data = body(request)
    quantity = positive(data.get("quantity"), "quantity")

    cart = get_object_or_404(
        Cart.objects.select_for_update(),
        pk=cart_id,
    )
    active_cart(cart)

    product = get_object_or_404(
        Product,
        pk=positive(data.get("product_id"), "product_id"),
    )

    existing = list(
        cart.cartitem_set
        .filter(product=product, status=True)
        .order_by("pk")
    )

    quantity += sum(item.quantity or 0 for item in existing)

    positive(quantity, "quantity acumulada")
    valid_product(product, quantity)

    if existing:
        item = existing[0]
        item.quantity = quantity
        item.modified_id = 0
        item.save()

        CartItem.objects.filter(
            pk__in=[item.pk for item in existing[1:]]
        ).delete()
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity,
            created_id=0,
        )

    return JsonResponse(cart_data(cart), status=201)


@endpoint(["PATCH", "DELETE"])
@transaction.atomic
def cart_item_detail(request, cart_id, item_id):
    cart = get_object_or_404(
        Cart.objects.select_for_update(),
        pk=cart_id,
    )
    active_cart(cart)

    item = get_object_or_404(
        CartItem,
        pk=item_id,
        cart=cart,
        status=True,
    )

    if request.method == "DELETE":
        item.delete()
    else:
        quantity = positive(
            body(request).get("quantity"),
            "quantity",
        )

        if item.product is None:
            raise InvalidRequest(
                "El ítem no tiene un producto válido."
            )

        valid_product(item.product, quantity)

        item.quantity = quantity
        item.modified_id = 0
        item.save()

    return JsonResponse(cart_data(cart))