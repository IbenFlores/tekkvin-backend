from decimal import Decimal

from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .api_common import (
    InvalidRequest,
    active_cart,
    body,
    endpoint,
    positive,
    valid_product,
)
from .models import Cart, Order, OrderItem, Product


def order_data(order):
    items = (
        order.orderitem_set
        .select_related("product")
        .order_by("pk")
    )

    return {
        "id": order.pk,
        "customer_id": order.customer_id,
        "status": (
            "registrado" if order.status else "cancelado"
        ),
        "created": order.created.isoformat(),
        "total": str(order.total_amount),
        "items": [
            {
                "id": item.pk,
                "product_id": item.product_id,
                "name": item.product.name,
                "quantity": item.quantity,
                "unit_price": str(item.unit_price),
                "subtotal": str(item.subtotal),
            }
            for item in items
        ],
    }


@endpoint(["GET", "POST"])
def orders(request):
    if request.method == "POST":
        return create_order(request)

    queryset = Order.objects.order_by("-pk")

    customer_id = request.GET.get("customer_id")

    if customer_id:
        try:
            customer_id = int(customer_id)
        except ValueError:
            raise InvalidRequest(
                "customer_id debe ser un entero positivo."
            )

        queryset = queryset.filter(
            customer_id=positive(customer_id, "customer_id")
        )

    try:
        page = int(request.GET.get("page", "1"))
    except ValueError:
        raise InvalidRequest(
            "page debe ser un entero positivo."
        )

    positive(page, "page")
    start = (page - 1) * 20

    return JsonResponse({
        "page": page,
        "count": queryset.count(),
        "results": [
            order_data(order)
            for order in queryset[start:start + 20]
        ],
    })


@transaction.atomic
def create_order(request):
    cart_id = positive(
        body(request).get("cart_id"),
        "cart_id",
    )

    cart = get_object_or_404(
        Cart.objects.select_for_update(),
        pk=cart_id,
    )
    active_cart(cart)

    if cart.customer is None or not cart.customer.status:
        raise InvalidRequest(
            "El carrito necesita un cliente activo."
        )

    items = list(
        cart.cartitem_set
        .filter(status=True)
        .order_by("pk")
    )

    if not items:
        raise InvalidRequest("El carrito está vacío.")

    quantities = {}

    for item in items:
        if item.product_id is None:
            raise InvalidRequest("Hay un ítem sin producto.")

        quantity = positive(item.quantity, "quantity")

        quantities[item.product_id] = (
            quantities.get(item.product_id, 0) + quantity
        )

    products = {
        product.pk: product
        for product in (
            Product.objects
            .select_for_update()
            .filter(pk__in=quantities)
            .order_by("pk")
        )
    }

    total = Decimal("0.00")
    lines = []

    for product_id, quantity in quantities.items():
        product = products.get(product_id)

        if product is None:
            raise InvalidRequest(
                "Un producto ya no existe."
            )

        valid_product(product, quantity)

        subtotal = product.sale_price * quantity
        total += subtotal

        if total > Decimal("9999999999.99"):
            raise InvalidRequest(
                "El total supera el límite permitido."
            )

        lines.append((product, quantity, subtotal))

    order = Order.objects.create(
        customer=cart.customer,
        total_amount=total,
        created_id=0,
    )

    for product, quantity, subtotal in lines:
        updated = Product.objects.filter(
            pk=product.pk,
            current_stock__gte=quantity,
        ).update(
            current_stock=F("current_stock") - quantity
        )

        if not updated:
            raise InvalidRequest(
                "El stock cambió. Vuelve a intentar."
            )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            unit_price=product.sale_price,
            subtotal=subtotal,
        )

    cart.status = False
    cart.modified_id = 0
    cart.save()

    return JsonResponse(order_data(order), status=201)


@endpoint(["GET"])
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    return JsonResponse(order_data(order))


@endpoint(["PATCH"])
@transaction.atomic
def cancel_order(request, order_id):
    order = get_object_or_404(
        Order.objects.select_for_update(),
        pk=order_id,
    )

    if not order.status:
        raise InvalidRequest(
            "El pedido ya está cancelado."
        )

    if order.sale_set.exists():
        raise InvalidRequest(
            "El pedido tiene una venta asociada y no puede "
            "cancelarse por esta ruta."
        )

    items = list(
        order.orderitem_set.order_by("product_id")
    )

    # Bloquear productos en motores compatibles.
    list(
        Product.objects
        .select_for_update()
        .filter(pk__in=[item.product_id for item in items])
        .order_by("pk")
    )

    updated = Order.objects.filter(
        pk=order.pk,
        status=True,
    ).update(
        status=False,
        modified_id=0,
        modified=timezone.now(),
    )

    if not updated:
        raise InvalidRequest(
            "El pedido ya está cancelado."
        )

    for item in items:
        Product.objects.filter(
            pk=item.product_id
        ).update(
            current_stock=F("current_stock") + item.quantity
        )

    order.refresh_from_db()

    return JsonResponse(order_data(order))