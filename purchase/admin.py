from django import forms
from django.contrib import admin
from .models import Costing, VendorPayment, VendorCreditDebitNote, Expense, NotesItem

class CostingAdminForm(forms.ModelForm):
    class Meta:
        model = Costing
        fields = '__all__'
        widgets = {
            'costing_number': forms.TextInput(attrs={'placeholder': 'Enter Costing Number'}),
            'created_date_editable': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            # Add other fields as needed
        }
        labels = {
            'costing_number': 'Costing Number',
            'created_date_editable': 'Editable Created Date',
            # Add other labels as needed
        }

class VendorPaymentAdminForm(forms.ModelForm):
    class Meta:
        model = VendorPayment
        fields = '__all__'
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter Amount'}),
            'payment_date': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            # Add other fields as needed
        }
        labels = {
            'amount': 'Payment Amount',
            'payment_date': 'Payment Date',
            # Add other labels as needed
        }

class VendorCreditDebitNoteAdminForm(forms.ModelForm):
    class Meta:
        model = VendorCreditDebitNote
        fields = '__all__'
        widgets = {
            'note_number': forms.TextInput(attrs={'placeholder': 'Enter Note Number'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter Amount'}),
            # Add other fields as needed
        }
        labels = {
            'note_number': 'Note Number',
            'amount': 'Amount',
            # Add other labels as needed
        }

class ExpenseAdminForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        widgets = {
            'bill_no': forms.TextInput(attrs={'placeholder': 'Enter Bill Number'}),
            'date': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            # Add other fields as needed
        }
        labels = {
            'bill_no': 'Bill Number',
            'date': 'Expense Date',
            # Add other labels as needed
        }

class NotesItemAdminForm(forms.ModelForm):
    class Meta:
        model = NotesItem
        fields = '__all__'
        widgets = {
            'product': forms.TextInput(attrs={'placeholder': 'Enter Product'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter Amount'}),
            # Add other fields as needed
        }
        labels = {
            'product': 'Product Name',
            'amount': 'Amount',
            # Add other labels as needed
        }

class CostingAdmin(admin.ModelAdmin):
    form = CostingAdminForm

class VendorPaymentAdmin(admin.ModelAdmin):
    form = VendorPaymentAdminForm

class VendorCreditDebitNoteAdmin(admin.ModelAdmin):
    form = VendorCreditDebitNoteAdminForm

class ExpenseAdmin(admin.ModelAdmin):
    form = ExpenseAdminForm

class NotesItemAdmin(admin.ModelAdmin):
    form = NotesItemAdminForm

admin.site.register(Costing, CostingAdmin)
admin.site.register(VendorPayment, VendorPaymentAdmin)
admin.site.register(VendorCreditDebitNote, VendorCreditDebitNoteAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(NotesItem, NotesItemAdmin)
