from django.conf import settings
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='customer',
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_id = models.IntegerField(default=1)
    modified_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'