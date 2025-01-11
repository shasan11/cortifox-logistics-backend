from django.db import migrations, models
from django.core.exceptions import ValidationError
from django.conf import settings


def create_default_records(apps, schema_editor):
    # Create ApplicationSettings if it doesn't exist
    ApplicationSettings = apps.get_model('master', 'ApplicationSettings')
    if not ApplicationSettings.objects.exists():
        ApplicationSettings.objects.create(
            name='My Logistics Company',
            logo='',   
            country='United States',
            state='California',
            address='123 Logistics Blvd, Suite 101, San Francisco, CA, 94101',
            bank_details='Bank: XYZ Bank, Account: 123456789, Branch: San Francisco',
            accounting_details='Account type: Checking, Financial period: January - December',
            financial_period_start='2025-01-01',
            financial_period_end='2025-12-31',
            phone='+1 800 555 1234',
            email='info@logisticscompany.com',
            PAN='ABCPQ1234D'
        )

    # Create ShipmentPrefixes if it doesn't exist
    ShipmentPrefixes = apps.get_model('master', 'ShipmentPrefixes')
    if not ShipmentPrefixes.objects.exists():
        ShipmentPrefixes.objects.create(
            shipment_prefix='SHIP',
            journal_voucher_prefix='JV',
            cash_transfer_prefix='CT',
            packages_prefix='PKG',
            bill_prefix='BILL',
            invoice_prefix='INV',
            credit_note_prefix='CN',
            cheque_prefix='CHQ'
        )


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0004_applicationsettings_pan_applicationsettings_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationSettings',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('name', models.CharField(max_length=255, default='My Logistics Company')),
                ('logo', models.ImageField(upload_to='logos/', default='logos/default_logo.png')),
                ('country', models.CharField(max_length=100, default='United States')),
                ('state', models.CharField(max_length=100, default='California', blank=True, null=True)),
                ('address', models.TextField(default='123 Logistics Blvd, Suite 101, San Francisco, CA, 94101')),
                ('bank_details', models.TextField(default='Bank: XYZ Bank, Account: 123456789, Branch: San Francisco')),
                ('accounting_details', models.TextField(default='Account type: Checking, Financial period: January - December')),
                ('financial_period_start', models.DateField(default='2025-01-01')),
                ('financial_period_end', models.DateField(default='2025-12-31')),
                ('phone', models.CharField(max_length=20, verbose_name="Phone", default='+1 800 555 1234')),
                ('email', models.EmailField(blank=True, null=True, verbose_name="Email", default='info@logisticscompany.com')),
                ('PAN', models.CharField(max_length=20, blank=True, null=True, verbose_name="PAN", default='ABCPQ1234D')),
            ],
            options={
                'verbose_name': 'Singleton Setting',
                'verbose_name_plural': 'Singleton Settings',
            },
        ),
        migrations.CreateModel(
            name='ShipmentPrefixes',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('shipment_prefix', models.CharField(max_length=20, default='SHIP', blank=True, null=True)),
                ('journal_voucher_prefix', models.CharField(max_length=20, default='JV', blank=True, null=True)),
                ('cash_transfer_prefix', models.CharField(max_length=20, default='CT', blank=True, null=True)),
                ('packages_prefix', models.CharField(max_length=20, default='PKG', blank=True, null=True)),
                ('bill_prefix', models.CharField(max_length=20, default='BILL', blank=True, null=True)),
                ('invoice_prefix', models.CharField(max_length=20, default='INV', blank=True, null=True)),
                ('credit_note_prefix', models.CharField(max_length=20, default='CN', blank=True, null=True)),
                ('cheque_prefix', models.CharField(max_length=20, default='CHQ', blank=True, null=True)),
            ],
        ),
        migrations.RunPython(create_default_records),  # Ensure this runs after creating the models
    ]
