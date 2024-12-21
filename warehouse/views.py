# views.py

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Warehouse, ShipmentItems, WarehouseStorage, WarehouseBin, ASN, GoodsRecieptNote,
    GoodsIssueOrder, GoodsDispatchOrder, StockTransfer,WarehouseJobsOrders
)
from .serializers import (
    WarehouseSerializer, ShipmentItemsSerializer, WarehouseStorageSerializer, 
    WarehouseBinSerializer, ASNSerializer, GoodsRecieptNoteSerializer, 
    GoodsIssueOrderSerializer, GoodsDispatchOrderSerializer, StockTransferSerializer,WarehouseJobSerializer
)
from rest_framework_bulk.generics import BulkModelViewSet

from django_filters import rest_framework as filters
from .models import (
    Warehouse, ShipmentItems, WarehouseStorage, WarehouseBin, ASN, GoodsRecieptNote,
    GoodsIssueOrder, GoodsDispatchOrder, StockTransfer
)

class WarehouseFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Warehouse
        fields = ['name', 'type', 'active']


class ShipmentItemsFilter(filters.FilterSet):
    status = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ShipmentItems
        fields = ['status', 'warehouse', 'active']


class WarehouseStorageFilter(filters.FilterSet):
    warehouse = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = WarehouseStorage
        fields = ['warehouse', 'active']


class WarehouseBinFilter(filters.FilterSet):
    warehouse_storage = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = WarehouseBin
        fields = ['warehouse_storage', 'active']


class ASNFilter(filters.FilterSet):
    asn_no = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ASN
        fields = ['asn_no', 'warehouse', 'is_received', 'is_issued', 'is_delivered']


class GoodsRecieptNoteFilter(filters.FilterSet):
    warehouse = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = GoodsRecieptNote
        fields = ['warehouse', 'active']


class GoodsIssueOrderFilter(filters.FilterSet):
    warehouse = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = GoodsIssueOrder
        fields = ['warehouse', 'active']


class GoodsDispatchOrderFilter(filters.FilterSet):
    warehouse = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = GoodsDispatchOrder
        fields = ['warehouse', 'active']


class StockTransferFilter(filters.FilterSet):
    from_warehouse = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = StockTransfer
        fields = ['from_warehouse', 'to_warehouse', 'active']


 
class WarehouseViewSet(BulkModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseFilter


class ShipmentItemsViewSet(BulkModelViewSet):
    queryset = ShipmentItems.objects.all()
    serializer_class = ShipmentItemsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShipmentItemsFilter


class WarehouseStorageViewSet(BulkModelViewSet):
    queryset = WarehouseStorage.objects.all()
    serializer_class = WarehouseStorageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseStorageFilter


class WarehouseBinViewSet(BulkModelViewSet):
    queryset = WarehouseBin.objects.all()
    serializer_class = WarehouseBinSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseBinFilter


class ASNViewSet(BulkModelViewSet):
    queryset = ASN.objects.all()
    serializer_class = ASNSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ASNFilter


class GoodsRecieptNoteViewSet(BulkModelViewSet):
    queryset = GoodsRecieptNote.objects.all()
    serializer_class = GoodsRecieptNoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GoodsRecieptNoteFilter


class GoodsIssueOrderViewSet(BulkModelViewSet):
    queryset = GoodsIssueOrder.objects.all()
    serializer_class = GoodsIssueOrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GoodsIssueOrderFilter


class GoodsDispatchOrderViewSet(BulkModelViewSet):
    queryset = GoodsDispatchOrder.objects.all()
    serializer_class = GoodsDispatchOrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GoodsDispatchOrderFilter


class StockTransferViewSet(BulkModelViewSet):
    queryset = StockTransfer.objects.all()
    serializer_class = StockTransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StockTransferFilter


class WarehouseJobOrderViewSet(BulkModelViewSet):
    queryset=WarehouseJobsOrders.objects.all()
    serializer_class=WarehouseJobSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_fields = ['shipment','from_warehouse','to_warehouse','port_origin','port_destination','from _warehouse_bin','to_warehouse_bin','port_handling_agent_origin','port_handling_agent_destination']

