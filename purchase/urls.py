from rest_framework.routers import DefaultRouter
from .views import CostingViewSet, VendorPaymentViewSet, VendorCreditDebitNoteViewSet, ExpenseViewSet, NotesItemViewSet
from rest_framework_bulk.routes import BulkRouter
router = BulkRouter()
router.register(r'costings', CostingViewSet)
router.register(r'vendor-payments', VendorPaymentViewSet)
router.register(r'vendor-credit-debit-notes', VendorCreditDebitNoteViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'notes-items', NotesItemViewSet)

urlpatterns = router.urls
