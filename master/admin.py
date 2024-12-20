from django.contrib import admin
from .models import (
    UnitofMeasurement,
    UnitofMeasurementLength,
    Ports,
    PackageType,
    Branch,
     
)

@admin.register(UnitofMeasurement)
class UnitofMeasurementAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'conversion_to_kg', 'active', 'created_at', 'updated_at', 'add_by')
    search_fields = ('name', 'symbol')
    list_filter = ('active', 'created_at', 'updated_at')

@admin.register(UnitofMeasurementLength)
class UnitofMeasurementLengthAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'conversion_to_cm', 'active', 'created_at', 'updated_at', 'added_by')
    search_fields = ('name', 'symbol')
    list_filter = ('active', 'created_at', 'updated_at')

@admin.register(Ports)
class PortsAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'active_status', 'iso', 'iata', 'edi', 'country', 'region', 'city', 'is_land', 'is_air', 'is_sea', 'active', 'created_at', 'updated_at', 'added_by')
    search_fields = ('name', 'symbol', 'iso', 'iata', 'edi', 'country', 'region', 'city')
    list_filter = ('active_status', 'is_land', 'is_air', 'is_sea', 'active', 'created_at', 'updated_at')

@admin.register(PackageType)
class PackageTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'length', 'breadth', 'width', 'length_unit', 'active', 'created_at', 'updated_at', 'added_by')
    search_fields = ('name',)
    list_filter = ('active', 'created_at', 'updated_at')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('branch_id', 'name', 'address', 'city', 'state', 'postal_code', 'country', 'contact_number', 'email', 'manager_name', 'manager_contact', 'operational_hours', 'status', 'established_date', 'active', 'created_at', 'updated_at', 'added_by')
    search_fields = ('branch_id', 'name', 'city', 'state', 'country')
    list_filter = ('status', 'active', 'created_at', 'updated_at')
    ordering = ['name']
    filter_horizontal = ('incharges',)
    list_per_page = 20

 