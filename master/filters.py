import django_filters
from .models import UnitofMeasurement, UnitofMeasurementLength, Ports, PackageType, Branch, MasterData,MASTER_DATA_TYPE


class UnitofMeasurementFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    symbol = django_filters.CharFilter(lookup_expr='icontains')
    active = django_filters.BooleanFilter()

    class Meta:
        model = UnitofMeasurement
        fields = ['name', 'symbol', 'active']

class UnitofMeasurementLengthFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    symbol = django_filters.CharFilter(lookup_expr='icontains')
    active = django_filters.BooleanFilter()

    class Meta:
        model = UnitofMeasurementLength
        fields = ['name', 'symbol', 'active']

class PortsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    country = django_filters.CharFilter(lookup_expr='icontains')
    active_status = django_filters.BooleanFilter()

    class Meta:
        model = Ports
        fields = ['name', 'country', 'active_status']

class PackageTypeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    container_type = django_filters.ChoiceFilter(choices=[("LCL", "LCL"), ("FCL", "FCL")])
    active = django_filters.BooleanFilter()

    class Meta:
        model = PackageType
        fields = ['name', 'container_type', 'active']

class BranchFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    city = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Branch
        fields = ['name', 'city', 'status']

class MasterDataFilter(django_filters.FilterSet):
    type_master = django_filters.ChoiceFilter(choices=MASTER_DATA_TYPE)
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = MasterData
        fields = ['type_master', 'name']
