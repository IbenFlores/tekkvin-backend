from django.core.exceptions import ValidationError
from django.db import models
from .Category import Category
from .Brand import Brand

class Product(models.Model):
    sku = models.CharField(max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    technical_specifications = models.JSONField(null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_stock = models.IntegerField(null=True, blank=True)
    minimum_stock = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    create_id = models.IntegerField()
    modified_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "products"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(sale_price__gte=0),
                name="product_sale_price_nonnegativo",
            ),
            models.CheckConstraint(
                condition=models.Q(current_stock__gte=0),
                name="product_stock_nonnegative",
            ),
            models.CheckConstraint(
                condition=models.Q(minimum_stock__gte=0),
                name="product_min_stock_nonnegative",
            ),
        ]

    def clean(self):
        super().clean()
        errors = {}

        if self.name is not None and not self.name.strip():
            errors["name"] = "El nombre del producto no puede estar vacío."

        if self.sale_price is not None and self.sale_price < 0:
            errors["sale_price"] = "El precio no puede ser negativo."

        if self.current_stock is not None and self.current_stock < 0:
            errors["current_stock"] = "El stock no puede ser negativo."

        if self.minimum_stock is not None and self.minimum_stock < 0:
            errors["minimum_stock"] = (
                "El stock mínimo no puede ser negativo."
            )

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return str(self.name)
