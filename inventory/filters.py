import django_filters
from .models import UnitofMeasurement, ProductCategory, Product, SecondaryUnit, InventoryAdjustment

class UnitofMeasurementFilter(django_filters.FilterSet):
    class Meta:
        model = UnitofMeasurement
        fields = {
            'name': ['icontains'],
            'short_name': ['icontains'],
            'accept_fraction': ['exact'],
            'active': ['exact'],
        }

class ProductCategoryFilter(django_filters.FilterSet):
    class Meta:
        model = ProductCategory
        fields = {
            'name': ['icontains'],
            'parent': ['exact'],
            'active': ['exact'],
        }

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
            'product_type': ['exact'],
            'category': ['exact'],
            'hs_code': ['icontains'],
            'active': ['exact'],
        }

class SecondaryUnitFilter(django_filters.FilterSet):
    class Meta:
        model = SecondaryUnit
        fields = {
            'product': ['exact'],
            'active': ['exact'],
        }

class InventoryAdjustmentFilter(django_filters.FilterSet):
    class Meta:
        model = InventoryAdjustment
        fields = {
            'product': ['exact'],
            'date': ['exact', 'gte', 'lte'],
            'stock_type': ['exact'],
            'active': ['exact'],
        }
