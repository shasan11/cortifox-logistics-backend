from rest_framework import serializers
from .models import Invoice, CustomerPayments, CreditNote
from rest_framework_bulk.serializers import BulkSerializerMixin
from core.AdaptedBulkListSerializer import AdaptedBulkListSerializer

class InvoiceSerializer(serializers.ModelSerializer,BulkSerializerMixin):
    class Meta:
        model = Invoice
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class CustomerPaymentsSerializer(serializers.ModelSerializer,BulkSerializerMixin):
    class Meta:
        model = CustomerPayments
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class CreditNoteSerializer(serializers.ModelSerializer,BulkSerializerMixin):
    class Meta:
        model = CreditNote
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer
