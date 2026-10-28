from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator
from .Product import Product
from .Supplier import Supplier

class ProductSupplier(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,  validators=[MinValueValidator(0)])
    estimated_delivery_days = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_id = models.IntegerField(null=True, blank=True)
    modified_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'product_suppliers'
        unique_together = (("product", "supplier"),)
        constraints = [
            models.CheckConstraint(
                condition=Q(purchase_price__gte=0) | Q(purchase_price__isnull=True),
                name="product_supplier_price_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(estimated_delivery_days__gte=0)
                | Q(estimated_delivery_days__isnull=True),
                name="product_supplier_delivery_days_nonnegative"
            ),
        ]