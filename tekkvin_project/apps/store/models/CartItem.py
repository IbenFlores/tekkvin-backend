from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from .Cart import Cart
from .Product import Product

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)],)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_id = models.IntegerField(null=True, blank=True)
    modified_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "cart_items"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name="cart_item_quantity_positive",
            ),
        ]

    def clean(self):
        super().clean()

        if self.quantity is not None and self.quantity <= 0:
            raise ValidationError({
                "quantity": "La cantidad debe ser mayor que cero."
            })
