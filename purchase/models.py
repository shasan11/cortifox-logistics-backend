from django.db import models
from shipments.models import Shipment
from accounting.models import Currency
from actor.models import Vendor
import uuid
from accounting.models import BankAccounts, ChartofAccounts, PaymentMethod
from django.contrib.auth.models import User
from core.getCurrentUser import get_current_user

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

class Costing(models.Model):
    id = models.BigAutoField(primary_key=True)
    costing_number = models.CharField(max_length=50)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='costings')
    shipment_job = models.ManyToManyField(Shipment, blank=True, related_name='costings')
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name='costings')
    total_amount = models.DecimalField(max_digits=50, decimal_places=10)
    paid_amount = models.DecimalField(max_digits=50, decimal_places=10)
    payment_status = models.CharField(max_length=20, choices=payment_status)
    costing_status = models.CharField(max_length=20, choices=invoice_status)
    created_date_editable = models.DateField()
    remarks=models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    user_add=models.ForeignKey(User,on_delete=models.PROTECT,editable=False,null=True,default=get_current_user)
    active=models.BooleanField(default=True)
    user=models.ForeignKey(User,on_delete=models.PROTECT,related_name='shipment_costing_user',blank=True,null=True)


class VendorPayment(models.Model):
    id = models.BigAutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name='vendor_payments')
    bank_accounts = models.ForeignKey(BankAccounts, on_delete=models.CASCADE, blank=True, null=True, related_name='vendor_payments')
    shipment_job = models.ManyToManyField(Costing, blank=True,  related_name='vendor_payments')
    amount = models.DecimalField(max_digits=50, decimal_places=10)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='vendor_payments')
    payment_status = models.CharField(max_length=20, choices=payment_status)
    payment_date = models.DateField()
    remarks=models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    user_add=models.ForeignKey(User,on_delete=models.PROTECT,editable=False,null=True,default=get_current_user)
    active=models.BooleanField(default=True)
    


    def __str__(self):
        return f"{self.vendor} - {self.amount} {self.currency}"

    class Meta:
        ordering = ['-payment_date']

class VendorCreditDebitNote(models.Model):
    id = models.BigAutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name='vendor_credit_debit_notes')
    note_number = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=50, decimal_places=10)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='vendor_credit_debit_notes')
    reason = models.TextField()
    remarks=models.TextField(blank=True,null=True)
    is_credit_note = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    user_add=models.ForeignKey(User,on_delete=models.PROTECT,editable=False,null=True,default=get_current_user)
    active=models.BooleanField(default=True)


    def __str__(self):
        return f"{self.note_number} - {self.amount} {self.currency}"

    class Meta:
        ordering = ['-created']

class Expense(models.Model):
    id = models.BigAutoField(primary_key=True)
    bill_no = models.CharField(max_length=50, unique=True)
    expense_cat=models.CharField(max_length=120)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='expenses')
    exchange_rate_to_npr = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    date = models.DateField()
    type = models.CharField(max_length=20, choices=[('debit', 'Debit'), ('credit', 'Credit'), ('purchase', 'Purchase'), ("e", "Expense")])
    chart_of_accounts = models.ForeignKey(ChartofAccounts, on_delete=models.CASCADE, blank=True, null=True, related_name='expenses')
    bank_accounts = models.ForeignKey(BankAccounts, on_delete=models.CASCADE, blank=True, null=True, related_name='expenses')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False)
    non_taxable_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False)
    taxable_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False)
    vat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False)
    created=models.DateTimeField(auto_now_add=True)
    remarks=models.TextField(blank=True,null=True)
    updated=models.DateTimeField(auto_now=True)
    user_add=models.ForeignKey(User,on_delete=models.PROTECT,editable=False,null=True,default=get_current_user)
    active=models.BooleanField(default=True)


class NotesItem(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False, default=uuid.uuid4)
    notes = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='items')
    product = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_type = models.CharField(max_length=20, choices=[('amount', 'Amount'), ('percent', 'Percent')])
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    remarks=models.TextField(blank=True,null=True)
    user_add=models.ForeignKey(User,on_delete=models.PROTECT,editable=False,null=True,default=get_current_user)
    active=models.BooleanField(default=True)


