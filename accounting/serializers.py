from rest_framework import serializers
from .models import (
    ChartofAccounts, BankAccounts, Currency, PaymentMethod,
    JournalEntry, JournalEntryItems, CashTransfers, ChequeRegister
)
from rest_framework_bulk.serializers import BulkSerializerMixin,BulkListSerializer
from core.AdaptedBulkListSerializer import AdaptedBulkListSerializer

class ChartofAccountsSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = ChartofAccounts
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer
        read_only_fields = ['id']
        depth=1
        
class BankAccountsSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class CurrencySerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class PaymentMethodSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class JournalEntrySerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class JournalEntryItemsSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = JournalEntryItems
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer
         

class CashTransfersSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = CashTransfers
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class ChequeRegisterSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = ChequeRegister
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer
