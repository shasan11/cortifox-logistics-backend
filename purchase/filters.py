import django_filters
from .models import Costing, VendorPayment, VendorCreditDebitNote, Expense, NotesItem

class CostingFilter(django_filters.FilterSet):
    class Meta:
        model = Costing
        fields = {
            'costing_number': ['exact', 'icontains'],
            'currency': ['exact'],
            'vendor': ['exact'],
            'total_amount': ['lt', 'lte', 'gt', 'gte'],
            'created': ['exact', 'year__exact', 'month__exact', 'day__exact'],
            'updated_date': ['exact', 'year__exact', 'month__exact', 'day__exact'],
        }

class VendorPaymentFilter(django_filters.FilterSet):
    class Meta:
        model = VendorPayment
        fields = {
            'vendor': ['exact'],
            'currency': ['exact'],
            'payment_status': ['exact'],
            'payment_date': ['exact', 'year__exact', 'month__exact', 'day__exact'],
            'amount': ['lt', 'lte', 'gt', 'gte'],
        }

class VendorCreditDebitNoteFilter(django_filters.FilterSet):
    class Meta:
        model = VendorCreditDebitNote
        fields = {
            'vendor': ['exact'],
            'note_number': ['exact', 'icontains'],
            'currency': ['exact'],
            'amount': ['lt', 'lte', 'gt', 'gte'],
            'created': ['exact', 'year__exact', 'month__exact', 'day__exact'],
        }

class ExpenseFilter(django_filters.FilterSet):
    class Meta:
        model = Expense
        fields = {
            'bill_no': ['exact', 'icontains'],
            'currency': ['exact'],
            'date': ['exact', 'year__exact', 'month__exact', 'day__exact'],
            'type': ['exact'],
            'subtotal': ['lt', 'lte', 'gt', 'gte'],
            'grand_total': ['lt', 'lte', 'gt', 'gte'],
        }

class NotesItemFilter(django_filters.FilterSet):
    class Meta:
        model = NotesItem
        fields = {
            'product': ['exact', 'icontains'],
            'amount': ['lt', 'lte', 'gt', 'gte'],
            'qty': ['lt', 'lte', 'gt', 'gte'],
            'discount': ['lt', 'lte', 'gt', 'gte'],
            'tax_percent': ['lt', 'lte', 'gt', 'gte'],
        }
