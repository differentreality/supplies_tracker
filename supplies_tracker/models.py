from hamlpy.views.generic import HamlExtensionTemplateView
from django.db import models
from django.utils import timezone

class Item(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField()
    price_bought = models.FloatField(default=0)
    reimbursement = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Space(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField
    address = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Storage(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    capacity = models.FloatField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    space_id = models.ForeignKey(Space, on_delete=models.CASCADE)
