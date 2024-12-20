# admin.py

from django.contrib import admin
from .models import Client, Ticket, ClientDocuments, RelatedConsignee
from .forms import ClientForm, TicketForm, ClientDocumentsForm, RelatedConsigneeForm

class TicketInline(admin.TabularInline):
    model = Ticket
    form = TicketForm
    extra = 1

class ClientDocumentsInline(admin.TabularInline):
    model = ClientDocuments
    form = ClientDocumentsForm
    extra = 1

class RelatedConsigneeInline(admin.TabularInline):
    model = RelatedConsignee
    form = RelatedConsigneeForm
    extra = 1

class ClientAdmin(admin.ModelAdmin):
    form = ClientForm
    list_display = ('name', 'type', 'contact_person', 'phone', 'email', 'active')
    inlines = [TicketInline, ClientDocumentsInline, RelatedConsigneeInline]

admin.site.register(Client, ClientAdmin)
