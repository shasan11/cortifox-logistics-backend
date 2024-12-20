from django.contrib import admin

from crm.models import Contacts,ContactsGroup

admin.site.register(ContactsGroup)

admin.site.register(Contacts)
# Register your models here.
