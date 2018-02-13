from __future__ import unicode_literals
from hamlpy.views.generic import HamlExtensionTemplateView
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField


##
# For the users of the application
class User(User):
    def name(self):
        return self.first_name + self.last_name

    class Meta:
        proxy = True


##
# For the items used
class Item(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    price_bought = models.FloatField(default=0, verbose_name="How much does this cost to buy?")
    reimbursement = models.FloatField(
        default=0, null=True,
        verbose_name="How much do you make? (Fill if you sell the items, or provide them against donation)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    storages = models.ManyToManyField('Storage', through='Items_Storage', related_name='Storage')
    image = ImageField(upload_to='whatever', null=True, blank=True)


##
# For the spaces created
class Space(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    image = ImageField(upload_to='whatever', null=True, blank=True)

    ##
    # Returns the class of the object
    # ==== Returns
    # * +String+ -> 'Space'
    def class_name(self):
        return self.__class__.__name__


##
# For the storages of the spaces
class Storage(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, null=False)
    item = models.ManyToManyField(Item, through='Items_Storage', related_name='Item')
    image = ImageField(upload_to='whatever', null=True, blank=True)

    ##
    # Returns the class of the object
    # ==== Returns
    # * +String+ -> 'Storage'
    def class_name(self):
        return self.__class__.__name__


##
# The join model for the many-to-many relationship
# between Item and Storage
# It also has additional attributes
class Items_Storage(models.Model):
    item = models.ForeignKey(Item)
    storage = models.ForeignKey(Storage)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)

    class Meta:
        unique_together = ('storage', 'item')
