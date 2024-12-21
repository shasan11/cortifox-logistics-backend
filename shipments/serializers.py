from rest_framework import serializers
from .models import (
    Shipment, ShipmentParty, ShipmentPackages, Transit, 
    PrePostLeg, RelatedDocuments, PickupDelivery, ShipmentCharges,Driver,Fleet
)
from django.contrib.auth.models import User
from master.models import (
    Ports, PackageType, UnitofMeasurement, UnitofMeasurementLength, Branch
)
from accounting.models import Currency
from actor.models import Vendor
from clients.models import Client, RelatedConsignee
from   rest_framework_bulk.serializers import BulkSerializerMixin
from core.AdaptedBulkListSerializer import AdaptedBulkListSerializer



class UserMinimalSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        list_serializer_class = AdaptedBulkListSerializer

class PortSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = Ports
        fields = ['id', 'name']
        list_serializer_class = AdaptedBulkListSerializer

class ClientSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name']
        list_serializer_class = AdaptedBulkListSerializer

class VendorSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name']
        list_serializer_class = AdaptedBulkListSerializer

class RelatedConsigneeSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = RelatedConsignee
        fields = ['id', 'name']
        list_serializer_class = AdaptedBulkListSerializer

class ShipmentPackagesSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    package_type_display = serializers.CharField(source='package_type.name', read_only=True)
    package_unit_display = serializers.CharField(source='package_unit.name', read_only=True)
    mass_unit_display = serializers.CharField(source='mass_unit.name', read_only=True)
    user_add_package = UserMinimalSerializer(read_only=True)

    class Meta:
        model = ShipmentPackages
        fields = '__all__'
        read_only_fields = ['user_add_package']
        list_serializer_class = AdaptedBulkListSerializer

class ShipmentPartySerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = ShipmentParty
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class RelatedDocumentsSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    user_add = UserMinimalSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = RelatedDocuments
        fields = '__all__'
        read_only_fields = ['user_add']
        list_serializer_class = AdaptedBulkListSerializer

    def get_file_url(self, obj):
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None

class ShipmentChargesSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    user_add = UserMinimalSerializer(read_only=True)

    class Meta:
        model = ShipmentCharges
        fields = '__all__'
        read_only_fields = ['user_add']
        list_serializer_class = AdaptedBulkListSerializer

class PrePostLegSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    user_add = UserMinimalSerializer(read_only=True)

    class Meta:
        model = PrePostLeg
        fields = '__all__'
        read_only_fields = ['user_add']
        list_serializer_class = AdaptedBulkListSerializer

class TransitSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    poa_details = PortSerializer(source='poa', read_only=True)
    pod_details = PortSerializer(source='pod', read_only=True)
    port_handling_agent_details = UserMinimalSerializer(source='port_handling_agent', read_only=True)
    transit_legs = PrePostLegSerializer(source='transit_post_pre_leg', many=True, read_only=True)

    class Meta:
        model = Transit
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class PickupDeliverySerializer(BulkSerializerMixin,serializers.ModelSerializer):
    user_add = UserMinimalSerializer(read_only=True)
    pod_url = serializers.SerializerMethodField()

    class Meta:
        model = PickupDelivery
        fields = '__all__'
        read_only_fields = ['user_add']
        list_serializer_class = AdaptedBulkListSerializer


    def get_pod_url(self, obj):
        if obj.pod:
            return self.context['request'].build_absolute_uri(obj.pod.url)
        return None

class ShipmentSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    branch_details = serializers.SerializerMethodField()
    client_details = ClientSerializer(source='client', read_only=True)
    consignee_details = RelatedConsigneeSerializer(source='consignee', read_only=True)
    shipper_details = VendorSerializer(source='shipper', read_only=True)
    notify_party_details = VendorSerializer(source='notify_party', read_only=True)
    port_origin_details = PortSerializer(source='port_origin', read_only=True)
    port_destination_details = PortSerializer(source='port_destination', read_only=True)
    port_handling_agent_origin_details = VendorSerializer(source='port_handling_agent_origin', read_only=True)
    port_handling_agent_destination_details = VendorSerializer(source='port_handling_agent_destination', read_only=True)
    user_add_details = UserMinimalSerializer(source='user_add', read_only=True)
    
    # Nested related data
    shipment_packages = ShipmentPackagesSerializer(many=True, read_only=True)
    shipment_party = ShipmentPartySerializer(many=True, read_only=True)
    documents = RelatedDocumentsSerializer(many=True, read_only=True)
    transits = TransitSerializer(many=True, read_only=True)
    shipment_charges = ShipmentChargesSerializer(many=True, read_only=True)
    shipment_pickup = PickupDeliverySerializer(many=True, read_only=True)

    class Meta:
        model = Shipment
        fields = '__all__'
        read_only_fields = ['user_add', 'created', 'updated']
        list_serializer_class = AdaptedBulkListSerializer

    def get_branch_details(self, obj):
        if obj.branch:
            return {
                'id': obj.branch.id,
                'name': obj.branch.name,
                'code': obj.branch.code if hasattr(obj.branch, 'code') else None
            }
        return None

    def validate(self, data):
        # Ensure scheduled dates are logical
        if data.get('scheduled_start_date') and data.get('scheduled_end_date'):
            if data['scheduled_start_date'] > data['scheduled_end_date']:
                raise serializers.ValidationError({
                    "scheduled_end_date": "End date must be after start date"
                })

        # Validate ETA/ETD dates for origin
        if data.get('eta_origin') and data.get('etd_origin'):
            if data['eta_origin'] < data['etd_origin']:
                raise serializers.ValidationError({
                    "eta_origin": "ETA at origin must be after ETD from origin"
                })

        # Validate ETA/ETD dates for destination
        if data.get('eta_origin_destination') and data.get('etd_destination'):
            if data['eta_origin_destination'] < data['etd_destination']:
                raise serializers.ValidationError({
                    "eta_origin_destination": "ETA at destination must be after ETD from destination"
                })

        return data

    def create(self, validated_data):
        # Ensure user is set
        if not validated_data.get('user_add'):
            validated_data['user_add'] = self.context['request'].user
        return super().create(validated_data)

class DriverSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

class FleetSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer        