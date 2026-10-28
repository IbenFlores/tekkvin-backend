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


class AuditAdmin(admin.ModelAdmin):
    exclude = ("created_id", "modified_id")
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_id = request.user.id
        obj.modified_id = request.user.id
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(AuditAdmin):
    list_display = ("id", "name", "parent_category", "status", "created")
    search_fields = ("name", "description")
    list_filter = ("status",)


@admin.register(Brand)
class BrandAdmin(AuditAdmin):
    list_display = ("id", "name", "status", "created")
    search_fields = ("name", "support_url")
    list_filter = ("status",)


@admin.register(Product)
class ProductAdmin(AuditAdmin):
    list_display = (
        "id", "sku", "name", "sale_price",
        "current_stock", "minimum_stock", "category", "brand", "status"
    )
    search_fields = ("sku", "name")
    list_filter = ("status", "category", "brand")
    list_select_related = ("category", "brand")


@admin.register(Supplier)
class SupplierAdmin(AuditAdmin):
    list_display = (
        "id", "company_name", "tax_id", "contact_email", "phone", "status"
    )
    search_fields = ("company_name", "tax_id", "contact_email")
    list_filter = ("status",)


@admin.register(Customer)
class CustomerAdmin(AuditAdmin):
    list_display = (
        "id", "first_name", "last_name", "email", "status", "created"
    )
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("status",)


@admin.register(Cart)
class CartAdmin(AuditAdmin):
    list_display = ("id", "customer", "status", "created")
    search_fields = ("customer__first_name", "customer__last_name")
    list_filter = ("status",)
    list_select_related = ("customer",)


@admin.register(CartItem)
class CartItemAdmin(AuditAdmin):
    list_display = ("id", "cart", "product", "quantity", "status", "created")
    search_fields = ("product__name", "product__sku")
    list_filter = ("status",)
    list_select_related = ("cart", "product")


@admin.register(ProductSupplier)
class ProductSupplierAdmin(AuditAdmin):
    list_display = (
        "id", "product", "supplier", "purchase_price",
        "estimated_delivery_days", "status"
    )
    search_fields = ("product__name", "supplier__company_name")
    list_filter = ("status",)
    list_select_related = ("product", "supplier")


@admin.register(Order)
class OrderAdmin(AuditAdmin):
    list_display = ("id", "customer", "total_amount", "status", "created")
    search_fields = (
        "customer__first_name", "customer__last_name", "customer__email"
    )
    list_filter = ("status",)
    list_select_related = ("customer",)


@admin.register(OrderItem)
class OrderItemAdmin(AuditAdmin):
    list_display = (
        "id", "order", "product", "quantity", "unit_price", "subtotal"
    )
    search_fields = ("product__name", "product__sku")
    list_select_related = ("order", "product")


@admin.register(Sale)
class SaleAdmin(AuditAdmin):
    list_display = (
        "id", "order", "receipt_number", "receipt_type",
        "payment_status", "payment_method", "total_amount"
    )
    search_fields = ("receipt_number", "payment_status", "payment_method")
    list_filter = ("receipt_type", "payment_status", "payment_method")
    list_select_related = ("order",)
