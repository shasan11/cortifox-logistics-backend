from django.contrib import admin
from .models import Shipment, ShipmentParty, ShipmentPackages, Transit
from simple_history.admin import SimpleHistoryAdmin

class ShipmentAdmin(SimpleHistoryAdmin):
    list_display = ('shipment_no', 'si_no', 'shipment_type', 'shipment_status', 'client', 'created', 'updated')
    search_fields = ('shipment_no', 'si_no', 'client__name')
    list_filter = ('shipment_type', 'shipment_status', 'client')
    ordering = ('-created',)
    list_per_page = 20

class ShipmentPartyAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'type', 'name', 'phone', 'email', 'address')
    search_fields = ('shipment__shipment_no', 'name', 'email')
    list_filter = ('type',)
    ordering = ('-shipment',)
    list_per_page = 20

class ShipmentPackagesAdmin(admin.ModelAdmin):
    list_display = ('shipment_package', 'good_desc', 'hs_code', 'package_type', 'length', 'width', 'height', 'gross_weight', 'quantity', 'volumetric_weight', 'chargable')
    search_fields = ('shipment_package', 'good_desc', 'hs_code')
    list_filter = ('package_type', 'mass_unit', 'package_unit')
    ordering = ('-shipment',)
    list_per_page = 20

class TransitAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'type', 'transport_mode', 'poa', 'pod', 'eta', 'eta', 'transportation_type', 'tracking_no')
    search_fields = ('shipment__shipment_no', 'type', 'tracking_no')
    list_filter = ('transport_mode', 'transportation_type', 'poa', 'pod')
    ordering = ('-shipment',)
    list_per_page = 20

# Registering the models with their respective admin classes
admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(ShipmentParty, ShipmentPartyAdmin)
admin.site.register(ShipmentPackages, ShipmentPackagesAdmin)
admin.site.register(Transit, TransitAdmin)
