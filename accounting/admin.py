from django.contrib import admin
from .models import (
    ChartofAccounts, BankAccounts, Currency,
    PaymentMethod, JournalEntry, JournalEntryItems,
    CashTransfers, ChequeRegister,ChequeIssued,ChequeReceived
)
from accounting.forms import ChequeRegisterForm


@admin.register(ChartofAccounts)
class ChartofAccountsAdmin(admin.ModelAdmin):
    list_display = ('name', 'coa_type', 'code', 'active', 'created', 'updated')
    list_filter = ('coa_type', 'active')
    search_fields = ('name', 'code', 'desc')
    change_form_template='admin/custom/accounting/ChartofAccounts/Form.html'
    change_list_template='admin/custom/accounting/ChartofAccounts/List.html'
    

@admin.register(BankAccounts)
class BankAccountsAdmin(admin.ModelAdmin):
    list_display = ('name', 'acc_type', 'display_name', 'account_number', 'currency', 'active', 'created', 'updated')
    list_filter = ('acc_type', 'type', 'active')
    search_fields = ('name', 'display_name', 'account_number', 'code')
    readonly_fields = ('uuid', 'created', 'updated')
    change_form_template='admin/custom/accounting/BankAccount.html'


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'decimal_places', 'is_default', 'active')
    list_filter = ('is_default', 'active')
    search_fields = ('name', 'symbol')
    readonly_fields = ('created', 'updated')


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'commission', 'active', 'created', 'updated')
    search_fields = ('name', 'desc')
    readonly_fields = ('uuid', 'created', 'updated')


class JournalEntryItemsInline(admin.TabularInline):
    model = JournalEntryItems
    extra = 1


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('jounral_entry_no', 'date', 'reference', 'active', 'created', 'updated')
    search_fields = ('jounral_entry_no', 'reference', 'notes')
    readonly_fields = ('uuid', 'created', 'updated')
    inlines = [JournalEntryItemsInline]


@admin.register(CashTransfers)
class CashTransfersAdmin(admin.ModelAdmin):
    list_display = ('bill_no', 'date', 'paid_from', 'to_account', 'amount', 'exchange_rate', 'active')
    list_filter = ('active',)
    search_fields = ('bill_no', 'reference', 'notes')
    readonly_fields = ('uuid', 'created', 'updated')


@admin.register(ChequeRegister)
class ChequeRegisterAdmin(admin.ModelAdmin):
    form = ChequeRegisterForm
    list_display = ('cheque_no', 'payee_name', 'bank_account', 'status', 'cheque_type', 'amount', 'created', 'updated')
    list_filter = ('status', 'cheque_type', 'active')
    search_fields = ('cheque_no', 'payee_name', 'reference')
    readonly_fields = ('created', 'updated')

@admin.register(ChequeIssued)
class ChequeIssuedAdmin(ChequeRegisterAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(cheque_type='Issued')

@admin.register(ChequeReceived)
class ChequeReceivedAdmin(ChequeRegisterAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(cheque_type='Received')