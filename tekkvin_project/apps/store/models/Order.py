from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator
from .Customer import Customer

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_id = models.IntegerField()
    modified_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "orders"
        constraints = [
            models.CheckConstraint(
                condition=Q(total_amount__gte=0),
                name="order_total_nonnegative"
            ),
        ]