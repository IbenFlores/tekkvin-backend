
from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator
from .Order import Order


class Sale(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    receipt_type = models.CharField(max_length=255)
    receipt_number = models.CharField(max_length=255, unique=True)
    payment_status = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
    tax_base = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)],)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)],)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)],)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_id = models.IntegerField(null=True, blank=True)
    modified_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "sale"
        constraints = [
            models.CheckConstraint(
                condition=Q(tax_base__gte=0),
                name="sale_tax_base_nonnegative",
            ),
            models.CheckConstraint(
                condition=Q(tax_amount__gte=0),
                name="sale_tax_amount_nonnegative",
            ),
            models.CheckConstraint(
                condition=Q(total_amount__gte=0),
                name="sale_total_nonnegative",
            ),
        ]
