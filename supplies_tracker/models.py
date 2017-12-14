from django.db import models
from django.utils import timezone

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_bought = models.FloatField(default=0)
    reimbursement = models.FloatField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
