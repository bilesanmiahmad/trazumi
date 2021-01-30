from django.contrib import admin
from .models import Brand, Store, Product, Address

# Register your models here.
admin.site.register(Address)
admin.site.register(Brand)
admin.site.register(Store)
admin.site.register(Product)
