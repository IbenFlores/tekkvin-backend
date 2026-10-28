
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from .Order import Order
from .Product import Product

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)],)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_id = models.IntegerField(null=True, blank=True)
    modified_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "order_item"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name="order_item_quantity_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(unit_price__gte=0),
                name="order_item_unit_price_nonnegative",
            ),
            models.CheckConstraint(
                condition=models.Q(subtotal__gte=0),
                name="order_item_subtotal_nonnegative",
            ),
        ]

    def clean(self):
        super().clean()
        errors = {}

        if self.quantity is not None and self.quantity <= 0:
            errors["quantity"] = "La cantidad debe ser mayor que cero."

        if self.unit_price is not None and self.unit_price < 0:
            errors["unit_price"] = (
                "El precio unitario no puede ser negativo."
            )

        if self.subtotal is not None and self.subtotal < 0:
            errors["subtotal"] = "El subtotal no puede ser negativo."

        if (
            self.quantity is not None
            and self.unit_price is not None
            and self.subtotal is not None
            and self.subtotal != self.quantity * self.unit_price
        ):
            errors["subtotal"] = (
                "El subtotal debe ser igual a cantidad por precio unitario."
            )

        if errors:
            raise ValidationError(errors)
