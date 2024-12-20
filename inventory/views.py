from rest_framework_bulk.generics import BulkModelViewSet
from .models import *
from .serializers import *
from .filters import UnitofMeasurementFilter, ProductCategoryFilter, ProductFilter, SecondaryUnitFilter, InventoryAdjustmentFilter
from django_filters.rest_framework import DjangoFilterBackend

class UnitofMeasurementViewSet(BulkModelViewSet):
    queryset = UnitofMeasurement.objects.all()
    serializer_class = UnitofMeasurementSerializer
    filterset_class = UnitofMeasurementFilter

class ProductCategoryViewSet(BulkModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filterset_class = ProductCategoryFilter

class ProductViewSet(BulkModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

class SecondaryUnitViewSet(BulkModelViewSet):
    queryset = SecondaryUnit.objects.all()
    serializer_class = SecondaryUnitSerializer
    filterset_class = SecondaryUnitFilter

class InventoryAdjustmentViewSet(BulkModelViewSet):
    queryset = InventoryAdjustment.objects.all()
    serializer_class = InventoryAdjustmentSerializer
    filterset_class = InventoryAdjustmentFilter

class BillofMaterialsViewSet(BulkModelViewSet):
    queryset = BillofMaterials.objects.all()
    serializer_class = BillofMaterialsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active', 'product', 'type_of_good']  # Filter by active BOM, product, and type_of_good

class BillofMaterialRawMaterialsViewSet(BulkModelViewSet):
    queryset = BillofMaterialRawMateials.objects.all()
    serializer_class = BillofMaterialRawMaterialsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active', 'bom', 'product']  # Filter by active, BOM, and raw material product

class BillofMaterialOutputViewSet(BulkModelViewSet):
    queryset = BillofMaterialOutput.objects.all()
    serializer_class = BillofMaterialOutputSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active', 'bom', 'product']  # Filter by active, BOM, and by-product

class BOMCostingViewSet(BulkModelViewSet):
    queryset = BOMCosting.objects.all()
    serializer_class = BOMCostingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active', 'bom']  # Filter by active and BOM