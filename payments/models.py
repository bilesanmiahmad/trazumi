from django.db import models
from accounts.models import User

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