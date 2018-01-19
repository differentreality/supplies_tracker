from __future__ import unicode_literals
from hamlpy.views.generic import HamlExtensionTemplateView
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

class User(User):
    def name(self):
        return self.first_name + self.last_name
    class Meta:
      proxy = True

class Item(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True,blank=True)
    price_bought = models.FloatField(default=0, verbose_name="How much does this cost to buy?")
    reimbursement = models.FloatField(default=0, null=True, verbose_name="How much do you make? (Fill if you sell the items, or provide them against donation)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    storages = models.ManyToManyField('Storage', through='Items_Storage', related_name='Storage')
    image = ImageField(upload_to='whatever',null= True,blank = True)

class Space(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    image = ImageField(upload_to='whatever',null=True, blank=True)

    def class_name(self):
      return self.__class__.__name__

class Storage(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, null=False)
    item = models.ManyToManyField(Item, through='Items_Storage', related_name='Item')
    image = ImageField(upload_to='whatever',null= True,blank=True)

    def class_name(self):
      return self.__class__.__name__

class Items_Storage(models.Model) :
    items = models.ForeignKey(Item)
    storage = models.ForeignKey(Storage)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=True,blank=False)
    price_bought = models.FloatField
    price_donated = models.FloatField

    class Meta:
        unique_together = (('storage', 'items'),)
