import json
from decimal import Decimal

from django.test import Client, TestCase

from .models import Cart, Customer, Order, Product


class ShoppingApiTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Kevin",
            last_name="Prueba",
            email="kevin@example.com",
            created_id=0,
        )

        self.product = Product.objects.create(
            name="Producto",
            sale_price=Decimal("20.00"),
            current_stock=5,
            is_active=True,
            create_id=0,
        )

    def send(self, method, url, data=None):
        return getattr(self.client, method)(
            url,
            data=json.dumps({} if data is None else data),
            content_type="application/json",
        )

    def cart(self, quantity=2):
        response = self.send(
            "post",
            "/api/carritos/",
            {"customer_id": self.customer.pk},
        )
        self.assertEqual(response.status_code, 201)

        cart_id = response.json()["id"]

        response = self.send(
            "post",
            f"/api/carritos/{cart_id}/items/",
            {
                "product_id": self.product.pk,
                "quantity": quantity,
            },
        )
        self.assertEqual(response.status_code, 201)

        item_id = response.json()["items"][0]["id"]

        return cart_id, item_id

    def test_purchase_and_cancel(self):
        cart_id, _ = self.cart()

        response = self.send(
            "post",
            "/api/pedidos/",
            {"cart_id": cart_id},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["total"], "40.00")

        order_id = response.json()["id"]

        self.product.refresh_from_db()
        self.assertEqual(self.product.current_stock, 3)

        # Un carrito confirmado no puede generar otro pedido.
        response = self.send(
            "post",
            "/api/pedidos/",
            {"cart_id": cart_id},
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.get(
            f"/api/pedidos/{order_id}/"
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/api/pedidos/")
        self.assertEqual(response.json()["count"], 1)

        response = self.send(
            "patch",
            f"/api/pedidos/{order_id}/cancelar/",
        )
        self.assertEqual(response.status_code, 200)

        # No debe devolver el stock por segunda vez.
        response = self.send(
            "patch",
            f"/api/pedidos/{order_id}/cancelar/",
        )
        self.assertEqual(response.status_code, 400)

        self.product.refresh_from_db()
        self.assertEqual(self.product.current_stock, 5)

    def test_cart_updates_and_delete(self):
        cart_id, item_id = self.cart()
        url = f"/api/carritos/{cart_id}/items/{item_id}/"

        response = self.send(
            "patch",
            url,
            {"quantity": 0},
        )
        self.assertEqual(response.status_code, 400)

        response = self.send(
            "patch",
            url,
            {"quantity": 4},
        )
        self.assertEqual(response.json()["total"], "80.00")

        response = self.send("delete", url)
        self.assertEqual(response.json()["items"], [])

        response = self.send(
            "post",
            "/api/pedidos/",
            {"cart_id": cart_id},
        )
        self.assertEqual(response.status_code, 400)

    def test_insufficient_stock_rolls_back(self):
        cart_id, _ = self.cart()

        self.product.current_stock = 1
        self.product.save()

        response = self.send(
            "post",
            "/api/pedidos/",
            {"cart_id": cart_id},
        )
        self.assertEqual(response.status_code, 400)

        self.assertEqual(Order.objects.count(), 0)
        self.assertTrue(
            Cart.objects.get(pk=cart_id).status
        )

    def test_bad_input(self):
        response = self.send(
            "post",
            "/api/carritos/",
            [],
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            "/api/carritos/",
            data="{",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response = self.send(
            "post",
            "/api/carritos/",
            {"customer_id": True},
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.get(
            "/api/pedidos/?page=abc"
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.get(
            "/api/carritos/9999/"
        )
        self.assertEqual(response.status_code, 404)

    def test_public_access_without_session_or_csrf(self):
        public = Client(enforce_csrf_checks=True)

        response = public.get("/api/pedidos/")
        self.assertEqual(response.status_code, 200)

        response = public.post(
            "/api/carritos/",
            data=json.dumps({
                "customer_id": self.customer.pk,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        cart_id = response.json()["id"]

        self.assertEqual(
            Cart.objects.get(pk=cart_id).created_id,
            0,
        )

        response = public.post(
            f"/api/carritos/{cart_id}/items/",
            data=json.dumps({
                "product_id": self.product.pk,
                "quantity": 2,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        item_id = response.json()["items"][0]["id"]
        url = f"/api/carritos/{cart_id}/items/{item_id}/"

        response = public.patch(
            url,
            data=json.dumps({"quantity": 3}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        response = public.post(
            "/api/pedidos/",
            data=json.dumps({"cart_id": cart_id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        order_id = response.json()["id"]

        self.assertEqual(
            Order.objects.get(pk=order_id).created_id,
            0,
        )

        response = public.patch(
            f"/api/pedidos/{order_id}/cancelar/"
        )
        self.assertEqual(response.status_code, 200)

        other_cart, other_item = self.cart()

        response = public.delete(
            f"/api/carritos/{other_cart}/items/{other_item}/"
        )
        self.assertEqual(response.status_code, 200)