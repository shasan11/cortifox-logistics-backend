from rest_framework import serializers
from rest_framework_bulk.serializers import BulkSerializerMixin
from .models import UnitofMeasurement, ProductCategory, Product, SecondaryUnit, InventoryAdjustment,BOMCosting,BillofMaterialRawMateials,BillofMaterials,BillofMaterialOutput
from core.AdaptedBulkListSerializer import AdaptedBulkListSerializer

class UnitofMeasurementSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = UnitofMeasurement
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class ProductCategorySerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class ProductSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class SecondaryUnitSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = SecondaryUnit
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class InventoryAdjustmentSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = InventoryAdjustment
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class BillofMaterialsSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = BillofMaterials
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class BillofMaterialRawMaterialsSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = BillofMaterialRawMateials
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class BillofMaterialOutputSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = BillofMaterialOutput
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class BOMCostingSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = BOMCosting
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer