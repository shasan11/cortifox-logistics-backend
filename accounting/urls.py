from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    ChartofAccountsViewSet, BankAccountsViewSet, CurrencyViewSet, PaymentMethodViewSet,
    JournalEntryViewSet, JournalEntryItemsViewSet, CashTransfersViewSet, ChequeRegisterViewSet
)
from rest_framework_bulk.routes import BulkRouter

router = BulkRouter()
router.register(r'chartofaccounts', ChartofAccountsViewSet)
router.register(r'bankaccounts', BankAccountsViewSet)
router.register(r'currency', CurrencyViewSet)
router.register(r'paymentmethods', PaymentMethodViewSet)
router.register(r'journalentries', JournalEntryViewSet)
router.register(r'journalentryitems', JournalEntryItemsViewSet)
router.register(r'cashtransfers', CashTransfersViewSet)
router.register(r'chequeregister', ChequeRegisterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
