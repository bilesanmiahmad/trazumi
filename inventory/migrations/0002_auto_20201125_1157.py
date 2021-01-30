# Generated by Django 2.2.13 on 2020-11-25 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0005_auto_20201125_1157'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='city',
        ),
        migrations.RemoveField(
            model_name='store',
            name='image',
        ),
        migrations.RemoveField(
            model_name='store',
            name='state',
        ),
        migrations.RemoveField(
            model_name='store',
            name='street1',
        ),
        migrations.RemoveField(
            model_name='store',
            name='street2',
        ),
        migrations.RemoveField(
            model_name='store',
            name='town',
        ),
        migrations.AddField(
            model_name='brand',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='brands', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='cost_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='products_by', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images'),
        ),
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(default='test product', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='store_products', to='inventory.Store'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='selling_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='store',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='addresses', to='accounts.Address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='store',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='stores', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='store',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='brand_stores', to='inventory.Brand'),
        ),
    ]