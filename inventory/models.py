from django.db import models
from accounts.models import User
# Create your models here.

class Brand(models.Model):
    name = models.CharField(
        'Brand Name',
        max_length=30
    )
    supervisor = models.OneToOneField(
        User,
        on_delete=models.PROTECT,        
    )
    logo = models.ImageField(
        'Logo',
        upload_to='logos'
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        'Updated',
        auto_now=True
    )


class Store(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name='stores'
    )
    image = models.ImageField(
        'Image',
        upload_to='pics/'
    )
    street1 = models.CharField(
        'Street 1',
        max_length=50,
        blank=True
    )
    street2 = models.CharField(
        'Street 2',
        max_length=50,
        blank=True,
    )
    town = models.CharField(
        'Town',
        max_length=20,
        blank=True,
    )
    city = models.CharField(
        'City',
        max_length=20,
        blank=True,
    )
    state = models.CharField(
        'State',
        max_length=20,
        blank=True,
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        'Updated',
        auto_now=True,
    )


class Product(models.Model):
    pass