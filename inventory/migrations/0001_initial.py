# Generated by Django 2.2 on 2020-11-04 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Brand Name')),
                ('logo', models.ImageField(upload_to='logos', verbose_name='Logo')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('supervisor', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='pics/', verbose_name='Image')),
                ('street1', models.CharField(blank=True, max_length=50, verbose_name='Street 1')),
                ('street2', models.CharField(blank=True, max_length=50, verbose_name='Street 2')),
                ('town', models.CharField(blank=True, max_length=20, verbose_name='Town')),
                ('city', models.CharField(blank=True, max_length=20, verbose_name='City')),
                ('state', models.CharField(blank=True, max_length=20, verbose_name='State')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stores', to='inventory.Brand')),
            ],
        ),
    ]
