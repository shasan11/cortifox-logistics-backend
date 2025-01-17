from shipments.models import Shipment
from accounting.models import Currency
from actor.models import Vendor
from crm.models import Contacts
import uuid
from accounting.models import BankAccounts, ChartofAccounts, PaymentMethod
from django.contrib.auth.models import User
from core.getCurrentUser import get_current_user
from simple_history.models import HistoricalRecords
from decimal import Decimal
from django.db import models
bill_status = [
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

VAT_CHOICES = (
    ("13", "13% VAT"),
    ("zero", "0% VAT"),
    ("no_vat", "No VAT")
)

class ExpenseCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="subcategories")

class Expenses(models.Model):
    id = models.BigAutoField(primary_key=True)
    invoice_reference = models.CharField(max_length=100)
    supplier = models.ForeignKey(Contacts, on_delete=models.CASCADE, related_name="supplier_party")
    date = models.DateField()
    due_date = models.DateField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="expenses_category")
    exchange_rate_to_npr = models.DecimalField(decimal_places=2, max_digits=15)
    subtotal_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    non_taxable_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    taxable_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    vat_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    paid_from = models.ForeignKey(BankAccounts, on_delete=models.PROTECT, related_name="expenses_paid_from")
    created = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='expenses_user', blank=True, null=True)

    history = HistoricalRecords()

class ExpensesItems(models.Model):
    id = models.BigAutoField(primary_key=True)
    expensesitems = models.ForeignKey(Expenses, on_delete=models.CASCADE, related_name="expenseitem")
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    vat_choices = models.CharField(max_length=100, choices=VAT_CHOICES)

    def update_expense_totals(self):
        expense = self.expensesitems
        items = expense.expenseitem.all()
        subtotal = sum(item.amount for item in items)
        non_taxable = sum(item.amount for item in items if item.vat_choices == "no_vat")
        taxable = sum(item.amount for item in items if item.vat_choices in ["13", "zero"])
        vat_amount = sum((item.amount * Decimal(0.13)) for item in items if item.vat_choices == "13")
        discount = expense.discount_amount
        total = subtotal - discount + vat_amount

        expense.subtotal_amount = subtotal
        expense.non_taxable_amount = non_taxable
        expense.taxable_amount = taxable
        expense.vat_amount = vat_amount
        expense.total_amount = total
        expense.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_expense_totals()

    def delete(self, *args, **kwargs):
        expense = self.expensesitems
        super().delete(*args, **kwargs)
        items = expense.expenseitem.all()
        if items.exists():
            self.update_expense_totals()
        else:
            expense.subtotal_amount = 0
            expense.non_taxable_amount = 0
            expense.taxable_amount = 0
            expense.vat_amount = 0
            expense.total_amount = 0
            expense.save()

class VendorBills(models.Model):
    id = models.BigAutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name="vendorbills")
    invoice_reference = models.CharField(max_length=100)
    date = models.DateField()
    due_date = models.DateField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="vendorbills_currency")
    exchange_rate_to_npr = models.DecimalField(decimal_places=2, max_digits=15)
    subtotal_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    non_taxable_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    taxable_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    vat_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    bill_status = models.CharField(choices=bill_status, default="due",max_length=20)
    remarks = models.TextField(blank=True, null=True)


    created = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='vendor_bills_user', blank=True, null=True)

    history = HistoricalRecords()

class VendorBillItems(models.Model):
    vendorbills = models.ForeignKey(VendorBills, on_delete=models.CASCADE, related_name="vendorbillitems")
    description = models.TextField(blank=True, null=True)
    rate = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    qty = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    taxes = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    discount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    vat_choices = models.CharField(max_length=100, choices=VAT_CHOICES)
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)

class VendorPayments(models.Model):
    id = models.BigAutoField(primary_key=True)
    paid_from = models.ForeignKey(BankAccounts, on_delete=models.PROTECT, related_name="payment_paid_from")
    paid_to = models.ForeignKey(BankAccounts, on_delete=models.PROTECT, related_name="payment_paid_to")
    date = models.DateField()
    remarks = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="vendorpayments_currency")
    exchange_rate_to_npr = models.DecimalField(decimal_places=2, max_digits=15)
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    bank_charges = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    tds_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    tds_type = models.CharField(max_length=100)
    tds_coa = models.ForeignKey(ChartofAccounts, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='vendorpayment_user', blank=True, null=True)
    bill_status = models.CharField(choices=bill_status, default="due",max_length=20)
    history = HistoricalRecords()

class VendorPaymentEntries(models.Model):
    id = models.BigAutoField(primary_key=True)
    vendor_payments = models.ForeignKey(VendorPayments, on_delete=models.CASCADE, related_name="vendor_paymententries")
    vendor_bills = models.ForeignKey(VendorBills, on_delete=models.PROTECT, related_name="vendor_payment_entries")
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def update_vendor_bill_status(self):
        vendor_bill = self.vendor_bills
        vendor_bill.paid_amount = sum(entry.amount for entry in vendor_bill.vendor_payment_entries.all())
        vendor_bill.remaining_amount = vendor_bill.total_amount - vendor_bill.paid_amount

        if vendor_bill.remaining_amount <= 0:
            vendor_bill.bill_status = "paid"
        elif vendor_bill.paid_amount > 0:
            vendor_bill.bill_status = "partially_paid"
        else:
            vendor_bill.bill_status = "due"

        vendor_bill.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_vendor_bill_status()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_vendor_bill_status()
