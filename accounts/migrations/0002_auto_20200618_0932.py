# Generated by Django 2.2.10 on 2020-06-18 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.TextField(blank=True, verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='profile',
            name='primary_phone',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Phone Number'),
        ),
        migrations.AddField(
            model_name='profile',
            name='secondary_phone',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Secondary Phone Number'),
        ),
    ]