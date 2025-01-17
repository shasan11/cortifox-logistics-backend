from rest_framework.routers import DefaultRouter
from .views import (
    ExpenseCategoryViewSet,
    ExpensesViewSet,
    ExpensesItemsViewSet,
    VendorBillsViewSet,
    VendorBillItemsViewSet,
    VendorPaymentsViewSet,
    VendorPaymentEntriesViewSet,
)
from rest_framework_bulk.routes import BulkRouter
# Create a router and register our viewsets
router = BulkRouter()
router.register(r'expense-categories', ExpenseCategoryViewSet, basename='expensecategory')
router.register(r'expenses', ExpensesViewSet, basename='expenses')
router.register(r'expense-items', ExpensesItemsViewSet, basename='expenseitems')
router.register(r'vendor-bills', VendorBillsViewSet, basename='vendorbills')
router.register(r'vendor-bill-items', VendorBillItemsViewSet, basename='vendorbillitems')
router.register(r'vendor-payments', VendorPaymentsViewSet, basename='vendorpayments')
router.register(r'vendor-payment-entries', VendorPaymentEntriesViewSet, basename='vendorpaymententries')

# URL patterns
urlpatterns = router.urls
