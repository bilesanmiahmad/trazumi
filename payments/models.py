import uuid
from django.db import models
from accounts.models import User
from inventory.models import Product

# Create your models here.

class PaymentType(models.Model):
    name = models.CharField(
        'Payment Type Name',
        max_length=20
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        'Updated',
        auto_now=True,
    )


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='payments'
    )


class Transaction(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='transactions')
    cart = models.ForeignKey('Cart', on_delete=models.DO_NOTHING, related_name='carts')
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='product')
    quantity = models.IntegerField(default=1)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)