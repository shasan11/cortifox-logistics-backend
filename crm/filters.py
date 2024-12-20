import django_filters
from .models import ContactsGroup, Contacts

class ContactsGroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    active = django_filters.BooleanFilter()

    class Meta:
        model = ContactsGroup
        fields = ['name', 'under', 'active', 'user_add']

class ContactsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    contact_group = django_filters.ModelChoiceFilter(queryset=ContactsGroup.objects.all())
    active = django_filters.BooleanFilter()

    class Meta:
        model = Contacts
        fields = ['name', 'phone', 'email', 'contact_group', 'active', 'user_add']
