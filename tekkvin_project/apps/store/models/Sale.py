from django.db import models
from .Order import Order

class Sale(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    receipt_type = models.CharField(max_length=255)
    receipt_number = models.CharField(max_length=255, unique=True)
    payment_status = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
    tax_base = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'sale'