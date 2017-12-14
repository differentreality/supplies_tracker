from django.db import models
from django.utils import timezone

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    # price_bought = models.FloatField()
    # reimbursement = models.FloatField()
    created_date = models.DateTimeField(default=timezone.now)
