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

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ProductSupplier)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Sale)