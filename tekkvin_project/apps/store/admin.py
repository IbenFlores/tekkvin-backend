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
    exclude = ('created_id', 'modified_id')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_id = request.user.id
        obj.modified_id = request.user.id
        super().save_model(request, obj, form, change)

admin.site.register(Category, AuditAdmin)
admin.site.register(Brand, AuditAdmin)
admin.site.register(Product, AuditAdmin)
admin.site.register(Supplier, AuditAdmin)
admin.site.register(Customer, AuditAdmin)
admin.site.register(Cart, AuditAdmin)
admin.site.register(CartItem, AuditAdmin)
admin.site.register(ProductSupplier, AuditAdmin)
admin.site.register(Order, AuditAdmin)
admin.site.register(OrderItem, AuditAdmin)
admin.site.register(Sale, AuditAdmin)