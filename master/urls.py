from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UnitofMeasurementViewSet, UnitofMeasurementLengthViewSet, PortsViewSet, 
    PackageTypeViewSet, BranchViewSet, MasterDataViewSet,ApplicationSettingsViewSet,ShipmentPrefixesViewSet
)
from rest_framework_bulk.routes import BulkRouter
router = BulkRouter()
router.register(r'unit-of-measurement', UnitofMeasurementViewSet)
router.register(r'unit-of-measurement-length', UnitofMeasurementLengthViewSet)
router.register(r'ports', PortsViewSet)
router.register(r'package-type', PackageTypeViewSet)
router.register(r'branch', BranchViewSet)
router.register(r'master-data', MasterDataViewSet)
router.register(r'application-settings', ApplicationSettingsViewSet)
router.register(r'shipment-prefixes', ShipmentPrefixesViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
