from rest_framework import viewsets
from rest_framework_bulk.generics import BulkModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import UnitofMeasurement, UnitofMeasurementLength, Ports, PackageType, Branch, MasterData
from .serializers import (
    UnitofMeasurementSerializer, UnitofMeasurementLengthSerializer, PortsSerializer, 
    PackageTypeSerializer, BranchSerializer, MasterDataSerializer
)
from .filters import (
    UnitofMeasurementFilter, UnitofMeasurementLengthFilter, PortsFilter, 
    PackageTypeFilter, BranchFilter, MasterDataFilter
)

class UnitofMeasurementViewSet(BulkModelViewSet):
    queryset = UnitofMeasurement.objects.all()
    serializer_class = UnitofMeasurementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UnitofMeasurementFilter

class UnitofMeasurementLengthViewSet(BulkModelViewSet):
    queryset = UnitofMeasurementLength.objects.all()
    serializer_class = UnitofMeasurementLengthSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UnitofMeasurementLengthFilter

class PortsViewSet(BulkModelViewSet):
    queryset = Ports.objects.all()
    serializer_class = PortsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PortsFilter

class PackageTypeViewSet(BulkModelViewSet):
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PackageTypeFilter

class BranchViewSet(BulkModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BranchFilter

class MasterDataViewSet(BulkModelViewSet):
    queryset = MasterData.objects.all()
    serializer_class = MasterDataSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MasterDataFilter
