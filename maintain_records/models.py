from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class DealersDetails(models.Model):
    dealer_number = models.AutoField(primary_key=True)
    dealer_name = models.CharField(max_length=50)
    dealer_phone_number = models.BigIntegerField(blank=True, null=True)
    dealer_email = models.CharField(max_length=50, blank=True, null=True)
    dealer_address = models.CharField(max_length=100, blank=True, null=True)
    total_transaction = models.FloatField(max_length=20, default=0)

class PurchaseDetails(models.Model):
    invoice_by = models.ForeignKey(User)
    invoice_date_and_time = models.DateTimeField(default=timezone.now())
    invoice_number = models.AutoField(primary_key=True)
    dealer = models.ForeignKey(DealersDetails)
    item_name = models.CharField(max_length=50)
    quantity = models.IntegerField()


class SalesDetails(models.Model):
    invoice_by = models.ForeignKey(User)
    invoice_date_and_time = models.DateTimeField(default=timezone.now())
    invoice_number = models.AutoField(primary_key=True)
    dealer = models.ForeignKey(DealersDetails)
    item_name = models.CharField(max_length=50)
    quantity = models.IntegerField()


class ItemDetails(models.Model):
    item_number = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    default_cost_price = models.FloatField(blank=True, null=True)
    default_selling_price = models.FloatField(blank=True, null=True)
    current_stock = models.IntegerField(blank=True, null=True, default=0)
