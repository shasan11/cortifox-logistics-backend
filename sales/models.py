from django.db import models
import uuid
from accounting.models import Currency
from clients.models import Client as Clients
import datetime
from core.getCurrentUser import get_current_user
from accounting.models import ChartofAccounts, BankAccounts, PaymentMethod
from shipments.models import Shipment
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User

invoice_status = [
    ("draft", "Draft"),
    ("pending", "Pending"),
    ("sent", "Sent"),
    ("due", "Due"),
    ("overdue", "Overdue"),
    ("partially_paid", "Partially Paid"),
    ("paid", "Paid"),
    ("processing", "Processing"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("cancelled", "Cancelled"),
]

payment_status = [
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("authorized", "Authorized"),
    ("captured", "Captured"),
    ("partially_paid", "Partially Paid"),
    ("paid", "Paid"),
    ("failed", "Failed"),
    ("refunded", "Refunded"),
    ("cancelled", "Cancelled"),
]

class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    invoice_number = models.CharField(max_length=50)
    shipment_job = models.ManyToManyField(Shipment, blank=True,)
    status = models.CharField(max_length=20, choices=invoice_status)
    client = models.ForeignKey(Clients, on_delete=models.PROTECT, related_name='invoices')
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='invoices')
    discount_amount = models.DecimalField(max_digits=50, decimal_places=10)
    total_amount = models.DecimalField(max_digits=50, decimal_places=10)
    paid_amount = models.DecimalField(max_digits=50, decimal_places=10)
    payment_status = models.CharField(max_length=20, choices=payment_status)
    created_date_editable = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    user=models.ForeignKey(User,on_delete=models.PROTECT,related_name='invoice_user',blank=True,null=True)

    history = HistoricalRecords() 

class CustomerPayments(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='customer_payments')
    bank_accounts = models.ForeignKey(BankAccounts, on_delete=models.CASCADE, blank=True, null=True, related_name='customer_payments')
    payment_mode = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, related_name='customer_payments')
    amount = models.DecimalField(max_digits=50, decimal_places=10)
    payment_status = models.CharField(max_length=20, choices=payment_status)
    payment_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    user=models.ForeignKey(User,on_delete=models.PROTECT,related_name='customer_payment_user',blank=True,null=True)

    class Meta:
        ordering = ['-payment_date']

class CreditNote(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='credit_notes')
    client = models.ForeignKey(Clients, on_delete=models.PROTECT, related_name='credit_notes')
    credit_note_number = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=50, decimal_places=10)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='credit_notes')
    reason = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    user=models.ForeignKey(User,on_delete=models.PROTECT,related_name='credit_user',blank=True,null=True) 

    class Meta:
        ordering = ['-created']
