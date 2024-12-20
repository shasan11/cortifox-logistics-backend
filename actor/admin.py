from django.contrib import admin
from .models import Vendor

from django import forms
from .models import Vendor
from image_uploader_widget.widgets import ImageUploaderWidget

class VendorAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the `vendor_class` based on the instance's proxy model type
        if isinstance(self.instance, BookingAgentVendor):
            self.fields['vendor_class'].initial = 'Booking Agent'
        elif isinstance(self.instance, CarrierVendor):
            self.fields['vendor_class'].initial = 'Carrier'
        elif isinstance(self.instance, CustomsAgentVendor):
            self.fields['vendor_class'].initial = 'Customs Agent'
        elif isinstance(self.instance, VendorVendor):
            self.fields['vendor_class'].initial = 'Vendor'
        # Disable the vendor_class field to prevent changes
        self.fields['vendor_class'].disabled = True

    class Meta:
        model = Vendor
        fields = '__all__'
        widgets = {
            'image': ImageUploaderWidget(),  # Use image uploader widget for the image field
            'name': forms.TextInput(attrs={'placeholder': 'Enter vendor name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'country': forms.TextInput(attrs={'placeholder': 'Enter country name'}),
            'state': forms.TextInput(attrs={'placeholder': 'Enter state'}),
            'acc_no': forms.TextInput(attrs={'placeholder': 'Enter account number'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter address'}),
            'credit_limit': forms.NumberInput(attrs={'placeholder': 'Enter credit limit'}),
            'no_of_days': forms.NumberInput(attrs={'placeholder': 'Enter number of days'}),
            'bank_info': forms.Textarea(attrs={'placeholder': 'Enter bank information'}),
            'trn': forms.TextInput(attrs={'placeholder': 'Enter TRN'}),
            'iata': forms.TextInput(attrs={'placeholder': 'Enter IATA'}),
        }

 
 

# Define proxy models for each vendor class
class BookingAgentVendor(Vendor):
    class Meta:
        proxy = True
        verbose_name = 'Booking Agent'
        verbose_name_plural = 'Booking Agent'


class CarrierVendor(Vendor):
    class Meta:
        proxy = True
        verbose_name = 'Carrier'
        verbose_name_plural = 'Carrier'


 

class CustomsAgentVendor(Vendor):
    class Meta:
        proxy = True
        verbose_name = 'Customs Agent'
        verbose_name_plural = 'Customs'


 

class VendorVendor(Vendor):
    class Meta:
        proxy = True
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'


# Define custom admin classes if needed
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor_class', 'email', 'phone', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'vendor_class', 'email', 'phone')
    change_form_template='admin/custom/actor/form.html'
    add_form_template=change_form_template
    form=VendorAdminForm
    change_list_template="admin/custom/actor/list.html"

# Register each proxy model in the admin panel
admin.site.register(BookingAgentVendor, VendorAdmin)
admin.site.register(CarrierVendor, VendorAdmin)
 
admin.site.register(CustomsAgentVendor, VendorAdmin)
 
admin.site.register(VendorVendor, VendorAdmin)
