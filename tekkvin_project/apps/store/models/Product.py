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
    created_id = models.IntegerField()
    modified_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return str(self.name)