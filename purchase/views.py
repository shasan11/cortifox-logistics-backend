from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Costing, VendorPayment, VendorCreditDebitNote, Expense, NotesItem
from .serializers import CostingSerializer, VendorPaymentSerializer, VendorCreditDebitNoteSerializer, ExpenseSerializer, NotesItemSerializer
from .filters import CostingFilter, VendorPaymentFilter, VendorCreditDebitNoteFilter, ExpenseFilter, NotesItemFilter
from rest_framework_bulk.generics import BulkModelViewSet

class CostingViewSet(BulkModelViewSet):
    queryset = Costing.objects.all()
    serializer_class = CostingSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CostingFilter
    ordering_fields = ['created', 'updated_date', 'total_amount']

class VendorPaymentViewSet(BulkModelViewSet):
    queryset = VendorPayment.objects.all()
    serializer_class = VendorPaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = VendorPaymentFilter
    ordering_fields = ['payment_date', 'amount']

class VendorCreditDebitNoteViewSet(BulkModelViewSet):
    queryset = VendorCreditDebitNote.objects.all()
    serializer_class = VendorCreditDebitNoteSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = VendorCreditDebitNoteFilter
    ordering_fields = ['created', 'amount']

class ExpenseViewSet(BulkModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ExpenseFilter
    ordering_fields = ['date', 'subtotal', 'grand_total']

class NotesItemViewSet(BulkModelViewSet):
    queryset = NotesItem.objects.all()
    serializer_class = NotesItemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = NotesItemFilter
    ordering_fields = ['amount', 'qty', 'tax_percent']
