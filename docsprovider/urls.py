from django.urls import path
from docsprovider.shipment_docs.views import ShipmentDetailView

urlpatterns = [
    path('shipments/<int:pk>/', ShipmentDetailView.as_view(), name='shipment-detail'),
]
