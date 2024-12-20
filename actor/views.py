from rest_framework import viewsets
from .models import Vendor
from .serializers import VendorSerializer
from rest_framework_bulk.generics import BulkModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

class VendorViewSet(BulkModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend]
    update_lookup_field = 'uuid'
    filterset_fields = ['active','type','vendor_class',]
