from django.contrib import admin
from .models.Category import Category
from .models.Brand import Brand
from .models.Product import Product
from .models.Supplier import Supplier
from .models.Customer import Customer
from .models.Cart import Cart
from .models.CartItem import CartItem
from .models.ProductSupplier import ProductSupplier
from .models.Order import Order
from .models.OrderItem import OrderItem
from .models.Sale import Sale

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent_category", "status")
    search_fields = ("name", "description")
    list_filter = ("status",)
    list_per_page = 20


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "support_url", "status")
    search_fields = ("name",)
    list_filter = ("status",)
    list_per_page = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id", "sku", "name", "sale_price",
        "current_stock", "category", "brand", "status",
    )
    search_fields = ("sku", "name")
    list_filter = ("status", "is_active", "category", "brand")
    list_select_related = ("category", "brand")
    list_per_page = 20


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "id", "company_name", "tax_id", "contact_email", "status",
    )
    search_fields = ("company_name", "tax_id", "contact_email")
    list_filter = ("status",)
    list_per_page = 20


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id", "first_name", "last_name", "email", "status",
    )
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("status",)
    list_per_page = 20


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "created")
    search_fields = ("customer__first_name", "customer__last_name")
    list_filter = ("status",)
    list_per_page = 20


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity", "status")
    search_fields = ("product__name",)
    list_filter = ("status",)
    list_per_page = 20


@admin.register(ProductSupplier)
class ProductSupplierAdmin(admin.ModelAdmin):
    list_display = (
        "id", "product", "supplier", "purchase_price",
        "estimated_delivery_days", "status",
    )
    search_fields = ("product__name", "supplier__company_name")
    list_filter = ("status",)
    list_per_page = 20


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", "customer", "total_amount", "status", "created",
    )
    search_fields = ("customer__first_name", "customer__last_name")
    list_filter = ("status",)
    list_per_page = 20


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id", "order", "product", "quantity", "unit_price", "subtotal",
    )
    search_fields = ("product__name",)
    list_per_page = 20


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "id", "order", "receipt_number", "payment_method",
        "payment_status", "total_amount", "issued_at",
    )
    search_fields = ("receipt_number",)
    list_filter = ("payment_status", "payment_method", "receipt_type")
    list_per_page = 20
