from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Invoice, CustomerPayments, CreditNote
from .serializers import InvoiceSerializer, CustomerPaymentsSerializer, CreditNoteSerializer
from rest_framework_bulk.generics import BulkModelViewSet

class InvoiceViewSet(BulkModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'client', 'currency', 'created_date_editable']
    ordering_fields = ['created', 'updated_date', 'total_amount', 'paid_amount']

class CustomerPaymentsViewSet(BulkModelViewSet):
    queryset = CustomerPayments.objects.all()
    serializer_class = CustomerPaymentsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['invoice', 'payment_mode', 'payment_status', 'payment_date']
    ordering_fields = ['payment_date', 'amount', 'created', 'updated']

class CreditNoteViewSet(BulkModelViewSet):
    queryset = CreditNote.objects.all()
    serializer_class = CreditNoteSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['invoice', 'client', 'currency', 'created']
    ordering_fields = ['created', 'updated', 'amount']
