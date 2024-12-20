from rest_framework import serializers
from .models import Vendor
from rest_framework_bulk.serializers import BulkSerializerMixin
from core.AdaptedBulkListSerializer import AdaptedBulkListSerializer

class VendorSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        list_serializer_class = AdaptedBulkListSerializer

