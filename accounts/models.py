from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        'Email Address',
        unique=True
    )
    username = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    first_name = models.CharField(
        'First Name',
        max_length=30,
        blank=True
    )
    last_name = models.CharField(
        'Last Name',
        max_length=30,
        blank=True
    )
    date_joined = models.DateTimeField(
        'Date Joined',
        auto_now_add=True
    )
    is_active = models.BooleanField(
        'Active',
        default=True
    )
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name
    
    def get_short_name(self):
        return self.first_name


class Profile(models.Model):
    AGENT = 'AG'
    CUSTOMER = 'CU'

    USER_TYPES = (
        (AGENT, 'Agent'),
        (CUSTOMER, 'Customer'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
        related_name='profile'
    )
    device_type = models.CharField(
        'Device Type',
        max_length=15
    )
    location = models.CharField(
        'Location',
        max_length=5
    )
    ip_address = models.GenericIPAddressField(
        'IP Address',
    )
    user_type = models.CharField(
        'User Type',
        max_length=5,
        choices=USER_TYPES,
        default=AGENT
    )
    primary_phone = models.BigIntegerField(
        'Phone Number',
    )
    secondary_phone = models.BigIntegerField(
        'Secondary Phone Number',
        blank=True,
        null=True,
    )
    address = models.TextField(
        'Address',
        blank=True,
    )

    def __str__(self):
        return self.user.email

