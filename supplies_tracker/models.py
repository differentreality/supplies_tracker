from __future__ import unicode_literals
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
    items = models.ManyToManyField('Storage',through='Items_Storage',related_name='item')


class Space(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True)
    address = models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Storage(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    space_id = models.ForeignKey(Space, on_delete=models.CASCADE,null=True)

class Items_Storage(models.Model) :
    item = models.ForeignKey(Item,related_name= 'content')
    storage = models.ForeignKey(Storage, related_name='content')
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=False,blank=False)
    price_bought = models.FloatField
    price_donated = models.FloatField

