from django.db import migrations, models
from django.core.exceptions import ValidationError


def create_default_records(apps, schema_editor):
    # Create ApplicationSettings with ID 1 if it doesn't exist
    ApplicationSettings = apps.get_model('master', 'ApplicationSettings')
    if not ApplicationSettings.objects.filter(id=1).exists():
        ApplicationSettings.objects.create()

    # Create ShipmentPrefixes with ID 1 if it doesn't exist
    ShipmentPrefixes = apps.get_model('master', 'ShipmentPrefixes')
    if not ShipmentPrefixes.objects.filter(id=1).exists():
        ShipmentPrefixes.objects.create()


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0008_merge_20250111_2107'),
    ]

    operations = [
        migrations.RunPython(create_default_records),  # Run the function after applying migrations
    ]
