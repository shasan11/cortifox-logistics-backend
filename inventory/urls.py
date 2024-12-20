from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UnitofMeasurementViewSet, ProductCategoryViewSet, ProductViewSet, SecondaryUnitViewSet, InventoryAdjustmentViewSet
from rest_framework_bulk.routes import BulkRouter
router = BulkRouter()
router.register(r'unit-of-measurements', UnitofMeasurementViewSet)
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'secondary-units', SecondaryUnitViewSet)
router.register(r'inventory-adjustments', InventoryAdjustmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
