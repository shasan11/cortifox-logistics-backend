from rest_framework_bulk.generics import BulkModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    UnitofMeasurement, UnitofMeasurementLength, Ports, 
    PackageType, Branch, MasterData,ApplicationSettings,ShipmentPrefixes
)
from .serializers import (
    UnitofMeasurementSerializer, UnitofMeasurementLengthSerializer, PortsSerializer, 
    PackageTypeSerializer, BranchSerializer, MasterDataSerializer,ApplicationSettingsSerializer,ShipmentPrefixesSerializer
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
    permission_classes = [IsAuthenticated]

class UnitofMeasurementLengthViewSet(BulkModelViewSet):
    queryset = UnitofMeasurementLength.objects.all()
    serializer_class = UnitofMeasurementLengthSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UnitofMeasurementLengthFilter
    permission_classes = [IsAuthenticated]

class PortsViewSet(BulkModelViewSet):
    queryset = Ports.objects.all()
    serializer_class = PortsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PortsFilter
    permission_classes = [IsAuthenticated]

class PackageTypeViewSet(BulkModelViewSet):
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PackageTypeFilter
    permission_classes = [IsAuthenticated]

class BranchViewSet(BulkModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BranchFilter
    permission_classes = [IsAuthenticated]

class MasterDataViewSet(BulkModelViewSet):
    queryset = MasterData.objects.all()
    serializer_class = MasterDataSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MasterDataFilter
    permission_classes = [IsAuthenticated]

class ApplicationSettingsViewSet(BulkModelViewSet):
    queryset = ApplicationSettings.objects.all()
    serializer_class = ApplicationSettingsSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

class ShipmentPrefixesViewSet(BulkModelViewSet):
    queryset = ShipmentPrefixes.objects.all()
    serializer_class = ShipmentPrefixesSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
