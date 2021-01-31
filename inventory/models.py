from django.db import models
from accounts.models import User, Address
# Create your models here.

class Brand(models.Model):
    name = models.CharField(
        'Brand Name',
        max_length=30
    )
    logo = models.ImageField(
        'Logo',
        upload_to='logos',
        blank=True,
        null=True
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.DO_NOTHING, 
        related_name='brands'
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        'Updated',
        auto_now=True
    )

    def __str__(self):
        return '{name}'.format(name=self.name)


class Store(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name='brand_stores'
    )
    address = models.ForeignKey(
        Address, 
        on_delete=models.DO_NOTHING, 
        related_name='addresses'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.DO_NOTHING, 
        related_name='stores'
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        'Updated',
        auto_now=True,
    )

    def __str__(self):
        return '{name} -- {city}'.format(name=self.brand.name, city=self.address.city)


class Product(models.Model):
    name = models.CharField(
        max_length=100
    )
    owner = models.ForeignKey(Store, on_delete=models.DO_NOTHING, related_name='store_products')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='products_by')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{name} by {brand}, {city}'.format(name=self.name, brand=self.owner.brand.name, city=self.owner.address.city)
