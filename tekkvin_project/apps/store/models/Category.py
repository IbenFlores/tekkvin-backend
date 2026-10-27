from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_id = models.IntegerField()
    modified_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return str(self.name)