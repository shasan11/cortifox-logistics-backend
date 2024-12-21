from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShipmentViewSet, ShipmentPartyViewSet, ShipmentPackagesViewSet,
    TransitViewSet, PrePostLegViewSet, RelatedDocumentsViewSet,
    PickupDeliveryViewSet, ShipmentChargesViewSet
)
from rest_framework_bulk.routes import BulkRouter
router = BulkRouter()
router.register(r'shipments', ShipmentViewSet)
router.register(r'shipment-parties', ShipmentPartyViewSet)
router.register(r'shipment-packages', ShipmentPackagesViewSet)
router.register(r'transits', TransitViewSet)
router.register(r'pre-post-legs', PrePostLegViewSet)
router.register(r'documents', RelatedDocumentsViewSet)
router.register(r'pickup-delivery', PickupDeliveryViewSet)
router.register(r'charges', ShipmentChargesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

