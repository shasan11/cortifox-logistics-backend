from rest_framework import serializers
from .models import Warehouse, ShipmentItems, WarehouseStorage, WarehouseBin, ASN, GoodsRecieptNote, GoodsIssueOrder, GoodsDispatchOrder, StockTransfer,WarehouseJobsOrders
from  rest_framework_bulk.serializers import BulkSerializerMixin
from core.AdaptedBulkListSerializer import AdaptedBulkListSerializer

class WarehouseSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class ShipmentItemsSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = ShipmentItems
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class WarehouseStorageSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = WarehouseStorage
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class WarehouseBinSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = WarehouseBin
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class ASNSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = ASN
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class GoodsRecieptNoteSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = GoodsRecieptNote
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class GoodsIssueOrderSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = GoodsIssueOrder
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class GoodsDispatchOrderSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = GoodsDispatchOrder
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class StockTransferSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = StockTransfer
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class WarehouseJobSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = WarehouseJobsOrders
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer
