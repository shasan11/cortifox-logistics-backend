# forms.py

from django import forms
from .models import Client, Ticket, ClientDocuments, RelatedConsignee

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter client name'}),
            'type': forms.Select(attrs={'placeholder': 'Select client type'}),
            'contact_person': forms.TextInput(attrs={'placeholder': 'Enter contact person'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'address1': forms.Textarea(attrs={'placeholder': 'Enter address 1'}),
            'address2': forms.Textarea(attrs={'placeholder': 'Enter address 2'}),
            'post_box_no': forms.TextInput(attrs={'placeholder': 'Enter post box number'}),
            'province': forms.TextInput(attrs={'placeholder': 'Enter province'}),
            'country': forms.TextInput(attrs={'placeholder': 'Enter country'}),
            'payment_terms': forms.Select(attrs={'placeholder': 'Select payment terms'}),
            # Add placeholders for other fields as needed
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter ticket title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter ticket description'}),
            'status': forms.Select(attrs={'placeholder': 'Select status'}),
            'priority': forms.Select(attrs={'placeholder': 'Select priority'}),
            # Add placeholders for other fields as needed
        }

class ClientDocumentsForm(forms.ModelForm):
    class Meta:
        model = ClientDocuments
        fields = '__all__'
        widgets = {
            'document_name': forms.TextInput(attrs={'placeholder': 'Enter document name'}),
            'document_no': forms.TextInput(attrs={'placeholder': 'Enter document ID/Code'}),
            'file': forms.FileInput(attrs={'placeholder': 'Upload file'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description'}),
            # Add placeholders for other fields as needed
        }

class RelatedConsigneeForm(forms.ModelForm):
    class Meta:
        model = RelatedConsignee
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'placeholder': 'Enter address'}),
            'consignor_name': forms.TextInput(attrs={'placeholder': 'Enter consignor name'}),
            'consigner_phone': forms.TextInput(attrs={'placeholder': 'Enter consignor phone number'}),
            'consigner_email': forms.EmailInput(attrs={'placeholder': 'Enter consignor email address'}),
            'remarks': forms.Textarea(attrs={'placeholder': 'Enter remarks'}),
            # Add placeholders for other fields as needed
        }
