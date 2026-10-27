from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    support_url = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_id = models.IntegerField()
    modified_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'brands'

    def __str__(self):
        return str(self.name)