# Generated by Django 5.1.2 on 2024-12-20 08:23

import core.getCurrentUser
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BillofMaterials',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('type_of_good', models.CharField(choices=[('BOM', 'BOM'), ('Production Order', 'Production Order'), ('Production Journal', 'Production Journal')], max_length=100)),
                ('output', models.FloatField(blank=True, null=True)),
                ('manufature_every_order', models.BooleanField(default=False)),
                ('desc_note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(blank=True, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bom_added_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BOMCosting',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('percentage_of_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('production_cost_terms', models.TextField(blank=True, null=True)),
                ('desc_note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(blank=True, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bom_costing', to=settings.AUTH_USER_MODEL)),
                ('bom', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bill_of_material_costing', to='inventory.billofmaterials')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalBOMCosting',
            fields=[
                ('id', models.BigIntegerField(blank=True, db_index=True)),
                ('percentage_of_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('production_cost_terms', models.TextField(blank=True, null=True)),
                ('desc_note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('active', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('added_by', models.ForeignKey(blank=True, db_constraint=False, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('bom', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.billofmaterials')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical bom costing',
                'verbose_name_plural': 'historical bom costings',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalUnitofMeasurement',
            fields=[
                ('id', models.BigIntegerField(blank=True, db_index=True)),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=255)),
                ('desc', models.TextField(blank=True, null=True)),
                ('accept_fraction', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('active', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('added_by', models.ForeignKey(blank=True, db_constraint=False, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical unitof measurement',
                'verbose_name_plural': 'historical unitof measurements',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('product_type', models.CharField(choices=[('Goods', 'Goods'), ('Service', 'Service')], max_length=100)),
                ('code', models.CharField(max_length=100)),
                ('hs_code', models.CharField(max_length=100)),
                ('selling_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('purchase_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('stock', models.FloatField(default=0)),
                ('added_by', models.ForeignKey(blank=True, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_added', to=settings.AUTH_USER_MODEL)),
                ('purchase_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_account_product', to='accounting.chartofaccounts')),
                ('purchase_account_return', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_account_return_product', to='accounting.chartofaccounts')),
                ('sales_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_account_product', to='accounting.chartofaccounts')),
                ('sales_account_return', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_account_return_product', to='accounting.chartofaccounts')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryAdjustment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('reference', models.CharField(blank=True, max_length=30, null=True)),
                ('quantity', models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('stock_type', models.CharField(choices=[('In', 'In'), ('Out', 'Out')], max_length=100)),
                ('rate', models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('desc_note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(blank=True, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_inventory_adjustment_added', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventory_adjustment_product', to='inventory.product')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalBillofMaterials',
            fields=[
                ('id', models.BigIntegerField(blank=True, db_index=True)),
                ('type_of_good', models.CharField(choices=[('BOM', 'BOM'), ('Production Order', 'Production Order'), ('Production Journal', 'Production Journal')], max_length=100)),
                ('output', models.FloatField(blank=True, null=True)),
                ('manufature_every_order', models.BooleanField(default=False)),
                ('desc_note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('active', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('added_by', models.ForeignKey(blank=True, db_constraint=False, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.product')),
            ],
            options={
                'verbose_name': 'historical billof materials',
                'verbose_name_plural': 'historical billof materialss',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalBillofMaterialRawMateials',
            fields=[
                ('id', models.BigIntegerField(blank=True, db_index=True)),
                ('output', models.FloatField()),
                ('desc_note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('active', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('added_by', models.ForeignKey(blank=True, db_constraint=False, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('bom', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.billofmaterials')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.product')),
            ],
            options={
                'verbose_name': 'historical billof material raw mateials',
                'verbose_name_plural': 'historical billof material raw mateialss',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalBillofMaterialOutput',
            fields=[
                ('id', models.BigIntegerField(blank=True, db_index=True)),
                ('output', models.FloatField(blank=True, null=True)),
                ('percentage_of_cost', models.FloatField()),
                ('desc_note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('active', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('added_by', models.ForeignKey(blank=True, db_constraint=False, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('bom', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.billofmaterials')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.product')),
            ],
            options={
                'verbose_name': 'historical billof material output',
                'verbose_name_plural': 'historical billof material outputs',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='billofmaterials',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bom_product', to='inventory.product'),
        ),
        migrations.CreateModel(
            name='BillofMaterialRawMateials',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('output', models.FloatField()),
                ('desc_note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(blank=True, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bom_raw_material_added', to=settings.AUTH_USER_MODEL)),
                ('bom', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bill_of_material', to='inventory.billofmaterials')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='raw_material', to='inventory.product')),
            ],
        ),
        migrations.CreateModel(
            name='BillofMaterialOutput',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('output', models.FloatField(blank=True, null=True)),
                ('percentage_of_cost', models.FloatField()),
                ('desc_note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(blank=True, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bom_output_added', to=settings.AUTH_USER_MODEL)),
                ('bom', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bill_of_material_output', to='inventory.billofmaterials')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='by_product', to='inventory.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('desc', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(blank=True, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_category_added', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children_product_category', to='inventory.productcategory')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.productcategory'),
        ),
        migrations.CreateModel(
            name='HistoricalProductCategory',
            fields=[
                ('id', models.BigIntegerField(blank=True, db_index=True)),
                ('name', models.CharField(max_length=255)),
                ('desc', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('active', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('added_by', models.ForeignKey(blank=True, db_constraint=False, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.productcategory')),
            ],
            options={
                'verbose_name': 'historical product category',
                'verbose_name_plural': 'historical product categorys',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('id', models.BigIntegerField(blank=True, db_index=True)),
                ('name', models.CharField(max_length=255)),
                ('product_type', models.CharField(choices=[('Goods', 'Goods'), ('Service', 'Service')], max_length=100)),
                ('code', models.CharField(max_length=100)),
                ('hs_code', models.CharField(max_length=100)),
                ('selling_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('purchase_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('active', models.BooleanField(default=True)),
                ('stock', models.FloatField(default=0)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('added_by', models.ForeignKey(blank=True, db_constraint=False, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('purchase_account', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounting.chartofaccounts')),
                ('purchase_account_return', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounting.chartofaccounts')),
                ('sales_account', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounting.chartofaccounts')),
                ('sales_account_return', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounting.chartofaccounts')),
                ('category', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.productcategory')),
            ],
            options={
                'verbose_name': 'historical product',
                'verbose_name_plural': 'historical products',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='SecondaryUnit',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('conversion_rate', models.FloatField(default=0)),
                ('selling_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('purchase_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(blank=True, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_sec_unit_added', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sec_unit_product', to='inventory.product')),
            ],
        ),
        migrations.CreateModel(
            name='UnitofMeasurement',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=255)),
                ('desc', models.TextField(blank=True, null=True)),
                ('accept_fraction', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(blank=True, default=core.getCurrentUser.get_current_user, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unit_of_measurement_added', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]