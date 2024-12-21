from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, CustomerPaymentsViewSet, CreditNoteViewSet
from rest_framework_bulk.routes import BulkRouter

router = BulkRouter()
router.register(r'invoices', InvoiceViewSet)
router.register(r'customer-payments', CustomerPaymentsViewSet)
router.register(r'credit-notes', CreditNoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
