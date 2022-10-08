# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

# Create your models here.

class ExpenseTracker(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.FloatField(null=False)
    category = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    paymentType = models.CharField(max_length=500)
    create_date = models.DateTimeField()

    class Meta:
        db_table='ExpenseTracker'