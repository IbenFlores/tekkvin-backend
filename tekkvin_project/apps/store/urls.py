from django.urls import path

from . import cart_views


urlpatterns = [
    # Carrito de compras
    path(
        "carritos/",
        cart_views.carts,
        name="cart-create",
    ),
    path(
        "carritos/<int:cart_id>/",
        cart_views.cart_detail,
        name="cart-detail",
    ),
    path(
        "carritos/<int:cart_id>/items/",
        cart_views.cart_items,
        name="cart-item-add",
    ),
    path(
        "carritos/<int:cart_id>/items/<int:item_id>/",
        cart_views.cart_item_detail,
        name="cart-item-detail",
    ),
]