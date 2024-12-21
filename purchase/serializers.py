from rest_framework import serializers
from .models import Costing, VendorPayment, VendorCreditDebitNote, Expense, NotesItem
from rest_framework_bulk.serializers import BulkSerializerMixin
from core.AdaptedBulkListSerializer import AdaptedBulkListSerializer

class CostingSerializer(serializers.ModelSerializer,BulkSerializerMixin):
    class Meta:
        model = Costing
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class VendorPaymentSerializer(serializers.ModelSerializer,BulkSerializerMixin):
    class Meta:
        model = VendorPayment
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer


class VendorCreditDebitNoteSerializer(serializers.ModelSerializer,BulkSerializerMixin):
    class Meta:
        model = VendorCreditDebitNote
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class ExpenseSerializer(serializers.ModelSerializer,BulkSerializerMixin):
    class Meta:
        model = Expense
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class NotesItemSerializer(serializers.ModelSerializer,BulkSerializerMixin):
    class Meta:
        model = NotesItem
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer
