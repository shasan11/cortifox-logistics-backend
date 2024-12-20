from django import forms
from .models import ChequeRegister,ChequeIssued,ChequeReceived

class ChequeRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the `vendor_class` based on the instance's proxy model type
        if isinstance(self.instance, ChequeIssued):
            self.fields['cheque_type'].initial = 'issued'
        elif isinstance(self.instance,ChequeReceived):
            self.fields['cheque_type'].initial = 'recieved'
        # Disable the vendor_class field to prevent changes
        self.fields['cheque_type'].disabled = True
    class Meta:
        model = ChequeRegister
        fields = ['cheque_no', 'payee_name', 'bank_account', 'status', 'cheque_type', 'amount']
        widgets = {
            'cheque_no': forms.TextInput(attrs={'placeholder': 'Enter Cheque Number'}),
            'payee_name': forms.TextInput(attrs={'placeholder': 'Enter Payee Name'}),
            'bank_account': forms.Select(attrs={'placeholder': 'Select Bank Account'}),
            'status': forms.Select(attrs={'placeholder': 'Enter Status'}),
            'cheque_type': forms.Select(attrs={'placeholder': 'Enter Cheque Type'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter Amount'}),
            'image': forms.ClearableFileInput(attrs={'placeholder': 'Upload Cheque Image'}),
        }
