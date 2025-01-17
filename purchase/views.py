from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    ExpenseCategorySerializer,
    ExpensesSerializer,
    ExpensesItemsSerializer,
    VendorBillsSerializer,
    VendorBillItemsSerializer,
    VendorPaymentsSerializer,
    VendorPaymentEntriesSerializer,
)
from .models import ExpenseCategory, Expenses, ExpensesItems, VendorBills, VendorBillItems, VendorPayments, VendorPaymentEntries
from rest_framework_bulk.generics import BulkModelViewSet


class ExpenseCategoryViewSet(BulkModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'parent']
    search_fields = ['name']
    ordering_fields = ['id', 'name']


class ExpensesViewSet(BulkModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['invoice_reference', 'supplier', 'date', 'currency']
    search_fields = ['invoice_reference']
    ordering_fields = ['date', 'due_date', 'total_amount']


class ExpensesItemsViewSet(BulkModelViewSet):
    queryset = ExpensesItems.objects.all()
    serializer_class = ExpensesItemsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['expensesitems', 'vat_choices']
    ordering_fields = ['amount']


class VendorBillsViewSet(BulkModelViewSet):
    queryset = VendorBills.objects.all()
    serializer_class = VendorBillsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vendor', 'date', 'due_date', 'bill_status']
    search_fields = ['invoice_reference']
    ordering_fields = ['date', 'due_date', 'total_amount']


class VendorBillItemsViewSet(BulkModelViewSet):
    queryset = VendorBillItems.objects.all()
    serializer_class = VendorBillItemsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vendorbills', 'vat_choices']
    ordering_fields = ['rate', 'qty', 'total']


class VendorPaymentsViewSet(BulkModelViewSet):
    queryset = VendorPayments.objects.all()
    serializer_class = VendorPaymentsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['paid_from', 'paid_to', 'date', 'bill_status']
    search_fields = ['remarks']
    ordering_fields = ['date', 'amount']


class VendorPaymentEntriesViewSet(BulkModelViewSet):
    queryset = VendorPaymentEntries.objects.all()
    serializer_class = VendorPaymentEntriesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vendor_payments', 'vendor_bills']
    ordering_fields = ['amount']
