from rest_framework import viewsets
from .models import (
    ChartofAccounts, BankAccounts, Currency, PaymentMethod,
    JournalEntry, JournalEntryItems, CashTransfers, ChequeRegister
)
from .serializers import (
    ChartofAccountsSerializer, BankAccountsSerializer, CurrencySerializer, PaymentMethodSerializer,
    JournalEntrySerializer, JournalEntryItemsSerializer, CashTransfersSerializer, ChequeRegisterSerializer
    
)
from rest_framework_bulk.generics import BulkModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

class ChartofAccountsViewSet(BulkModelViewSet):
    queryset = ChartofAccounts.objects.all()
    serializer_class = ChartofAccountsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active','coa_type','user_add','under']
    lookup_field="id"
    
    

class BankAccountsViewSet(BulkModelViewSet):
    queryset = BankAccounts.objects.all()
    serializer_class = BankAccountsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active','acc_type','user_add', "type"]

class CurrencyViewSet(BulkModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active']

class PaymentMethodViewSet(BulkModelViewSet,viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active']

class JournalEntryViewSet(BulkModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active']
    lookup_field='uuid'

class JournalEntryItemsViewSet(BulkModelViewSet):
    queryset = JournalEntryItems.objects.all()
    serializer_class = JournalEntryItemsSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields=['journal_entry']
    
     

class CashTransfersViewSet(BulkModelViewSet):
    queryset = CashTransfers.objects.all()
    serializer_class = CashTransfersSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active']

class ChequeRegisterViewSet(BulkModelViewSet):
    queryset = ChequeRegister.objects.all()
    serializer_class = ChequeRegisterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active','cheque_type']
