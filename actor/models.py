from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from core.getCurrentUser import get_current_user
from accounting.models import ChartofAccounts
from simple_history.models import HistoricalRecords
import re


# Define choices for the type field
TYPE_CHOICES = [
    ('individual', 'Individual'),
    ('company', 'Company'),
]

VENDOR_CLASS_CHOICES = [
    ('Booking Agent', 'Booking Agent'),
    ('Carrier', 'Carrier'),
    ('Customer', 'Customer'),
    ('Customs Agent', 'Customs Agent'),
    ('Employee', 'Employee'),
    ('Vendor', 'Vendor'),
]

TRANSPORT_MEDIUM = (
    ("Air", "Air"),
    ("Sea", "Sea"),
    ("Land", "Land"),
)

class Vendor(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to='vendor_images', blank=True, null=True)
    vendor_class = models.CharField(max_length=20, choices=VENDOR_CLASS_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)
    account_head = models.ForeignKey(ChartofAccounts, on_delete=models.PROTECT)
    country_code = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    acc_no = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField()
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    no_of_days = models.IntegerField(default=0)
    bank_info = models.TextField()
    trn = models.CharField(max_length=50, blank=True, null=True)
    iata = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_add = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, default=get_current_user, verbose_name="added_by_vendor")
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='vendor_user', blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    # Custom clean method for validation
    def clean(self):
        # Validate `vendor_class`
        if self.vendor_class not in dict(VENDOR_CLASS_CHOICES).keys():
            raise ValidationError({'vendor_class': 'Invalid vendor class selected.'})

        # Validate `type`
        if self.type not in dict(TYPE_CHOICES).keys():
            raise ValidationError({'type': 'Invalid type selected.'})

        # Validate `name`
        if not self.name:
            raise ValidationError({'name': 'Name cannot be blank.'})

        # Validate `phone`
        if self.phone:
            if len(self.phone) > 20:
                raise ValidationError({'phone': 'Phone number cannot exceed 20 characters.'})
            if not re.match(r'^\+?1?\d{9,15}$', self.phone):  # Simple regex to validate international phone number
                raise ValidationError({'phone': 'Enter a valid phone number.'})

        # Validate `email`
        if self.email:
            if len(self.email) > 254:  # Check for max length of email (RFC 5321)
                raise ValidationError({'email': 'Email address cannot exceed 254 characters.'})

        # Validate `country_code`
        if len(self.country_code) > 255:
            raise ValidationError({'country_code': 'Country code cannot exceed 255 characters.'})

        # Validate `country` and `state`
        if len(self.country) > 50:
            raise ValidationError({'country': 'Country name cannot exceed 50 characters.'})
        if len(self.state) > 50:
            raise ValidationError({'state': 'State name cannot exceed 50 characters.'})

        # Validate `credit_limit`
        if self.credit_limit and (self.credit_limit < 0 or self.credit_limit > 99999999.99):
            raise ValidationError({'credit_limit': 'Credit limit must be a positive number and less than 100 million.'})

        # Validate `no_of_days`
        if self.no_of_days < 0:
            raise ValidationError({'no_of_days': 'Number of days cannot be negative.'})

        # Validate `acc_no`
        if self.acc_no and len(self.acc_no) > 50:
            raise ValidationError({'acc_no': 'Account number cannot exceed 50 characters.'})

        # Validate `trn` and `iata`
        if self.trn and len(self.trn) > 50:
            raise ValidationError({'trn': 'TRN number cannot exceed 50 characters.'})
        if self.iata and len(self.iata) > 50:
            raise ValidationError({'iata': 'IATA code cannot exceed 50 characters.'})

        # Validate `bank_info`
        if len(self.bank_info) > 500:  # Limiting the bank info to 500 characters
            raise ValidationError({'bank_info': 'Bank information cannot exceed 500 characters.'})

        # Validate `user_add` (must be a valid user, default should be the current user)
        if not self.user_add:
            raise ValidationError({'user_add': 'User adding the vendor is required.'})

        # Validate `user` (if provided)
        if self.user and not isinstance(self.user, User):
            raise ValidationError({'user': 'The user field must reference a valid user.'})

    # Override save to call clean method before saving
    def save(self, *args, **kwargs):
        self.clean()  # Ensure custom validation is called
        super().save(*args, **kwargs)
