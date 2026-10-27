import json
from functools import wraps

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


class InvalidRequest(Exception):
    pass


def endpoint(methods):
    def decorate(view):
        @csrf_exempt
        @wraps(view)
        @require_http_methods(methods)
        def wrapped(request, *args, **kwargs):
            try:
                return view(request, *args, **kwargs)
            except InvalidRequest as exc:
                return JsonResponse(
                    {"error": str(exc)},
                    status=400,
                )

        return wrapped

    return decorate


def body(request):
    try:
        value = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        raise InvalidRequest("El cuerpo debe ser JSON válido.")

    if not isinstance(value, dict):
        raise InvalidRequest("Envía un objeto JSON.")

    return value


def positive(value, field):
    if type(value) is not int or not 1 <= value <= 2147483647:
        raise InvalidRequest(
            f"{field} debe ser un entero positivo válido."
        )

    return value


def active_cart(cart):
    if not cart.status:
        raise InvalidRequest(
            "El carrito ya fue confirmado o está cerrado."
        )


def valid_product(product, quantity):
    if not product.status or product.is_active is not True:
        raise InvalidRequest(
            f"El producto {product.pk} no está activo."
        )

    if product.sale_price is None or product.sale_price < 0:
        raise InvalidRequest(
            f"El producto {product.pk} no tiene un precio válido."
        )

    if (
        product.current_stock is None
        or quantity > product.current_stock
    ):
        raise InvalidRequest(
            f"Stock insuficiente para el producto {product.pk}."
        )