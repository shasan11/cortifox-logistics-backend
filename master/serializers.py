from rest_framework import serializers, viewsets, routers
from rest_framework.permissions import IsAuthenticated
from django.urls import path, include
from .models import (
    UnitofMeasurement, UnitofMeasurementLength, Ports, PackageType, Branch, MasterData, ApplicationSettings, ShipmentPrefixes
)
from core.AdaptedBulkListSerializer import AdaptedBulkListSerializer
from rest_framework_bulk.serializers import BulkSerializerMixin


# Serializers
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



class ApplicationSettingsSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = ApplicationSettings
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer



class ShipmentPrefixesSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = ShipmentPrefixes
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer
