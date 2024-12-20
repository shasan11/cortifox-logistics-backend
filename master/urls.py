from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UnitofMeasurementViewSet, UnitofMeasurementLengthViewSet, PortsViewSet, 
    PackageTypeViewSet, BranchViewSet, MasterDataViewSet
)
from rest_framework_bulk.routes import BulkRouter
router = BulkRouter()
router.register(r'unit-of-measurement', UnitofMeasurementViewSet, basename='unitofmeasurement')
router.register(r'unit-of-measurement-length', UnitofMeasurementLengthViewSet, basename='unitofmeasurementlength')
router.register(r'ports', PortsViewSet, basename='ports')
router.register(r'package-type', PackageTypeViewSet, basename='packagetype')
router.register(r'branch', BranchViewSet, basename='branch')
router.register(r'master-data', MasterDataViewSet, basename='masterdata')

urlpatterns = [
    path('', include(router.urls)),
]
