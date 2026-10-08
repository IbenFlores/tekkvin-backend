from django.db import models

class Supplier(models.Model):
    company_name = models.TextField(null=True, blank=True)
    tax_id = models.TextField(unique=True, null=True, blank=True)
    contact_email = models.TextField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_id = models.IntegerField(null=True, blank=True)
    modified_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'suppliers'

    def __str__(self):
        return str(self.company_name)