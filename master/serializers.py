from rest_framework import serializers
from .models import UnitofMeasurement, UnitofMeasurementLength, Ports, PackageType, Branch, MasterData
from   rest_framework_bulk.serializers import BulkSerializerMixin
from core.AdaptedBulkListSerializer import AdaptedBulkListSerializer

class UnitofMeasurementSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = UnitofMeasurement
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class UnitofMeasurementLengthSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = UnitofMeasurementLength
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class PortsSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = Ports
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class PackageTypeSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class BranchSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class MasterDataSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = MasterData
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer
