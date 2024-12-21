# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WarehouseViewSet, ShipmentItemsViewSet, WarehouseStorageViewSet, WarehouseBinViewSet,
    ASNViewSet, GoodsRecieptNoteViewSet, GoodsIssueOrderViewSet, GoodsDispatchOrderViewSet,
    StockTransferViewSet,WarehouseJobOrderViewSet
)
from rest_framework_bulk.routes import BulkRouter

router = BulkRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'shipment-items', ShipmentItemsViewSet)
router.register(r'warehouse-storages', WarehouseStorageViewSet)
router.register(r'warehouse-bins', WarehouseBinViewSet)
router.register(r'asn', ASNViewSet)
router.register(r'goods-receipt-notes', GoodsRecieptNoteViewSet)
router.register(r'goods-issue-orders', GoodsIssueOrderViewSet)
router.register(r'goods-dispatch-orders', GoodsDispatchOrderViewSet)
router.register(r'stock-transfers', StockTransferViewSet)
router.register(r'warehouse-job-order', WarehouseJobOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
